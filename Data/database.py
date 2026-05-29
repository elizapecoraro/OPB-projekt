import os
from contextlib import contextmanager
from pathlib import Path

import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def _obvezna_nastavitev(ime: str) -> str:
    vrednost = os.getenv(ime)
    if vrednost is None or vrednost.strip() == "":
        raise RuntimeError(f"Manjka nastavitev {ime} v datoteki .env")
    return vrednost


def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=_obvezna_nastavitev("DB_NAME"),
        user=_obvezna_nastavitev("DB_USER"),
        password=os.getenv("DB_PASSWORD", ""),
        cursor_factory=RealDictCursor,
    )


@contextmanager
def get_cursor():
    conn = get_connection()
    cur = conn.cursor()

    try:
        yield cur
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()