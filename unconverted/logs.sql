\connect logs

-- <http://stackoverflow.com/a/6454469>
GRANT SELECT ON ALL TABLES IN SCHEMA public TO jwodder;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO jwodder;

CREATE TABLE apache_access (
    timestamp timestamp with time zone NOT NULL,
    host varchar(255) NOT NULL,
    port integer NOT NULL,
    src_addr inet NOT NULL,
    authuser varchar(255) NOT NULL,
    bytesIn integer NOT NULL,
    bytesOut integer NOT NULL,
    microsecs bigint NOT NULL,
    status integer NOT NULL,
    reqline varchar(2048) NOT NULL,
    method varchar(255) NOT NULL,
    path varchar(2048) NOT NULL,
    protocol varchar(255) NOT NULL,
    referer varchar(2048) NOT NULL,
    user_agent varchar(2048) NOT NULL
);

ALTER TABLE public.apache_access OWNER TO logger;

CREATE TABLE authfail (
    timestamp timestamp with time zone NOT NULL,
    username varchar(255) NOT NULL,
    src_addr inet NOT NULL
);

ALTER TABLE public.authfail OWNER TO logger;

CREATE TABLE inbox_contacts (
    id SERIAL PRIMARY KEY,
    realname varchar(2048) NOT NULL,
    email_address varchar(2048) NOT NULL,
    UNIQUE (realname, email_address)
);

CREATE TABLE inbox (
    id SERIAL PRIMARY KEY,
    timestamp timestamp with time zone NOT NULL,
    subject varchar(2048) NOT NULL,
    sender integer NOT NULL REFERENCES inbox_contacts(id),
    size integer NOT NULL,
    date timestamp with time zone NOT NULL
);

CREATE TABLE inbox_tocc (
    msg_id integer NOT NULL REFERENCES inbox(id),
    contact_id integer NOT NULL REFERENCES inbox_contacts(id),
    UNIQUE (msg_id, contact_id)
);

ALTER TABLE public.inbox_contacts OWNER TO logger;
ALTER TABLE public.inbox OWNER TO logger;
ALTER TABLE public.inbox_tocc OWNER TO logger;

CREATE OR REPLACE FUNCTION formataddr(realname VARCHAR, email_address VARCHAR)
                                     RETURNS VARCHAR
    AS $$
    SELECT CASE WHEN email_address IS NULL THEN NULL
                WHEN realname IS NULL OR realname = '' THEN email_address
                ELSE realname || ' <' || email_address || '>'
            END
    $$ LANGUAGE SQL IMMUTABLE CALLED ON NULL INPUT;

CREATE OR REPLACE VIEW inbox_view
    AS SELECT inbox.id, inbox.date, inbox.timestamp, inbox.subject,
              formataddr(sender.realname, sender.email_address) AS sender,
              (SELECT array_agg(formataddr(recip.realname, recip.email_address))
                      FROM inbox_tocc JOIN inbox_contacts AS recip
                           ON inbox_tocc.contact_id = recip.id
                      WHERE inbox.id = inbox_tocc.msg_id) AS recipients,
              inbox.size
    FROM inbox JOIN inbox_contacts AS sender ON inbox.sender = sender.id;
