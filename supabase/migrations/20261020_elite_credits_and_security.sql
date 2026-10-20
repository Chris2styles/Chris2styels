-- Elite styling credit, booking safety and security fixes.
-- Tested on the practice database "Chris 2 styles - TEST" on 20 Oct 2026.
-- NOT YET APPLIED TO LIVE. Apply only after Christine's final approval, then deploy the matching code.

-- 1. Close open write policies (server uses the secret key, which bypasses RLS)
drop policy if exists service_update_membership on public.memberships;
drop policy if exists service_insert_membership on public.memberships;
drop policy if exists service_insert_clients on public.clients;
drop policy if exists service_insert_slots on public.slots;
drop policy if exists service_all_events on public.processed_events;
drop policy if exists client_insert_booking on public.bookings;
create policy admin_update_memberships on public.memberships for update using (public.is_admin()) with check (public.is_admin());
create policy admin_select_payments on public.payments for select using (public.is_admin() or client_id in (select id from public.clients where email = auth.email()));
create policy admin_select_events on public.processed_events for select using (public.is_admin());

-- 2. Payments: one row per Stripe invoice
create unique index if not exists payments_stripe_payment_id_key on public.payments(stripe_payment_id);

-- 3. Bookings: link to slot, block double-booking of a slot
alter table public.bookings add column if not exists booking_date date, add column if not exists booking_time time, add column if not exists addons text[] default '{}', add column if not exists credit_applied numeric not null default 0, add column if not exists approved_at timestamptz;
create unique index if not exists bookings_one_active_per_slot on public.bookings(slot_id) where slot_id is not null and status in ('pending','confirmed');

-- 4. Credit ledger
create table if not exists public.credit_ledger (
  id uuid primary key default extensions.uuid_generate_v4(),
  membership_id uuid not null references public.memberships(id),
  client_id uuid not null references public.clients(id),
  kind text not null check (kind in ('issue','redeem','adjustment')),
  amount numeric(10,2) not null check (amount <> 0),
  stripe_invoice_id text,
  booking_id uuid references public.bookings(id),
  note text,
  created_by text,
  created_at timestamptz not null default now(),
  check ((kind = 'issue' and amount > 0 and stripe_invoice_id is not null) or kind <> 'issue'),
  check ((kind = 'redeem' and amount < 0 and booking_id is not null) or kind <> 'redeem')
);
create unique index if not exists credit_one_issue_per_invoice on public.credit_ledger(stripe_invoice_id) where kind = 'issue';
create unique index if not exists credit_one_redeem_per_booking on public.credit_ledger(booking_id) where kind = 'redeem';
create index if not exists credit_ledger_membership_idx on public.credit_ledger(membership_id, created_at desc);
alter table public.credit_ledger enable row level security;
create policy credit_select_own_or_admin on public.credit_ledger for select using (public.is_admin() or client_id in (select id from public.clients where email = auth.email()));

create or replace function public.credit_balance(p_membership uuid) returns numeric language sql stable security definer set search_path = public as $$
  select coalesce(sum(amount),0)::numeric(10,2) from public.credit_ledger where membership_id = p_membership;
$$;

create or replace function public.issue_elite_credit(p_membership uuid, p_invoice text, p_amount numeric) returns numeric language plpgsql security definer set search_path = public as $$
declare m public.memberships;
begin
  select * into m from public.memberships where id = p_membership for update;
  if not found then raise exception 'membership not found'; end if;
  if m.package <> 'elite' then return public.credit_balance(p_membership); end if;
  insert into public.credit_ledger(membership_id, client_id, kind, amount, stripe_invoice_id, note, created_by)
  values (m.id, m.client_id, 'issue', p_amount, p_invoice, 'Monthly Elite styling credit', 'stripe')
  on conflict (stripe_invoice_id) where kind = 'issue' do nothing;
  update public.memberships set style_credit = public.credit_balance(m.id) where id = m.id;
  return public.credit_balance(m.id);
end; $$;
revoke execute on function public.issue_elite_credit(uuid,text,numeric) from public, anon, authenticated;

create or replace function public.approve_booking(p_booking uuid, p_credit numeric default 0) returns json language plpgsql security definer set search_path = public as $$
declare b public.bookings; m public.memberships; bal numeric; included boolean;
begin
  if not public.is_admin() then raise exception 'admin only'; end if;
  if p_credit is null or p_credit < 0 then raise exception 'credit must be zero or more'; end if;
  select * into b from public.bookings where id = p_booking for update;
  if not found then raise exception 'booking not found'; end if;
  if b.status <> 'pending' then raise exception 'booking is already %', b.status; end if;
  select * into m from public.memberships where client_id = b.client_id and status = 'active' order by created_at desc limit 1 for update;
  if not found then raise exception 'member has no active membership'; end if;
  included := b.service in ('Monthly Maintenance');
  if included and m.package <> 'essential' then
    if m.sessions_used >= m.sessions_total then raise exception 'included monthly appointment already used this month'; end if;
    update public.memberships set sessions_used = sessions_used + 1 where id = m.id;
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
  return json_build_object('booking', b.id, 'credit_applied', p_credit, 'balance', public.credit_balance(m.id));
end; $$;
revoke execute on function public.approve_booking(uuid,numeric) from public, anon;
grant execute on function public.approve_booking(uuid,numeric) to authenticated;

create or replace function public.decline_booking(p_booking uuid) returns void language plpgsql security definer set search_path = public as $$
declare b public.bookings;
begin
  if not public.is_admin() then raise exception 'admin only'; end if;
  select * into b from public.bookings where id = p_booking for update;
  if not found then raise exception 'booking not found'; end if;
  if b.status <> 'pending' then raise exception 'booking is already %', b.status; end if;
  update public.bookings set status = 'cancelled' where id = b.id;
  if b.slot_id is not null then update public.slots set booked = false where id = b.slot_id; end if;
end; $$;
revoke execute on function public.decline_booking(uuid) from public, anon;
grant execute on function public.decline_booking(uuid) to authenticated;

create or replace function public.adjust_credit(p_membership uuid, p_amount numeric, p_note text) returns numeric language plpgsql security definer set search_path = public as $$
declare m public.memberships;
begin
  if not public.is_admin() then raise exception 'admin only'; end if;
  if p_note is null or length(trim(p_note)) = 0 then raise exception 'a reason is required'; end if;
  select * into m from public.memberships where id = p_membership for update;
  if not found then raise exception 'membership not found'; end if;
  if public.credit_balance(m.id) + p_amount < 0 then raise exception 'balance cannot go below zero'; end if;
  insert into public.credit_ledger(membership_id, client_id, kind, amount, note, created_by) values (m.id, m.client_id, 'adjustment', p_amount, p_note, auth.email());
  update public.memberships set style_credit = public.credit_balance(m.id) where id = m.id;
  return public.credit_balance(m.id);
end; $$;
revoke execute on function public.adjust_credit(uuid,numeric,text) from public, anon;
grant execute on function public.adjust_credit(uuid,numeric,text) to authenticated;

create or replace function public.create_booking(p_client uuid, p_slot uuid, p_service text, p_addons text[], p_notes text) returns uuid language plpgsql security definer set search_path = public as $$
declare s public.slots; bid uuid;
begin
  update public.slots set booked = true where id = p_slot and booked = false and coalesce(is_blocked,false) = false returning * into s;
  if not found then raise exception 'slot no longer available'; end if;
  insert into public.bookings(client_id, slot_id, stylist_id, service, status, notes, booking_date, booking_time, addons)
  values (p_client, s.id, s.stylist_id, p_service, 'pending', p_notes, s.slot_date, s.slot_time, coalesce(p_addons,'{}'))
  returning id into bid;
  return bid;
end; $$;
revoke execute on function public.create_booking(uuid,uuid,text,text[],text) from public, anon, authenticated;
revoke execute on function public.credit_balance(uuid) from public, anon, authenticated;

-- 5. Carry over any Elite credit given by the old code (Elite is on sale while this is prepared).
insert into public.credit_ledger(membership_id, client_id, kind, amount, note, created_by)
select id, client_id, 'adjustment', style_credit, 'Opening balance carried over', 'migration'
from public.memberships where package = 'elite' and coalesce(style_credit,0) > 0
and not exists (select 1 from public.credit_ledger l where l.membership_id = memberships.id);
