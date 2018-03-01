update mogiminsk_user set telegram_context = telegram_context::jsonb || '{"bot": "tg"}'::jsonb;
update mogiminsk_user set viber_context = viber_context::jsonb || '{"bot": "viber"}'::jsonb;