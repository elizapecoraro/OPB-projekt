"""Vzpostavljanje povezav s PostgreSQL.

Privzeto uporabi javne podatke iz auth_public.py. Vrednosti v datoteki .env
imajo prednost, zato zasebnih gesel ni treba zapisati v Git.
"""

import os
from contextlib import contextmanager
from pathlib import Path

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor

import Data.auth_public as auth


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def _nastavitev(ime: str, privzeta_vrednost):
    vrednost = os.getenv(ime)
    if vrednost is None or vrednost.strip() == "":
        return privzeta_vrednost
    return vrednost.strip()


def get_connection():
    return psycopg2.connect(
        host=_nastavitev("DB_HOST", auth.host),
        port=int(_nastavitev("DB_PORT", auth.port)),
        dbname=_nastavitev("DB_NAME", auth.db),
        user=_nastavitev("DB_USER", auth.user),
        password=os.getenv("DB_PASSWORD", auth.password),
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
