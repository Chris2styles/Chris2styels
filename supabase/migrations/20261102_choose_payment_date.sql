-- Members can choose their monthly payment date (1st-28th) at sign-up (Christine, 2 Nov 2026).
-- Until the first payment goes through the membership is 'pending': no booking, no benefits.
-- On the first payment the webhook sets status 'active', starts_on and created_at to that day, so the
-- membership year and benefit periods count from the payment date.
alter table public.memberships drop constraint if exists memberships_status_check;
alter table public.memberships add constraint memberships_status_check check (status in ('active','payment_failed','paused','cancelled','pending'));
alter table public.memberships add column if not exists starts_on date;
update public.memberships set starts_on = created_at::date where starts_on is null;
