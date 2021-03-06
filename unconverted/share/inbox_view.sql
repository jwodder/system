-- \connect logs

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
