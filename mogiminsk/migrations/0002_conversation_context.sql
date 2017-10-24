ALTER TABLE mogiminsk_conversation add column messenger varchar(31) NOT NULL default 'telegram';
ALTER TABLE mogiminsk_conversation add column context json default '{}'::json;