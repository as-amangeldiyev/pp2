-- Practice 8
ALTER TABLE contacts ADD COLUMN IF NOT EXISTS surname VARCHAR(100);

CREATE OR REPLACE FUNCTION find_contacts(p_pattern TEXT)
RETURNS TABLE (
    id BIGINT,
    first_name VARCHAR,
    surname VARCHAR,
    phone VARCHAR,
    created_at TIMESTAMPTZ
)
LANGUAGE sql
STABLE
AS $$
    SELECT c.id, c.first_name, c.surname, c.phone, c.created_at
    FROM contacts AS c
    WHERE c.first_name ILIKE '%' || COALESCE(p_pattern, '') || '%'
       OR COALESCE(c.surname, '') ILIKE '%' || COALESCE(p_pattern, '') || '%'
       OR c.phone ILIKE '%' || COALESCE(p_pattern, '') || '%'
    ORDER BY c.first_name, c.surname NULLS FIRST, c.id;
$$;

CREATE OR REPLACE FUNCTION get_contacts_page(p_limit INTEGER, p_offset INTEGER)
RETURNS TABLE (
    id BIGINT,
    first_name VARCHAR,
    surname VARCHAR,
    phone VARCHAR,
    created_at TIMESTAMPTZ
)
LANGUAGE plpgsql
STABLE
AS $$
BEGIN
    IF p_limit IS NULL OR p_limit < 1 OR p_limit > 500 THEN
        RAISE EXCEPTION 'limit must be between 1 and 500';
    END IF;
    IF p_offset IS NULL OR p_offset < 0 THEN
        RAISE EXCEPTION 'offset must be zero or greater';
    END IF;

    RETURN QUERY
    SELECT c.id, c.first_name, c.surname, c.phone, c.created_at
    FROM contacts AS c
    ORDER BY c.first_name, c.surname NULLS FIRST, c.id
    LIMIT p_limit OFFSET p_offset;
END;
$$;
