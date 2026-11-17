CREATE OR REPLACE PROCEDURE add_phone(p_contact_name VARCHAR, p_phone VARCHAR, p_type VARCHAR)
LANGUAGE plpgsql AS $$
DECLARE contact_key BIGINT;
BEGIN
 IF p_type NOT IN ('home','work','mobile') THEN RAISE EXCEPTION 'type must be home, work, or mobile'; END IF;
 SELECT id INTO contact_key FROM contacts WHERE LOWER(first_name)=LOWER(BTRIM(p_contact_name)) ORDER BY id LIMIT 1;
 IF contact_key IS NULL THEN RAISE EXCEPTION 'contact not found'; END IF;
 INSERT INTO phones(contact_id,phone,type) VALUES(contact_key,BTRIM(p_phone),p_type);
END; $$;

CREATE OR REPLACE PROCEDURE move_to_group(p_contact_name VARCHAR, p_group_name VARCHAR)
LANGUAGE plpgsql AS $$
DECLARE group_key INTEGER;
BEGIN
 INSERT INTO contact_groups(name) VALUES(BTRIM(p_group_name)) ON CONFLICT(name) DO UPDATE SET name=EXCLUDED.name RETURNING id INTO group_key;
 UPDATE contacts SET group_id=group_key WHERE LOWER(first_name)=LOWER(BTRIM(p_contact_name));
 IF NOT FOUND THEN RAISE EXCEPTION 'contact not found'; END IF;
END; $$;

CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(id BIGINT, first_name VARCHAR, surname VARCHAR, email VARCHAR, birthday DATE, group_name VARCHAR, phones JSONB, created_at TIMESTAMPTZ)
LANGUAGE sql STABLE AS $$
 SELECT c.id,c.first_name,c.surname,c.email,c.birthday,g.name,
 COALESCE((SELECT JSONB_AGG(JSONB_BUILD_OBJECT('phone',p.phone,'type',p.type) ORDER BY p.id) FROM phones p WHERE p.contact_id=c.id),'[]'::jsonb),c.created_at
 FROM contacts c LEFT JOIN contact_groups g ON g.id=c.group_id
 WHERE c.first_name ILIKE '%'||COALESCE(p_query,'')||'%' OR COALESCE(c.surname,'') ILIKE '%'||COALESCE(p_query,'')||'%'
 OR COALESCE(c.email,'') ILIKE '%'||COALESCE(p_query,'')||'%' OR EXISTS(SELECT 1 FROM phones p WHERE p.contact_id=c.id AND p.phone ILIKE '%'||COALESCE(p_query,'')||'%')
 ORDER BY c.first_name,c.id;
$$;
