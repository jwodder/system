\connect logs

-- <http://stackoverflow.com/a/6454469>
GRANT SELECT ON ALL TABLES IN SCHEMA public TO jwodder;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO jwodder;

-- CREATE TABLE apache_access  -- converted to Python

ALTER TABLE public.apache_access OWNER TO logger;

-- CREATE TABLE authfail  -- converted to Python

ALTER TABLE public.authfail OWNER TO logger;

-- CREATE TABLE inbox_contacts  -- converted to Python

-- CREATE TABLE inbox  -- converted to Python

-- CREATE TABLE inbox_tocc  -- converted to Python

ALTER TABLE public.inbox_contacts OWNER TO logger;
ALTER TABLE public.inbox OWNER TO logger;
ALTER TABLE public.inbox_tocc OWNER TO logger;
