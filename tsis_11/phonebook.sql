CREATE OR REPLACE FUNCTION search_phonebook(pattern TEXT)
RETURNS TABLE(id INT, first_name TEXT, phone_number TEXT)
AS $$
BEGIN
    RETURN QUERY
    SELECT id, first_name, phone_number
    FROM phonebook
    WHERE first_name ILIKE '%' || pattern || '%' OR phone_number ILIKE '%' || pattern || '%';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE insert_or_update_user(name TEXT, phone TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE first_name = name) THEN
        UPDATE phonebook SET phone_number = phone WHERE first_name = name;
    ELSE
        INSERT INTO phonebook(first_name, phone_number) VALUES (name, phone);
    END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE insert_many_users(names TEXT[], phones TEXT[], OUT invalid_data TEXT[])
LANGUAGE plpgsql
AS $$
DECLARE
    i INT;
BEGIN
    invalid_data := ARRAY[]::TEXT[];
    FOR i IN 1 .. array_length(names, 1) LOOP
        IF phones[i] ~ '^\\d{6,15}$' THEN
            CALL insert_or_update_user(names[i], phones[i]);
        ELSE
            invalid_data := array_append(invalid_data, names[i] || ' - ' || phones[i]);
        END IF;
    END LOOP;
END;
$$;

CREATE OR REPLACE FUNCTION get_phonebook_page(limit_count INT, offset_count INT)
RETURNS TABLE(id INT, first_name TEXT, phone_number TEXT)
AS $$
BEGIN
    RETURN QUERY
    SELECT id, first_name, phone_number
    FROM phonebook
    ORDER BY id
    LIMIT limit_count OFFSET offset_count;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE delete_user(identifier TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM phonebook
    WHERE first_name = identifier OR phone_number = identifier;
END;
$$;
