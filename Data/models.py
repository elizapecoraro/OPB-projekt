"""Podatkovni modeli in DTO-ji aplikacije."""

from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Lokacija:
    lokacija_id: int = 0
    ime_lokacije: str = ""


@dataclass_json
@dataclass
class Kuhinja:
    kuhinja_id: int = 0
    vrsta: str = ""


@dataclass_json
@dataclass
class Restavracija:
    """Model, ki ustreza tabeli restavracija."""

    restavracija_id: int = 0
    osm_id: Optional[int] = None
    osm_tip: Optional[str] = None
    ime: str = ""
    ulica: Optional[str] = None
    hisna_stevilka: Optional[str] = None
    telefon: Optional[str] = None
    spletna_stran: Optional[str] = None
    zemljepisna_sirina: Optional[Decimal] = None
    zemljepisna_dolzina: Optional[Decimal] = None
    opening_hours_raw: Optional[str] = None
    lokacija_id: int = 0


@dataclass_json
@dataclass
class RestavracijaDto:
    """Podatki, ki jih aplikacija prikazuje po združitvi več tabel."""

    restavracija_id: int = 0
    osm_id: Optional[int] = None
    osm_tip: Optional[str] = None
    ime: str = ""
    ulica: Optional[str] = None
    hisna_stevilka: Optional[str] = None
    telefon: Optional[str] = None
    spletna_stran: Optional[str] = None
    zemljepisna_sirina: Optional[Decimal] = None
    zemljepisna_dolzina: Optional[Decimal] = None
    opening_hours_raw: Optional[str] = None
    ime_lokacije: Optional[str] = None
    kuhinje: str = ""


@dataclass_json
@dataclass
class DelovniCas:
    delovni_cas_id: int = 0
    restavracija_id: int = 0
    dan_v_tednu: int = 0
    ura_od: Optional[str] = None
    ura_do: Optional[str] = None
