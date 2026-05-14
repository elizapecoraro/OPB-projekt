DROP TABLE IF EXISTS restavracija_kuhinja CASCADE;
DROP TABLE IF EXISTS delovni_cas CASCADE;
DROP TABLE IF EXISTS restavracija CASCADE;
DROP TABLE IF EXISTS kuhinja CASCADE;
DROP TABLE IF EXISTS lokacija CASCADE;

CREATE TABLE lokacija (
    lokacija_id SERIAL PRIMARY KEY,
    ime_lokacije VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE restavracija (
    restavracija_id SERIAL PRIMARY KEY,
    osm_id BIGINT NOT NULL,
    osm_tip VARCHAR(50) NOT NULL,

    ime VARCHAR(150) NOT NULL,
    ulica VARCHAR(150),
    hisna_stevilka VARCHAR(20),
    telefon VARCHAR(50),
    spletna_stran VARCHAR(255),

    zemljepisna_sirina DECIMAL(10, 8),
    zemljepisna_dolzina DECIMAL(11, 8),

    -- originalen OSM zapis, npr. "Mo-Fr 10:00-22:00; Sa 12:00-23:00"
    opening_hours_raw TEXT,

    lokacija_id INT NOT NULL REFERENCES lokacija(lokacija_id),

    UNIQUE (osm_id, osm_tip)
);

CREATE TABLE kuhinja (
    kuhinja_id SERIAL PRIMARY KEY,
    vrsta VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE restavracija_kuhinja (
    restavracija_id INT NOT NULL REFERENCES restavracija(restavracija_id) ON DELETE CASCADE,
    kuhinja_id INT NOT NULL REFERENCES kuhinja(kuhinja_id) ON DELETE CASCADE,
    PRIMARY KEY (restavracija_id, kuhinja_id)
);

CREATE TABLE delovni_cas (
    delovni_cas_id SERIAL PRIMARY KEY,
    restavracija_id INT NOT NULL REFERENCES restavracija(restavracija_id) ON DELETE CASCADE,

    -- 1 = ponedeljek, 2 = torek, ..., 7 = nedelja
    dan_v_tednu SMALLINT NOT NULL CHECK (dan_v_tednu BETWEEN 1 AND 7),

    ura_od TIME,
    ura_do TIME,

    UNIQUE (restavracija_id, dan_v_tednu, ura_od, ura_do)
);

CREATE INDEX idx_restavracija_lokacija ON restavracija(lokacija_id);
CREATE INDEX idx_restavracija_ime ON restavracija(LOWER(ime));
CREATE INDEX idx_kuhinja_vrsta ON kuhinja(LOWER(vrsta));
CREATE INDEX idx_delovni_cas_dan ON delovni_cas(dan_v_tednu);


SELECT COUNT(*) FROM restavracija;
SELECT COUNT(*) FROM lokacija;
SELECT COUNT(*) FROM kuhinja;
SELECT COUNT(*) FROM delovni_cas;