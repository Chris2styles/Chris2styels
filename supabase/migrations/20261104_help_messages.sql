-- Help messages from members go to the admin Messages tab, with an email to the salon (Christine, 4 Nov 2026).
-- Members can leave a phone number for a call back within 24 hours.
alter table public.messages add column if not exists phone text;
alter table public.messages add column if not exists client_email text;
alter table public.messages add column if not exists called_back_at timestamptz;
alter table public.messages add column if not exists replied_at timestamptz;
alter table public.messages alter column created_at set default now();
alter table public.messages alter column read set default false;
-- Messages are now saved by the server (which checks who the member is), so the open insert rule is removed.
drop policy if exists client_insert_message on public.messages;
