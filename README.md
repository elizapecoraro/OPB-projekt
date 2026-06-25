# Iskalnik restavracij po Sloveniji

Projekt pri predmetu **Osnove podatkovnih baz**.

**Avtorici:** Eliza Katarina Pecoraro in Kaja Blažko

## Opis aplikacije

Aplikacija omogoča pregledovanje in iskanje restavracij po Sloveniji. Podatki o restavracijah, lokacijah, vrstah kuhinje in delovnem času so shranjeni v podatkovni bazi PostgreSQL. Spletni del aplikacije je izdelan v Pythonu z ogrodjem Bottle.

Aplikacija je namenjena pregledovanju podatkov, zato za običajno uporabo potrebuje samo bralni dostop do baze prek uporabnika `javnost`.

## Osnovne funkcionalnosti

Uporabnik lahko:

- išče restavracije po imenu, kraju ali vrsti kuhinje;
- filtrira restavracije po lokaciji, vrsti kuhinje in dnevu v tednu;
- prikaže samo restavracije, ki imajo telefonsko številko, spletno stran ali podatek o delovnem času;
- pregleduje rezultate po straneh;
- odpre podrobnosti posamezne restavracije;
- vidi naslov, vrste kuhinje, telefonsko številko, spletno stran in delovni čas;
- odpre lokacijo restavracije na zemljevidu.

## Lokalni zagon aplikacije

### 1. Kloniranje repozitorija

```bash
git clone https://github.com/elizapecoraro/OPB-projekt.git
cd OPB-projekt
```

Vse nadaljnje ukaze je treba izvajati iz korenske mape projekta.

### 2. Ustvarjanje virtualnega okolja

```bash
python -m venv .venv
```

Aktivacija virtualnega okolja:

**Windows PowerShell**

```powershell
.venv\Scripts\Activate.ps1
```

**Windows Command Prompt**

```cmd
.venv\Scripts\activate.bat
```

**macOS ali Linux**

```bash
source .venv/bin/activate
```

### 3. Namestitev knjižnic

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Nastavitev povezave z bazo

V korenski mapi projekta naredite datoteko `.env`. Najlažje je kopirati priloženo datoteko `.env.example` in jo preimenovati v `.env`.

Vsebina datoteke naj bo:

```dotenv
DB_HOST=baza.fmf.uni-lj.si
DB_PORT=5432
DB_NAME=sem2026_kajabl
DB_USER=javnost
DB_PASSWORD=
```

Datoteka `.env` ni vključena v repozitorij. Aplikacija jo ob zagonu samodejno prebere.

### 5. Zagon

```bash
python app.py
```

V brskalniku odprite:

```text
http://localhost:8080
```

Aplikacijo ustavite s `Ctrl+C`.

## Kratka navodila za uporabo

1. Na začetni strani v iskalno polje vnesite ime restavracije, kraja ali vrste kuhinje.
2. Po potrebi izberite lokacijo, vrsto kuhinje ali dan v tednu.
3. Z dodatnimi možnostmi omejite prikaz na restavracije s telefonom, spletno stranjo ali delovnim časom.
4. Pritisnite gumb za iskanje oziroma filtriranje.
5. Za več informacij kliknite posamezno restavracijo.
6. Na strani s podrobnostmi lahko odprete spletno stran restavracije ali njeno lokacijo na zemljevidu.

## Dostop do podatkovne baze

Aplikacija se mora povezovati z uporabnikom `javnost`, ki ima pravice za povezavo z bazo, uporabo sheme `public` in branje tabel aplikacije.
Za pripravo lokalne konfiguracije kopirajte datoteko `.env.example` v `.env`.

**Windows PowerShell:**
```powershell
Copy-Item .env.example .env
```

**macOS ali Linux:**
```bash
cp .env.example .env
```

Nastavitve javne povezave so že zapisane v datoteki `.env.example`.

## ER-diagram
![ER-diagram podatkovne baze](docs/restavracije_ER_koncni.png)

## Posodabljanje podatkov

1. `Data/download_osm.py` pridobi podatke iz Overpass API.
2. `Data/create.sql` na novo izdela podatkovno shemo.
3. `Data/import_osm.py` uvozi pridobljene podatke.

**Pozor:** `Data/create.sql` najprej izbriše obstoječe tabele, zato ga ne zaganjajte nad bazo, ki jo želite ohraniti.

## Vir podatkov

Začetni podatki o restavracijah so pridobljeni iz projekta OpenStreetMap.
