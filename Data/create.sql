CREATE TABLE lokacija (
    lokacija_id SERIAL PRIMARY KEY,
    ime_lokacije VARCHAR(100) NOT NULL
);

CREATE TABLE restavracija (
    restavracija_id SERIAL PRIMARY KEY,
    osm_id BIGINT,
    osm_tip VARCHAR(50),
    ime VARCHAR(150) NOT NULL,
    ulica VARCHAR(150),
    hisna_stevilka VARCHAR(20),
    telefon VARCHAR(50),
    spletna_stran VARCHAR(255),
    zemljepisna_sirina DECIMAL(10, 8),
    zemljepisna_dolzina DECIMAL(11, 8),
    lokacija_id INT NOT NULL,

    FOREIGN KEY (lokacija_id)
        REFERENCES lokacija(lokacija_id)
);

CREATE TABLE kuhinja (
    kuhinja_id SERIAL PRIMARY KEY,
    vrsta VARCHAR(100) NOT NULL
);

CREATE TABLE restavracija_kuhinja (
    restavracija_id INT NOT NULL,
    kuhinja_id INT NOT NULL,

    PRIMARY KEY (restavracija_id, kuhinja_id),

    FOREIGN KEY (restavracija_id)
        REFERENCES restavracija(restavracija_id),

    FOREIGN KEY (kuhinja_id)
        REFERENCES kuhinja(kuhinja_id)
);

CREATE TABLE delovni_cas (
    delovni_cas_id SERIAL PRIMARY KEY,
    restavracija_id INT NOT NULL,
    dan_v_tednu VARCHAR(20) NOT NULL,
    ura_od TIME,
    ura_do TIME,

    FOREIGN KEY (restavracija_id)
        REFERENCES restavracija(restavracija_id)
);