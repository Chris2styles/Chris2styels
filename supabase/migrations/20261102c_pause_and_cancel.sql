-- Pause and cancel (Christine, 2 Nov 2026).
--   * A member can pause for 1, 2 or 3 months, starting from their next payment date (they keep the month already paid for).
--   * At most 3 months of pause per membership year in total. One pause at a time.
--   * During a pause: no payments, no booking, no benefits. Payments restart automatically when the pause ends.
--   * A member can end a pause early from their dashboard: payment is taken that day and booking reopens.
--   * A member can cancel; it takes effect at the end of the month they've paid for.

create table if not exists public.membership_pauses (
  id uuid primary key default extensions.uuid_generate_v4(),
  membership_id uuid not null references public.memberships(id),
  client_id uuid not null references public.clients(id),
  starts_on date not null,
  ends_on date not null,             -- the day payments restart (exclusive end of the pause)
  months int not null check (months between 1 and 3),
  status text not null default 'scheduled' check (status in ('scheduled','active','ended','cancelled')),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  check (ends_on > starts_on)
);
create index if not exists membership_pauses_idx on public.membership_pauses(membership_id, starts_on);
alter table public.membership_pauses enable row level security;
drop policy if exists pauses_select_own_or_admin on public.membership_pauses;
create policy pauses_select_own_or_admin on public.membership_pauses for select
  using (public.is_admin() or client_id in (select id from public.clients where email = auth.email()));

alter table public.memberships add column if not exists cancel_at date;

-- Is the membership paused on this date?
create or replace function public.hhc_paused(p_membership uuid, p_on date) returns boolean
language sql stable security definer set search_path = public as $$
  select exists (select 1 from public.membership_pauses where membership_id = p_membership
                 and status in ('scheduled','active','ended') and starts_on <= p_on and p_on < ends_on)
$$;

-- Months of pause used (whole or part months count as a month) in the membership year containing p_on.
create or replace function public.hhc_pause_months_used(p_membership uuid, p_on date) returns int
language plpgsql stable security definer set search_path = public as $$
declare m public.memberships; w record; total int := 0; r record; a interval;
begin
  select * into m from public.memberships where id = p_membership;
  select * into w from public.hhc_window(m.package, m.created_at::date, 'complimentary', p_on);
  for r in select * from public.membership_pauses where membership_id = p_membership and status <> 'cancelled'
           and starts_on between w.window_start and w.window_end loop
    a := age(r.ends_on, r.starts_on);
    total := total + (date_part('year', a) * 12 + date_part('month', a))::int + case when date_part('day', a) > 0 then 1 else 0 end;
  end loop;
  return total;
end; $$;

revoke execute on function public.hhc_paused(uuid, date) from public, anon, authenticated;
revoke execute on function public.hhc_pause_months_used(uuid, date) from public, anon, authenticated;

-- Benefits summary now also reports pause and cancellation.
create or replace function public.membership_benefits(p_membership uuid, p_on date default current_date)
returns json language plpgsql stable security definer set search_path = public as $$
declare m public.memberships; c public.clients; mw record; cw record; mused int; cused int; next_top date; last_given date; pz public.membership_pauses; pused int;
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
  select * into pz from public.membership_pauses where membership_id = m.id and status in ('scheduled','active') and ends_on > p_on order by starts_on limit 1;
  pused := public.hhc_pause_months_used(m.id, p_on);
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
    'credit', case when m.package = 'elite' then public.credit_balance(m.id) else null end,
    'paused_now', public.hhc_paused(m.id, p_on),
    'pause', case when pz.id is null then null else json_build_object('id', pz.id, 'starts_on', pz.starts_on, 'ends_on', pz.ends_on, 'months', pz.months, 'started', pz.starts_on <= p_on) end,
    'pause_months_used', pused,
    'pause_months_left', greatest(3 - pused, 0),
    'cancel_at', m.cancel_at
  );
end; $$;
revoke execute on function public.membership_benefits(uuid, date) from public, anon;
grant execute on function public.membership_benefits(uuid, date) to authenticated, service_role;

-- No booking approvals or credit gifts while paused.
create or replace function public.hhc_assert_not_paused(p_membership uuid, p_on date) returns void
language plpgsql stable security definer set search_path = public as $$
declare pz public.membership_pauses;
begin
  select * into pz from public.membership_pauses where membership_id = p_membership and status in ('scheduled','active','ended')
    and starts_on <= p_on and p_on < ends_on limit 1;
  if found then raise exception 'membership is paused until %', to_char(pz.ends_on, 'DD Mon YYYY'); end if;
end; $$;
revoke execute on function public.hhc_assert_not_paused(uuid, date) from public, anon, authenticated;

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
  perform public.hhc_assert_not_paused(m.id, on_date);
  perform public.hhc_assert_not_paused(m.id, current_date);

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

create or replace function public.gift_credit(p_membership uuid, p_name text, p_under18 boolean, p_age int, p_phone text, p_email text, p_amount numeric) returns json
language plpgsql security definer set search_path = public as $$
declare m public.memberships; c public.clients; bal numeric; w record; gid uuid; ph text; em text;
begin
  select * into m from public.memberships where id = p_membership for update;
  if not found then raise exception 'membership not found'; end if;
  select * into c from public.clients where id = m.client_id;
  if auth.email() is null or lower(c.email) <> lower(auth.email()) then raise exception 'not allowed'; end if;
  if m.package <> 'elite' then raise exception 'credit gifting is an Elite benefit'; end if;
  if m.status <> 'active' then raise exception 'your membership needs to be active to gift credit'; end if;
  perform public.hhc_assert_not_paused(m.id, current_date);
  if p_name is null or length(trim(p_name)) = 0 then raise exception 'please enter the name of the person'; end if;
  if p_age is not null and (p_age < 0 or p_age > 120) then raise exception 'please enter a valid age'; end if;
  if p_age is not null and p_age >= 18 and coalesce(p_under18,false) then raise exception 'the age entered is 18 or over'; end if;
  ph := nullif(trim(coalesce(p_phone,'')), ''); em := nullif(trim(coalesce(p_email,'')), '');
  if not coalesce(p_under18,false) and ph is null then raise exception 'please enter a phone number for the person'; end if;
  if p_amount is null or p_amount <= 0 then raise exception 'enter an amount above £0'; end if;
  p_amount := round(p_amount, 2);
  bal := public.credit_balance(m.id);
  if p_amount > bal then raise exception 'you have £% available to gift', bal; end if;
  select * into w from public.hhc_window(m.package, m.created_at::date, 'maintenance', current_date);
  insert into public.credit_gifts(membership_id, from_client_id, recipient_name, recipient_contact, recipient_under18, recipient_age, recipient_phone, recipient_email, amount, expires_on)
  values (m.id, m.client_id, trim(p_name), coalesce(ph, em), coalesce(p_under18,false), p_age, ph, em, p_amount, w.window_end) returning id into gid;
  insert into public.credit_ledger(membership_id, client_id, kind, amount, note, created_by)
  values (m.id, m.client_id, 'gift', -p_amount, 'Gifted to ' || trim(p_name), auth.email());
  update public.memberships set style_credit = public.credit_balance(m.id) where id = m.id;
  return json_build_object('gift', gid, 'amount', p_amount, 'expires_on', w.window_end, 'balance', public.credit_balance(m.id));
end; $$;
revoke execute on function public.gift_credit(uuid, text, boolean, int, text, text, numeric) from public, anon;
grant execute on function public.gift_credit(uuid, text, boolean, int, text, text, numeric) to authenticated;
