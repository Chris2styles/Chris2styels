-- Healthy Hair Club rules confirmed by Christine on 28 Oct 2026 (second batch):
--   * A complimentary service = ONE add-on of the client's choice free on that visit (Essential 1/yr, Signature & Elite 2/yr).
--   * Aftercare (Signature & Elite): the stylist decides top-ups from how long each product lasts; admin records the
--     product and next top-up date. Admin-only; clients just see "Complimentary Aftercare Products Provided".
--   * Elite members can gift styling credit to anyone (family, friends, non-clients), in the app. A gift expires at the
--     end of the member's current month, the same day the member's own credit would expire.
--   * Package upgrades/downgrades take effect at the next payment date (handled by the Stripe webhook).

-- 1. Complimentary add-on: the client's request on the booking, and the add-on actually made free.
alter table public.bookings add column if not exists complimentary_addon text;

drop function if exists public.approve_booking(uuid, numeric, boolean);
create or replace function public.approve_booking(p_booking uuid, p_credit numeric default 0, p_use_complimentary boolean default false, p_complimentary_addon text default null)
returns json language plpgsql security definer set search_path = public as $$
declare b public.bookings; m public.memberships; bal numeric; on_date date; w record; used int; free_addon text;
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
    free_addon := nullif(trim(coalesce(p_complimentary_addon, b.complimentary_addon, '')), '');
    if free_addon is null then raise exception 'choose which add-on is complimentary'; end if;
    if not (free_addon = any(coalesce(b.addons, '{}'))) then raise exception 'the complimentary add-on must be one of the add-ons on this booking'; end if;
    select * into w from public.hhc_window(m.package, m.created_at::date, 'complimentary', on_date);
    select count(*) into used from public.benefit_redemptions where membership_id = m.id and kind = 'complimentary' and period_start = w.window_start;
    if used >= w.allowed then raise exception 'no complimentary add-ons left this membership year (resets %)', to_char(w.window_end + 1, 'DD Mon YYYY'); end if;
    insert into public.benefit_redemptions(membership_id, client_id, booking_id, kind, period_start, period_end, service, created_by)
    values (m.id, m.client_id, b.id, 'complimentary', w.window_start, w.window_end, free_addon, auth.email());
    update public.bookings set complimentary_addon = free_addon where id = b.id;
  else
    update public.bookings set complimentary_addon = null where id = b.id;
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
    'used_complimentary', p_use_complimentary, 'complimentary_addon', case when p_use_complimentary then free_addon end,
    'used_maintenance', public.hhc_is_maintenance(b.service));
end; $$;
revoke execute on function public.approve_booking(uuid, numeric, boolean, text) from public, anon;
grant execute on function public.approve_booking(uuid, numeric, boolean, text) to authenticated;

-- 2. Aftercare log: product given and when the stylist expects the next top-up.
alter table public.benefit_redemptions add column if not exists next_due date;
drop function if exists public.record_aftercare(uuid, text);
create or replace function public.record_aftercare(p_membership uuid, p_note text, p_next_due date default null) returns void
language plpgsql security definer set search_path = public as $$
declare m public.memberships;
begin
  if not public.is_admin() then raise exception 'admin only'; end if;
  if p_note is null or length(trim(p_note)) = 0 then raise exception 'please enter the product given'; end if;
  select * into m from public.memberships where id = p_membership;
  if not found then raise exception 'membership not found'; end if;
  if m.package not in ('signature','elite') then raise exception 'aftercare products are included with Signature and Elite only'; end if;
  insert into public.benefit_redemptions(membership_id, client_id, kind, note, next_due, created_by)
  values (m.id, m.client_id, 'aftercare', trim(p_note), p_next_due, auth.email());
end; $$;
revoke execute on function public.record_aftercare(uuid, text, date) from public, anon;
grant execute on function public.record_aftercare(uuid, text, date) to authenticated;
-- Clients do not see aftercare records (admin only, as requested).
drop policy if exists benefit_select_own_or_admin on public.benefit_redemptions;
create policy benefit_select_own_or_admin on public.benefit_redemptions for select
  using (public.is_admin() or (kind <> 'aftercare' and client_id in (select id from public.clients where email = auth.email())));

-- 3. Elite credit gifts.
alter table public.credit_ledger drop constraint if exists credit_ledger_kind_check;
alter table public.credit_ledger add constraint credit_ledger_kind_check check (kind in ('issue','redeem','adjustment','expiry','gift'));

create table if not exists public.credit_gifts (
  id uuid primary key default extensions.uuid_generate_v4(),
  membership_id uuid not null references public.memberships(id),
  from_client_id uuid not null references public.clients(id),
  recipient_name text not null,
  recipient_contact text not null,
  amount numeric(10,2) not null check (amount > 0),
  used_amount numeric(10,2) not null default 0 check (used_amount >= 0),
  expires_on date not null,
  status text not null default 'active' check (status in ('active','used','cancelled')),
  note text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  check (used_amount <= amount)
);
create index if not exists credit_gifts_membership_idx on public.credit_gifts(membership_id, created_at desc);
alter table public.credit_gifts enable row level security;
drop policy if exists gifts_select_own_or_admin on public.credit_gifts;
create policy gifts_select_own_or_admin on public.credit_gifts for select
  using (public.is_admin() or from_client_id in (select id from public.clients where email = auth.email()));

create table if not exists public.credit_gift_redemptions (
  id uuid primary key default extensions.uuid_generate_v4(),
  gift_id uuid not null references public.credit_gifts(id),
  amount numeric(10,2) not null check (amount > 0),
  note text,
  created_by text,
  created_at timestamptz not null default now()
);
alter table public.credit_gift_redemptions enable row level security;
drop policy if exists gift_redemptions_admin on public.credit_gift_redemptions;
create policy gift_redemptions_admin on public.credit_gift_redemptions for select using (public.is_admin());

-- Member gives credit. Only the member themself, only Elite, only an active membership, only up to their balance.
create or replace function public.gift_credit(p_membership uuid, p_name text, p_contact text, p_amount numeric) returns json
language plpgsql security definer set search_path = public as $$
declare m public.memberships; c public.clients; bal numeric; w record; gid uuid;
begin
  select * into m from public.memberships where id = p_membership for update;
  if not found then raise exception 'membership not found'; end if;
  select * into c from public.clients where id = m.client_id;
  if auth.email() is null or lower(c.email) <> lower(auth.email()) then raise exception 'not allowed'; end if;
  if m.package <> 'elite' then raise exception 'credit gifting is an Elite benefit'; end if;
  if m.status <> 'active' then raise exception 'your membership needs to be active to gift credit'; end if;
  if p_name is null or length(trim(p_name)) = 0 or p_contact is null or length(trim(p_contact)) = 0 then
    raise exception 'please enter the name and a phone number or email for the person'; end if;
  if p_amount is null or p_amount <= 0 then raise exception 'enter an amount above £0'; end if;
  p_amount := round(p_amount, 2);
  bal := public.credit_balance(m.id);
  if p_amount > bal then raise exception 'you have £% available to gift', bal; end if;
  select * into w from public.hhc_window(m.package, m.created_at::date, 'maintenance', current_date);
  insert into public.credit_gifts(membership_id, from_client_id, recipient_name, recipient_contact, amount, expires_on)
  values (m.id, m.client_id, trim(p_name), trim(p_contact), p_amount, w.window_end) returning id into gid;
  insert into public.credit_ledger(membership_id, client_id, kind, amount, note, created_by)
  values (m.id, m.client_id, 'gift', -p_amount, 'Gifted to ' || trim(p_name), auth.email());
  update public.memberships set style_credit = public.credit_balance(m.id) where id = m.id;
  return json_build_object('gift', gid, 'amount', p_amount, 'expires_on', w.window_end, 'balance', public.credit_balance(m.id));
end; $$;
revoke execute on function public.gift_credit(uuid, text, text, numeric) from public, anon;
grant execute on function public.gift_credit(uuid, text, text, numeric) to authenticated;

-- Salon uses a gift when the person visits (part or all of it).
create or replace function public.redeem_gift(p_gift uuid, p_amount numeric, p_note text default null) returns json
language plpgsql security definer set search_path = public as $$
declare g public.credit_gifts; left_amt numeric;
begin
  if not public.is_admin() then raise exception 'admin only'; end if;
  select * into g from public.credit_gifts where id = p_gift for update;
  if not found then raise exception 'gift not found'; end if;
  if g.status <> 'active' then raise exception 'this gift is already %', g.status; end if;
  if current_date > g.expires_on then raise exception 'this gift expired on %', to_char(g.expires_on, 'DD Mon YYYY'); end if;
  left_amt := g.amount - g.used_amount;
  if p_amount is null or p_amount <= 0 then raise exception 'enter an amount above £0'; end if;
  if p_amount > left_amt then raise exception 'only £% left on this gift', left_amt; end if;
  insert into public.credit_gift_redemptions(gift_id, amount, note, created_by) values (g.id, p_amount, p_note, auth.email());
  update public.credit_gifts set used_amount = used_amount + p_amount,
    status = case when used_amount + p_amount >= amount then 'used' else 'active' end, updated_at = now() where id = g.id;
  return json_build_object('gift', g.id, 'left', left_amt - p_amount);
end; $$;
revoke execute on function public.redeem_gift(uuid, numeric, text) from public, anon;
grant execute on function public.redeem_gift(uuid, numeric, text) to authenticated;

-- Salon cancels a gift made by mistake; the unused part goes back to the member if it hasn't expired.
create or replace function public.cancel_gift(p_gift uuid) returns json
language plpgsql security definer set search_path = public as $$
declare g public.credit_gifts; back numeric := 0;
begin
  if not public.is_admin() then raise exception 'admin only'; end if;
  select * into g from public.credit_gifts where id = p_gift for update;
  if not found then raise exception 'gift not found'; end if;
  if g.status <> 'active' then raise exception 'this gift is already %', g.status; end if;
  if current_date <= g.expires_on then
    back := g.amount - g.used_amount;
    if back > 0 then
      insert into public.credit_ledger(membership_id, client_id, kind, amount, note, created_by)
      values (g.membership_id, g.from_client_id, 'adjustment', back, 'Gift to ' || g.recipient_name || ' cancelled', auth.email());
      update public.memberships set style_credit = public.credit_balance(g.membership_id) where id = g.membership_id;
    end if;
  end if;
  update public.credit_gifts set status = 'cancelled', updated_at = now() where id = g.id;
  return json_build_object('gift', g.id, 'returned', back);
end; $$;
revoke execute on function public.cancel_gift(uuid) from public, anon;
grant execute on function public.cancel_gift(uuid) to authenticated;

-- 4. Package changes at the next payment date: the webhook calls this when Stripe switches the price.
create or replace function public.change_package(p_sub text, p_package text) returns void
language plpgsql security definer set search_path = public as $$
begin
  if p_package not in ('essential','signature','elite') then raise exception 'unknown package %', p_package; end if;
  update public.memberships set package = p_package,
    sessions_total = case when p_package = 'essential' then 0 else 1 end,
    sessions_used = least(sessions_used, case when p_package = 'essential' then 0 else 1 end)
  where stripe_sub_id = p_sub and package <> p_package;
end; $$;
revoke execute on function public.change_package(text, text) from public, anon, authenticated;

-- 5. Signature/Elite clients see their next aftercare top-up date (no product names; Christine 28 Oct).
create or replace function public.membership_benefits(p_membership uuid, p_on date default current_date)
returns json language plpgsql stable security definer set search_path = public as $$
declare m public.memberships; c public.clients; mw record; cw record; mused int; cused int; next_top date; last_given date;
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
  select min(next_due) into next_top from public.benefit_redemptions where membership_id = m.id and kind = 'aftercare' and next_due >= p_on;
  select max(created_at)::date into last_given from public.benefit_redemptions where membership_id = m.id and kind = 'aftercare';
  return json_build_object(
    'package', m.package, 'status', m.status, 'member_since', m.created_at::date,
    'maintenance', json_build_object('cadence', case when m.package = 'essential' then 'quarterly' else 'monthly' end,
      'window_start', mw.window_start, 'window_end', mw.window_end, 'started', mw.started,
      'allowed', mw.allowed, 'used', mused, 'remaining', case when mw.started then greatest(mw.allowed - mused, 0) else 0 end),
    'complimentary', json_build_object('window_start', cw.window_start, 'window_end', cw.window_end,
      'allowed', cw.allowed, 'used', cused, 'remaining', greatest(cw.allowed - cused, 0)),
    'aftercare', m.package in ('signature','elite'),
    'aftercare_next_due', case when m.package in ('signature','elite') then next_top end,
    'aftercare_last_given', case when m.package in ('signature','elite') then last_given end,
    'credit', case when m.package = 'elite' then public.credit_balance(m.id) else null end
  );
end; $$;
