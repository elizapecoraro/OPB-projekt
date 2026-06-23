-- Ukaze izvede lastnik baze.
-- Aplikacija je bralna, zato uporabnik javnost potrebuje pravico SELECT.

GRANT CONNECT ON DATABASE sem2026_kajabl TO javnost;
GRANT USAGE ON SCHEMA public TO javnost;

GRANT SELECT ON TABLE
    lokacija,
    restavracija,
    kuhinja,
    restavracija_kuhinja,
    delovni_cas
TO javnost;

ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT SELECT ON TABLES TO javnost;
