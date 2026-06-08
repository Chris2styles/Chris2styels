-- ============================================================
-- CHRIS 2 STYLES SALON — HEALTHY HAIR CLUB
-- Supabase Database Schema (Simple Version)
-- ============================================================

-- ── EXTENSIONS ───────────────────────────────────────────────
create extension if not exists "uuid-ossp";

-- ── 1. CLIENTS ───────────────────────────────────────────────
create table public.clients (
  id            uuid primary key default uuid_generate_v4(),
  full_name     text not null,
  email         text not null unique,
  phone         text,
  auth_id       uuid,
  created_at    timestamptz default now(),
  updated_at    timestamptz default now()
);

-- ── 2. MEMBERSHIPS ───────────────────────────────────────────
create table public.memberships (
  id                   uuid primary key default uuid_generate_v4(),
  client_id            uuid not null references public.clients(id) on delete cascade,
  package              text not null check (package in ('essential','signature','elite')),
  status               text not null default 'active'
                         check (status in ('active','payment_failed','paused','cancelled')),
  stripe_customer_id   text,
  stripe_sub_id        text,
  current_period_start timestamptz,
  current_period_end   timestamptz,
  sessions_used        int not null default 0,
  sessions_total       int not null default 0,
  style_credit         numeric(6,2) default 0,
  created_at           timestamptz default now(),
  updated_at           timestamptz default now()
);

-- ── 3. STYLISTS ──────────────────────────────────────────────
create table public.stylists (
  id         uuid primary key default uuid_generate_v4(),
  name       text not null,
  color      text default '#C9A84C',
  active     boolean default true,
  created_at timestamptz default now()
);

-- Seed Christine as the default stylist
insert into public.stylists (name, color) values ('Christine', '#C9A84C');

-- ── 4. AVAILABILITY SLOTS ────────────────────────────────────
create table public.slots (
  id            uuid primary key default uuid_generate_v4(),
  stylist_id    uuid references public.stylists(id) on delete cascade,
  slot_date     date not null,
  slot_time     time not null,
  duration_mins int not null default 60,
  members_only  boolean default true,
  is_blocked    boolean default false,
  booked        boolean default false,
  created_at    timestamptz default now()
);

-- ── 5. BOOKINGS ──────────────────────────────────────────────
create table public.bookings (
  id          uuid primary key default uuid_generate_v4(),
  client_id   uuid not null references public.clients(id) on delete cascade,
  slot_id     uuid references public.slots(id) on delete set null,
  stylist_id  uuid references public.stylists(id) on delete set null,
  service     text not null,  status      text not null default 'pending'

                check (status in ('pending','confirmed','cancelled','completed')),
  notes       text,
  created_at  timestamptz default now(),
  updated_at  timestamptz default now()
);

-- ── 6. BOOKING ADD-ONS ───────────────────────────────────────
create table public.booking_addons (
  id          uuid primary key default uuid_generate_v4(),
  booking_id  uuid not null references public.bookings(id) on delete cascade,
  addon_name  text not null,
  full_price  numeric(6,2) not null,
  disc_price  numeric(6,2) not null
);

-- ── 7. ADD-ON SERVICES CATALOG ───────────────────────────────
create table public.addon_services (
  id         uuid primary key default uuid_generate_v4(),
  category   text not null,
  name       text not null,
  price      numeric(6,2) not null,
  active     boolean default true,
  created_at timestamptz default now()
);

-- ── 8. VISIT HISTORY ─────────────────────────────────────────
create table public.visits (
  id          uuid primary key default uuid_generate_v4(),
  client_id   uuid not null references public.clients(id) on delete cascade,
  booking_id  uuid references public.bookings(id) on delete set null,
  visit_date  date not null,
  service     text not null,
  stylist_id  uuid references public.stylists(id) on delete set null,
  notes       text,
  created_at  timestamptz default now()
);

-- ── 9. VISIT TREATMENTS ──────────────────────────────────────
create table public.visit_treatments (
  id        uuid primary key default uuid_generate_v4(),
  visit_id  uuid not null references public.visits(id) on delete cascade,
  treatment text not null
);

-- ── 10. CLIENT NOTES ─────────────────────────────────────────
create table public.client_notes (
  id         uuid primary key default uuid_generate_v4(),
  client_id  uuid not null references public.clients(id) on delete cascade unique,
  notes      text,
  updated_at timestamptz default now()
);

-- ── 11. BLOCKED DATES ────────────────────────────────────────
create table public.blocked_dates (
  id         uuid primary key default uuid_generate_v4(),
  block_date date not null,
  reason     text,
  created_at timestamptz default now()
);

-- ── 12. PAYMENTS LOG ─────────────────────────────────────────
create table public.payments (
  id                uuid primary key default uuid_generate_v4(),
  client_id         uuid not null references public.clients(id) on delete cascade,
  membership_id     uuid references public.memberships(id) on delete set null,
  stripe_payment_id text,
  amount            numeric(8,2) not null,
  currency          text default 'gbp',
  status            text not null check (status in ('paid','failed','refunded','pending')),
  created_at        timestamptz default now()
);

-- ── 13. MESSAGES / INBOX ─────────────────────────────────────
create table public.messages (
  id          uuid primary key default uuid_generate_v4(),
  client_id   uuid references public.clients(id) on delete set null,
  client_name text,
  type        text not null check (type in ('message','callback','consultation','stylist_question')),
  body        text not null,
  read        boolean default false,
  reply       text,
  created_at  timestamptz default now()
);

-- ── INDEXES for performance ───────────────────────────────────
create index on public.memberships (client_id);
create index on public.memberships (status);
create index on public.bookings    (client_id);
create index on public.bookings    (status);
create index on public.visits      (client_id);
create index on public.slots       (slot_date, slot_time);
create index on public.payments    (client_id);
create index on public.messages    (read);

-- ── AUTO UPDATED_AT TRIGGER ───────────────────────────────────
create or replace function public.handle_updated_at()
returns trigger language plpgsql as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

create trigger set_updated_at before update on public.clients
  for each row execute function public.handle_updated_at();

create trigger set_updated_at before update on public.memberships
  for each row execute function public.handle_updated_at();

create trigger set_updated_at before update on public.bookings
  for each row execute function public.handle_updated_at();





mv app/HHCAPP.jsx app/HHCApp.jsx
