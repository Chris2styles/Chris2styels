-- Launch contacts: Christine's client list imported from Treatwell (9 Nov 2026) for the Healthy Hair Club launch messages.
-- Admin-only. Messages are sent from Christine's own phone (SMS / WhatsApp links); this table only tracks who has been messaged.
create table if not exists public.launch_contacts (
  id uuid primary key default gen_random_uuid(),
  name text,
  phone text not null unique,
  email text,
  opt_in boolean not null default false,
  bookings integer not null default 0,
  first_seen date,
  source text not null default 'treatwell',
  sms_sent_at timestamptz,
  wa_sent_at timestamptz,
  created_at timestamptz not null default now()
);
alter table public.launch_contacts enable row level security;
drop policy if exists admin_all_launch_contacts on public.launch_contacts;
create policy admin_all_launch_contacts on public.launch_contacts for all using (public.is_admin()) with check (public.is_admin());
create index if not exists launch_contacts_opt_in_idx on public.launch_contacts (opt_in, name);
