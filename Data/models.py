from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

@dataclass_json
@dataclass
class Lokacija:
    lokacija_id: int
    ime_lokacije: str

@dataclass_json
@dataclass
class Kuhinja:
    kuhinja_id: int
    vrsta: str

@dataclass_json
@dataclass
class Restavracija:
    restavracija_id: int
    osm_id: Optional[int]
    osm_tip: Optional[str]
    ime: str
    ulica: Optional[str]
    hisna_stevilka: Optional[str]
    telefon: Optional[str]
    spletna_stran: Optional[str]
    zemljepisna_sirina: Optional[Decimal]
    zemljepisna_dolzina: Optional[Decimal]
    lokacija_id: int
    ime_lokacije: Optional[str] = None

@dataclass_json
@dataclass
class DelovniCas:
    delovni_cas_id: int
    restavracija_id: int
    dan_v_tednu: str
    ura_od: Optional[str]
    ura_do: Optional[str]
