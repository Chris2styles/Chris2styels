-- 24-hour appointment reminders (email always; text once Twilio is connected).
alter table public.bookings add column if not exists reminder_email_at timestamptz;
alter table public.bookings add column if not exists reminder_sms_at timestamptz;
alter table public.bookings add column if not exists reminder_sms_error text;
