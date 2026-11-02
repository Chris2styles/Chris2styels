-- Members change their own package from the dashboard (Christine, 2 Nov 2026).
-- The change is scheduled in Stripe for the next payment date; these columns show it until then.
alter table public.memberships add column if not exists pending_package text check (pending_package in ('essential','signature','elite'));
alter table public.memberships add column if not exists pending_package_from date;

-- When Stripe switches the price, the package changes and the pending change is cleared.
create or replace function public.change_package(p_sub text, p_package text) returns void
language plpgsql security definer set search_path = public as $$
begin
  if p_package not in ('essential','signature','elite') then raise exception 'unknown package %', p_package; end if;
  update public.memberships set package = p_package,
    sessions_total = case when p_package = 'essential' then 0 else 1 end,
    sessions_used = least(sessions_used, case when p_package = 'essential' then 0 else 1 end)
  where stripe_sub_id = p_sub and package <> p_package;
  update public.memberships set pending_package = null, pending_package_from = null
  where stripe_sub_id = p_sub and pending_package = p_package;
end; $$;
revoke execute on function public.change_package(text, text) from public, anon, authenticated;
