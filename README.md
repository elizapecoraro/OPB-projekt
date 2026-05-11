# Restavracije v Sloveniji

Projekt pri predmetu **Osnove podatkovnih baz**. Cilj projekta je spletna aplikacija za pregled restavracij v Sloveniji. Podatki izhajajo iz OpenStreetMap/Overpass izvoza, aplikacija pa bo omogočala pregled restavracij po lokaciji, kuhinji in osnovnih kontaktnih podatkih.

## ER diagram baze

![ER diagram baze](docs/restavracije_ER_koncni.png)

## Trenutna struktura projekta

```text
restavracije_slovenija_projekt/
├── app.py
├── README.md
├── requirements.txt
├── requirenments.txt
├── .gitignore
├── .env.example
├── .vscode/
│   └── launch.json
├── Data/
│   ├── __init__.py
│   ├── create.sql
│   ├── database.py
│   ├── models.py
│   └── restavracija_repository.py
├── Services/
│   ├── __init__.py
│   └── restavracija_service.py
├── Presentation/
│   ├── __init__.py
│   ├── static/
│   │   └── style.css
│   └── views/
│       └── index.tpl
├── data/
│   ├── json_to_csv.py
│   ├── restavracije.csv
│   └── restavracije_slovenija.json
└── docs/
    └── restavracije_ER_koncni.png
```

Projekt je razdeljen na tri osnovne nivoje:

- `Data/` vsebuje podatkovni nivo: SQL shemo, modele in repozitorije za dostop do PostgreSQL baze.
- `Services/` vsebuje aplikacijski nivo: poslovno logiko, ki uporablja podatkovni nivo.
- `Presentation/` vsebuje predstavitveni nivo: predloge HTML in statične datoteke.

## Baza

SQL shema je v datoteki `Data/create.sql`. Trenutno vsebuje tabele:

- `lokacija`
- `restavracija`
- `kuhinja`
- `restavracija_kuhinja`
- `delovni_cas`

Osnovna ideja sheme je, da ima restavracija eno lokacijo, lahko ima več vrst kuhinj, in ima lahko več zapisov delovnega časa.

## Podatki

V mapi `data/` so izvorni podatki:

- `restavracije_slovenija.json` – izvoz iz OpenStreetMap/Overpass API.
- `json_to_csv.py` – skripta za pretvorbo JSON v CSV.
- `restavracije.csv` – CSV z restavracijami, ki imajo ime.

## Virtualno okolje

V korenu projekta ustvari virtualno okolje:

```bash
python -m venv env
```

Aktiviraj okolje na Linux/macOS:

```bash
source env/bin/activate
```

Aktiviraj okolje na Windows:

```bash
env\Scripts\activate
```

Namesti knjižnice:

```bash
pip install -r requirements.txt
```

Če preverjanje pri predmetu uporablja ime iz navodil `requirenments.txt`, je v projektu dodana tudi kopija te datoteke.

## Nastavitev baze

Ustvari PostgreSQL bazo, na primer:

```bash
createdb restavracije
```

Nato zaženi SQL shemo:

```bash
psql -d restavracije -f Data/create.sql
```

Za lokalne nastavitve baze lahko kopiraš `.env.example` v `.env` in popraviš vrednosti. Datoteka `.env` je namenoma v `.gitignore`, ker lahko vsebuje gesla.

## Zagon aplikacije

Ko je virtualno okolje aktivirano:

```bash
python app.py
```

Aplikacija se zažene na:

```text
http://localhost:8080
```

Če baza še ni ustvarjena ali podatki še niso uvoženi, se bo prikazalo opozorilo. To je pričakovano v začetni fazi projekta.

## Naslednji koraki

1. Pripravi skripto za uvoz podatkov iz `data/restavracije.csv` v PostgreSQL.
2. Dopolni podatkovni nivo z metodami za kuhinje, lokacije in delovni čas.
3. Dopolni spletne strani za iskanje po mestu, vrsti kuhinje in podrobnostih restavracije.
