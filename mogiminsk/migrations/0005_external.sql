ALTER TABLE public.mogiminsk_user ADD COLUMN external json;
ALTER TABLE public.mogiminsk_user ALTER COLUMN external SET DEFAULT '{}'::json;