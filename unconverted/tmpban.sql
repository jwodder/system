CREATE USER tmpban WITH NOSUPERUSER CREATEDB CREATEROLE
                        ENCRYPTED PASSWORD '---REDACTED---';

CREATE DATABASE tmpban WITH OWNER tmpban ENCODING 'utf8';

\connect tmpban

GRANT SELECT ON ALL TABLES IN SCHEMA public TO jwodder;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO jwodder;

CREATE TABLE bans (
    ip_addr inet PRIMARY KEY,
    ban_start timestamp with time zone NOT NULL,
    ban_end timestamp with time zone NOT NULL,
    reason varchar(255)
);

ALTER TABLE public.bans OWNER TO tmpban;
