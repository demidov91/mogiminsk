alter table public.mogiminsk_user add column viber_context json;
alter table public.mogiminsk_user add column  viber_id integer;
alter table public.mogiminsk_user add column  viber_state character varying(31);
alter table public.mogiminsk_user add column  viber_messages character varying(1023);

alter table public.mogiminsk_user alter column  telegram_id drop not NULL;
alter table public.mogiminsk_user alter column  telegram_messages drop not NULL;