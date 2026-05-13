import os
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager

from Data import auth_public


def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", auth_public.host),
        port=os.getenv("DB_PORT", auth_public.port),
        dbname=os.getenv("DB_NAME", auth_public.db),
        user=os.getenv("DB_USER", auth_public.user),
        password=os.getenv("DB_PASSWORD"),
        cursor_factory=RealDictCursor,
    )


@contextmanager
def get_cursor():
    conn = get_connection()
    try:
        cur = conn.cursor()
        yield cur
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()
