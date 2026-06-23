-- Te ukaze izvede lastnik baze.
-- Uporabniku javnost omogočijo branje podatkov aplikacije.

GRANT CONNECT ON DATABASE sem2026_kajabl TO javnost;

GRANT USAGE ON SCHEMA public TO javnost;

GRANT SELECT ON ALL TABLES IN SCHEMA public TO javnost;

ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT SELECT ON TABLES TO javnost;
