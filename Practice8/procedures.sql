CREATE OR REPLACE PROCEDURE upsert_contact(
    p_first_name VARCHAR,
    p_phone VARCHAR,
    p_surname VARCHAR DEFAULT NULL
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF NULLIF(BTRIM(p_first_name), '') IS NULL THEN
        RAISE EXCEPTION 'name cannot be blank';
    END IF;
    IF NULLIF(BTRIM(p_phone), '') IS NULL THEN
        RAISE EXCEPTION 'phone cannot be blank';
    END IF;

    -- A contact is considered existing when its full name matches.
    IF EXISTS (
        SELECT 1 FROM contacts c
        WHERE LOWER(c.first_name) = LOWER(BTRIM(p_first_name))
          AND LOWER(COALESCE(c.surname, '')) = LOWER(COALESCE(NULLIF(BTRIM(p_surname), ''), ''))
    ) THEN
        UPDATE contacts c
        SET phone = BTRIM(p_phone)
        WHERE LOWER(c.first_name) = LOWER(BTRIM(p_first_name))
          AND LOWER(COALESCE(c.surname, '')) = LOWER(COALESCE(NULLIF(BTRIM(p_surname), ''), ''));
    ELSE
        INSERT INTO contacts (first_name, surname, phone)
        VALUES (BTRIM(p_first_name), NULLIF(BTRIM(p_surname), ''), BTRIM(p_phone));
    END IF;
END;
$$;

-- Pass parallel arrays. Invalid rows are collected in p_invalid_data as JSONB;
-- valid rows are inserted or updated. Phone format: optional + and 7-15 digits.
CREATE OR REPLACE PROCEDURE upsert_contacts_batch(
    IN p_names TEXT[],
    IN p_phones TEXT[],
    INOUT p_invalid_data JSONB DEFAULT '[]'::JSONB
)
LANGUAGE plpgsql
AS $$
DECLARE
    i INTEGER;
    clean_name TEXT;
    clean_phone TEXT;
BEGIN
    p_invalid_data := '[]'::JSONB;
    IF p_names IS NULL OR p_phones IS NULL OR CARDINALITY(p_names) <> CARDINALITY(p_phones) THEN
        RAISE EXCEPTION 'names and phones must be non-null arrays of equal length';
    END IF;

    FOR i IN 1..COALESCE(CARDINALITY(p_names), 0) LOOP
        clean_name := BTRIM(p_names[i]);
        clean_phone := BTRIM(p_phones[i]);

        IF NULLIF(clean_name, '') IS NULL OR clean_phone !~ '^\+?[0-9]{7,15}$' THEN
            p_invalid_data := p_invalid_data || JSONB_BUILD_ARRAY(JSONB_BUILD_OBJECT(
                'row', i, 'name', p_names[i], 'phone', p_phones[i],
                'reason', CASE
                    WHEN NULLIF(clean_name, '') IS NULL THEN 'name is blank'
                    ELSE 'phone must contain 7-15 digits and may start with +'
                END
            ));
        ELSE
            CALL upsert_contact(clean_name, clean_phone);
        END IF;
    END LOOP;
END;
$$;

CREATE OR REPLACE PROCEDURE delete_contacts(
    p_username TEXT DEFAULT NULL,
    p_phone TEXT DEFAULT NULL
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF NULLIF(BTRIM(p_username), '') IS NULL AND NULLIF(BTRIM(p_phone), '') IS NULL THEN
        RAISE EXCEPTION 'provide a username or phone number to delete';
    END IF;

    DELETE FROM contacts c
    WHERE (NULLIF(BTRIM(p_username), '') IS NOT NULL
           AND LOWER(c.first_name) = LOWER(BTRIM(p_username)))
       OR (NULLIF(BTRIM(p_phone), '') IS NOT NULL
           AND c.phone = BTRIM(p_phone));
END;
$$;
