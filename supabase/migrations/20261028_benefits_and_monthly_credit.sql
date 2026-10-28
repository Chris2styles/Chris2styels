-- Healthy Hair Club: membership benefit tracking + Elite credit expiring monthly.
-- Rules approved by Christine on 28 Oct 2026:
--   * Membership year starts on the join date. Unused complimentary services expire at the end of the year.
--   * Essential: 1 full maintenance service per 3-month block, first block starting in the 3rd month
--     of membership (join + 2 months); 1 extra complimentary eligible service per membership year.
--   * Signature / Elite: 1 maintenance service per membership month; 2 extra complimentary services per year.
--   * Elite: GBP 30 styling credit per paid month; unused credit expires when the next month's credit is issued.
-- Not decided yet (left to admin judgement, nothing automatic): which services count as "complimentary
-- eligible", aftercare product allocation, family credit transfers, tier changes.

-- 1. Redemption history (never deleted; one row per benefit used)
create table if not exists public.benefit_redemptions (
  id uuid primary key default extensions.uuid_generate_v4(),
  membership_id uuid not null references public.memberships(id),
  client_id uuid not null references public.clients(id),
  booking_id uuid references public.bookings(id),
  kind text not null check (kind in ('maintenance','complimentary','aftercare')),
  period_start date,
  period_end date,
  service text,
  note text,
  created_by text,
  created_at timestamptz not null default now()
);
-- A booking can use each benefit at most once; a maintenance block can be used at most once.
create unique index if not exists benefit_one_per_booking on public.benefit_redemptions(booking_id, kind) where booking_id is not null and kind in ('maintenance','complimentary');
create unique index if not exists benefit_one_maintenance_per_period on public.benefit_redemptions(membership_id, period_start) where kind = 'maintenance';
create index if not exists benefit_redemptions_membership_idx on public.benefit_redemptions(membership_id, kind, period_start);
alter table public.benefit_redemptions enable row level security;
drop policy if exists benefit_select_own_or_admin on public.benefit_redemptions;
create policy benefit_select_own_or_admin on public.benefit_redemptions for select
  using (public.is_admin() or client_id in (select id from public.clients where email = auth.email()));

-- 2. Benefit windows. Pure date maths, so it can be tested on its own.
--    Returns the window containing p_on (or the first future window if none has started yet).
create or replace function public.hhc_window(p_pkg text, p_start date, p_kind text, p_on date)
returns table(window_start date, window_end date, allowed int, started boolean)
language plpgsql immutable set search_path = public as $$
declare months int; k int;
begin
  months := (date_part('year', age(p_on, p_start)) * 12 + date_part('month', age(p_on, p_start)))::int;
  if p_on < p_start then months := 0; end if;
  -- age() undercounts around month ends (e.g. joined 31 Jan, on 28 Feb); step forward until the window contains p_on.
  while (p_start + make_interval(months => months + 1))::date <= p_on loop months := months + 1; end loop;
  if p_kind = 'complimentary' then
    k := months / 12;
    window_start := (p_start + make_interval(months => 12 * k))::date;
    window_end := (p_start + make_interval(months => 12 * (k + 1)))::date - 1;
    allowed := case when p_pkg = 'essential' then 1 else 2 end;
    started := true;
  elsif p_kind = 'maintenance' and p_pkg = 'essential' then
    if months < 2 then
      window_start := (p_start + make_interval(months => 2))::date;
      window_end := (p_start + make_interval(months => 5))::date - 1;
      allowed := 1; started := false;
    else
      k := (months - 2) / 3;
      window_start := (p_start + make_interval(months => 2 + 3 * k))::date;
      window_end := (p_start + make_interval(months => 5 + 3 * k))::date - 1;
      allowed := 1; started := true;
    end if;
  elsif p_kind = 'maintenance' then
    window_start := (p_start + make_interval(months => months))::date;
    window_end := (p_start + make_interval(months => months + 1))::date - 1;
    allowed := 1; started := true;
  else
    raise exception 'unknown benefit %', p_kind;
  end if;
  return next;
end; $$;

-- Services that use the maintenance allowance.
create or replace function public.hhc_is_maintenance(p_service text) returns boolean
language sql immutable as $$ select p_service in ('Monthly Maintenance','Quarterly Maintenance') $$;

-- 3. What a member has left. Members see only their own; admin and the server see anyone's.
create or replace function public.membership_benefits(p_membership uuid, p_on date default current_date)
returns json language plpgsql stable security definer set search_path = public as $$
declare m public.memberships; c public.clients; mw record; cw record; mused int; cused int;
begin
  select * into m from public.memberships where id = p_membership;
  if not found then raise exception 'membership not found'; end if;
  select * into c from public.clients where id = m.client_id;
  if not (public.is_admin() or coalesce(auth.role(),'') = 'service_role' or lower(c.email) = lower(auth.email())) then
    raise exception 'not allowed';
  end if;
  select * into mw from public.hhc_window(m.package, m.created_at::date, 'maintenance', p_on);
  select * into cw from public.hhc_window(m.package, m.created_at::date, 'complimentary', p_on);
  select count(*) into mused from public.benefit_redemptions where membership_id = m.id and kind = 'maintenance' and period_start = mw.window_start;
  select count(*) into cused from public.benefit_redemptions where membership_id = m.id and kind = 'complimentary' and period_start = cw.window_start;
  return json_build_object(
    'package', m.package, 'status', m.status, 'member_since', m.created_at::date,
    'maintenance', json_build_object('cadence', case when m.package = 'essential' then 'quarterly' else 'monthly' end,
      'window_start', mw.window_start, 'window_end', mw.window_end, 'started', mw.started,
      'allowed', mw.allowed, 'used', mused, 'remaining', case when mw.started then greatest(mw.allowed - mused, 0) else 0 end),
    'complimentary', json_build_object('window_start', cw.window_start, 'window_end', cw.window_end,
      'allowed', cw.allowed, 'used', cused, 'remaining', greatest(cw.allowed - cused, 0)),
    'aftercare', m.package in ('signature','elite'),
    'credit', case when m.package = 'elite' then public.credit_balance(m.id) else null end
  );
end; $$;
revoke execute on function public.membership_benefits(uuid, date) from public, anon;
grant execute on function public.membership_benefits(uuid, date) to authenticated, service_role;

-- 4. Elite credit expires monthly: when a new month's credit is issued, any unused balance is expired first.
alter table public.credit_ledger drop constraint if exists credit_ledger_kind_check;
alter table public.credit_ledger add constraint credit_ledger_kind_check check (kind in ('issue','redeem','adjustment','expiry'));

create or replace function public.issue_elite_credit(p_membership uuid, p_invoice text, p_amount numeric) returns numeric
language plpgsql security definer set search_path = public as $$
declare m public.memberships; prev numeric;
begin
  select * into m from public.memberships where id = p_membership for update;
  if not found then raise exception 'membership not found'; end if;
  if m.package <> 'elite' then return public.credit_balance(p_membership); end if;
  -- Same invoice twice (Stripe retry): do nothing.
  if exists (select 1 from public.credit_ledger where stripe_invoice_id = p_invoice and kind = 'issue') then
    return public.credit_balance(m.id);
  end if;
  prev := public.credit_balance(m.id);
  if prev > 0 then
    insert into public.credit_ledger(membership_id, client_id, kind, amount, stripe_invoice_id, note, created_by)
    values (m.id, m.client_id, 'expiry', -prev, p_invoice, 'Unused credit expired at end of month', 'stripe');
  end if;
  insert into public.credit_ledger(membership_id, client_id, kind, amount, stripe_invoice_id, note, created_by)
  values (m.id, m.client_id, 'issue', p_amount, p_invoice, 'Monthly Elite styling credit', 'stripe');
  update public.memberships set style_credit = public.credit_balance(m.id) where id = m.id;
  return public.credit_balance(m.id);
end; $$;
revoke execute on function public.issue_elite_credit(uuid,text,numeric) from public, anon, authenticated;

-- 5. Approving a booking now records benefit use. Old 2-argument version is replaced.
drop function if exists public.approve_booking(uuid, numeric);
create or replace function public.approve_booking(p_booking uuid, p_credit numeric default 0, p_use_complimentary boolean default false)
returns json language plpgsql security definer set search_path = public as $$
declare b public.bookings; m public.memberships; bal numeric; on_date date; w record; used int;
begin
  if not public.is_admin() then raise exception 'admin only'; end if;
  if p_credit is null or p_credit < 0 then raise exception 'credit must be zero or more'; end if;
  select * into b from public.bookings where id = p_booking for update;
  if not found then raise exception 'booking not found'; end if;
  if b.status <> 'pending' then raise exception 'booking is already %', b.status; end if;
  select * into m from public.memberships where client_id = b.client_id and status = 'active' order by created_at desc limit 1 for update;
  if not found then raise exception 'member has no active membership'; end if;
  on_date := coalesce(b.booking_date, current_date);

  if public.hhc_is_maintenance(b.service) then
    select * into w from public.hhc_window(m.package, m.created_at::date, 'maintenance', on_date);
    if not w.started then raise exception 'first quarterly maintenance is available from %', to_char(w.window_start, 'DD Mon YYYY'); end if;
    select count(*) into used from public.benefit_redemptions where membership_id = m.id and kind = 'maintenance' and period_start = w.window_start;
    if used >= w.allowed then raise exception 'maintenance service already used for % to %', to_char(w.window_start,'DD Mon'), to_char(w.window_end,'DD Mon YYYY'); end if;
    insert into public.benefit_redemptions(membership_id, client_id, booking_id, kind, period_start, period_end, service, created_by)
    values (m.id, m.client_id, b.id, 'maintenance', w.window_start, w.window_end, b.service, auth.email());
    if m.package <> 'essential' then update public.memberships set sessions_used = least(sessions_used + 1, sessions_total) where id = m.id; end if;
  end if;

  if p_use_complimentary then
    select * into w from public.hhc_window(m.package, m.created_at::date, 'complimentary', on_date);
    select count(*) into used from public.benefit_redemptions where membership_id = m.id and kind = 'complimentary' and period_start = w.window_start;
    if used >= w.allowed then raise exception 'no complimentary services left this membership year (resets %)', to_char(w.window_end + 1, 'DD Mon YYYY'); end if;
    insert into public.benefit_redemptions(membership_id, client_id, booking_id, kind, period_start, period_end, service, created_by)
    values (m.id, m.client_id, b.id, 'complimentary', w.window_start, w.window_end, b.service, auth.email());
  end if;

  if p_credit > 0 then
    if m.package <> 'elite' then raise exception 'only Elite members have styling credit'; end if;
    bal := public.credit_balance(m.id);
    if p_credit > bal then raise exception 'not enough credit (balance £%)', bal; end if;
    insert into public.credit_ledger(membership_id, client_id, kind, amount, booking_id, note, created_by)
    values (m.id, m.client_id, 'redeem', -p_credit, b.id, 'Redeemed on ' || b.service, auth.email());
    update public.memberships set style_credit = public.credit_balance(m.id) where id = m.id;
  end if;

  update public.bookings set status = 'confirmed', credit_applied = p_credit, approved_at = now() where id = b.id;
  return json_build_object('booking', b.id, 'credit_applied', p_credit, 'balance', public.credit_balance(m.id),
    'used_complimentary', p_use_complimentary, 'used_maintenance', public.hhc_is_maintenance(b.service));
end; $$;
revoke execute on function public.approve_booking(uuid, numeric, boolean) from public, anon;
grant execute on function public.approve_booking(uuid, numeric, boolean) to authenticated;

-- 6. Admin can log aftercare products handed over (a record only; no allowance is set or promised).
create or replace function public.record_aftercare(p_membership uuid, p_note text) returns void
language plpgsql security definer set search_path = public as $$
declare m public.memberships;
begin
  if not public.is_admin() then raise exception 'admin only'; end if;
  if p_note is null or length(trim(p_note)) = 0 then raise exception 'please describe what was given'; end if;
  select * into m from public.memberships where id = p_membership;
  if not found then raise exception 'membership not found'; end if;
  if m.package not in ('signature','elite') then raise exception 'aftercare products are included with Signature and Elite only'; end if;
  insert into public.benefit_redemptions(membership_id, client_id, kind, note, created_by)
  values (m.id, m.client_id, 'aftercare', trim(p_note), auth.email());
end; $$;
revoke execute on function public.record_aftercare(uuid, text) from public, anon;
grant execute on function public.record_aftercare(uuid, text) to authenticated;
alter function public.hhc_is_maintenance(text) set search_path = public;
