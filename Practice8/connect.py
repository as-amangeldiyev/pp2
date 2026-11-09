import psycopg2
from psycopg2.extensions import connection

from config import DB_CONFIG


CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS contacts (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL CHECK (length(trim(first_name)) > 0),
    phone VARCHAR(32) NOT NULL UNIQUE CHECK (length(trim(phone)) > 0),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
)
"""

ADD_SURNAME_SQL = "ALTER TABLE contacts ADD COLUMN IF NOT EXISTS surname VARCHAR(100)"


def get_connection() -> connection:
    """Open a PostgreSQL connection using the settings in config.py."""
    return psycopg2.connect(**DB_CONFIG)


def initialize_database() -> None:
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(CREATE_TABLE_SQL)
            cursor.execute(ADD_SURNAME_SQL)
