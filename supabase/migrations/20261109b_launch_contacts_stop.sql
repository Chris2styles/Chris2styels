-- Clients who replied STOP (or asked not to be messaged): hidden from Launch Contacts and never included in group texts.
alter table public.launch_contacts add column if not exists do_not_contact boolean not null default false;
alter table public.launch_contacts add column if not exists stopped_at timestamptz;
