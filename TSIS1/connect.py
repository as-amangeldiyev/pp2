import psycopg2
from psycopg2.extensions import connection

from config import DB_CONFIG


def get_connection() -> connection:
    return psycopg2.connect(**DB_CONFIG)


def initialize_database() -> None:
    base = __import__("pathlib").Path(__file__).resolve().parent
    with get_connection() as conn, conn.cursor() as cursor:
        cursor.execute("CREATE TABLE IF NOT EXISTS contact_groups (id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY, name VARCHAR(50) UNIQUE NOT NULL)")
        cursor.execute("CREATE TABLE IF NOT EXISTS contacts (id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, first_name VARCHAR(100) NOT NULL CHECK (BTRIM(first_name) <> ''), surname VARCHAR(100), email VARCHAR(100), birthday DATE, group_id INTEGER REFERENCES contact_groups(id), created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP)")
        cursor.execute("ALTER TABLE contacts ADD COLUMN IF NOT EXISTS surname VARCHAR(100), ADD COLUMN IF NOT EXISTS email VARCHAR(100), ADD COLUMN IF NOT EXISTS birthday DATE, ADD COLUMN IF NOT EXISTS group_id INTEGER REFERENCES contact_groups(id)")
        cursor.execute("CREATE TABLE IF NOT EXISTS phones (id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, contact_id BIGINT NOT NULL REFERENCES contacts(id) ON DELETE CASCADE, phone VARCHAR(32) NOT NULL, type VARCHAR(10) NOT NULL CHECK (type IN ('home','work','mobile')), UNIQUE(contact_id, phone))")
        cursor.execute("INSERT INTO contact_groups(name) VALUES ('Family'),('Work'),('Friend'),('Other') ON CONFLICT (name) DO NOTHING")
        cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name='contacts' AND column_name='phone'")
        if cursor.fetchone():
            cursor.execute("INSERT INTO phones(contact_id, phone, type) SELECT c.id, c.phone, 'mobile' FROM contacts c WHERE NOT EXISTS (SELECT 1 FROM phones p WHERE p.contact_id=c.id AND p.phone=c.phone) ON CONFLICT DO NOTHING")
