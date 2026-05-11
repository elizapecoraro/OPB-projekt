import os
from contextlib import contextmanager

import psycopg2
from psycopg2.extras import RealDictCursor


def get_connection():
    """Vrne povezavo na PostgreSQL bazo.

    Podatke nastavimo z okoljskimi spremenljivkami:
    DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD.
    """
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "restavracije"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
    )


@contextmanager
def get_cursor():
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            yield cur
            conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
