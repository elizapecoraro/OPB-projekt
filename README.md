# Restavracije v Sloveniji

Projekt pri predmetu **Osnove podatkovnih baz**.

Avtorici: Eliza Katarina Pecoraro in Kaja Blažko

## Opis

Spletna aplikacija prikazuje gostinske obrate v Sloveniji na podlagi podatkov
OpenStreetMap. Uporabnik lahko podatke išče in filtrira po lokaciji, vrsti
kuhinje, dnevu v tednu, telefonu, spletni strani in delovnem času.

Poizvedba trenutno zajema objekte OSM z oznakami `restaurant`, `fast_food`
in `cafe`.

## Struktura projekta

- `Data/`: modeli, povezava z bazo, repozitorij ter uvoz podatkov;
- `Services/`: aplikacijska oziroma poslovna logika;
- `Presentation/`: HTML predloge in statične datoteke;
- `app.py`: vhodna točka spletne aplikacije.

`auth_public.py` vsebuje javni račun z omejenimi pravicami za zagon aplikacije.
Za ustvarjanje tabel in uvoz podatkov uporabi svojega lastnika baze prek datoteke
`.env`; primer je v `.env.example`. Zasebnega gesla ne objavi v Git.

## Namestitev

```bash
pip install -r requirenments.txt
```

V PostgreSQL izvedi `Data/create.sql`.

Javnemu uporabniku morajo biti dodeljene vsaj pravice za branje tabel:

```sql
GRANT CONNECT ON DATABASE sem2026_kajabl TO javnost;
GRANT USAGE ON SCHEMA public TO javnost;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO javnost;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT SELECT ON TABLES TO javnost;
```

## Prenos in posodobitev podatkov OSM

Celotno osvežitev izvede en ukaz:

```bash
python -m Data.sync_osm
```

Ta ukaz:

1. za Slovenijo prenese aktualne podatke iz Overpass API;
2. varno prepiše lokalni JSON;
3. doda nove restavracije;
4. posodobi obstoječe restavracije, kuhinje in delovne čase.

Restavracij, ki so bile iz OpenStreetMap odstranjene, ukaz namenoma ne izbriše
iz baze.

Ločena ukaza sta:

```bash
python -m Data.download_osm
python -m Data.import_json
```

## Zagon aplikacije

```bash
python app.py
```

Aplikacija je nato dosegljiva na `http://localhost:8080`.

## ER-diagram

![ER diagram baze](docs/restavracije_ER_koncni.png)
