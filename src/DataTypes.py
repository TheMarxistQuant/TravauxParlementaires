from dataclasses import dataclass
from enum import Enum


@dataclass
class BaseDataType:
    ...

class SingletonMeta(type):
    _instances = {}
    _keys_name: tuple

    def __call__(cls, *args, **kwargs):
        if cls not in SingletonMeta._instances:
            SingletonMeta._instances[cls] = {}
        key = SingletonMeta.get_key(cls._keys_name, **kwargs)
        if not key in cls._instances[cls]:
            SingletonMeta._instances[cls][key] = super().__call__(*args, **kwargs)
        return SingletonMeta._instances[cls][key]

    @staticmethod
    def get_key(keys_name, **kwargs):
        key_list = []
        for key_name in keys_name:
            d = kwargs
            key_name_parts = key_name.split('.')
            for part in key_name_parts[:-1]:
                d = d[part]
            key_list.append(d[key_name_parts[-1]])
        return tuple(key_list)


@dataclass
class Scrutin(BaseDataType, metaclass=SingletonMeta):
    _keys_name = ("numero", "date")
    numero: int
    date: str
    type: str
    sort: str
    titre: str
    nombre_votants: str
    nombre_pours: str
    nombre_contres: str
    nombre_abstentions: str
    demandeurs: str
    demandeurs_groupes_acronymes: str
    url_institution: str
    url_nosdeputes: str
    url_nosdeputes_api: str

    def __hash__(self):
        return hash(f"{self.numero}_{self.date}")


class VotePosition(Enum):
    pour = 1
    contre = -1
    abstention = 0
    nonVotant = 0
    _default = 0

    @classmethod
    def from_string(cls, value):
        try:
            return cls[value]
        except KeyError:
            return cls._default


@dataclass
class Vote(BaseDataType, metaclass=SingletonMeta):
    _keys_name = ("scrutin.numero", "scrutin.date", "parlementaire_slug")
    scrutin: Scrutin
    parlementaire_groupe_acronyme: str
    parlementaire_slug: str
    position: VotePosition
    position_groupe: VotePosition
    par_delegation: str
    mise_au_point_position: str

    def __post_init__(self):
        self.scrutin = Scrutin(**self.scrutin)
        self.position = VotePosition.from_string(self.position)
        self.position_groupe = VotePosition.from_string(self.position_groupe)


@dataclass(kw_only=True)
class Depute(BaseDataType, metaclass=SingletonMeta):
    _keys_name = ("id", "slug", "mandat_debut")
    id: str
    nom: str
    nom_de_famille: str
    prenom: str
    sexe: str
    date_naissance: str
    lieu_naissance: str
    num_deptmt: str
    nom_circo: str
    num_circo: str
    mandat_debut: str
    mandat_fin: str = None
    ancien_depute: int = None
    groupe_sigle: str
    parti_ratt_financier: str
    sites_web: list
    emails: list = None
    adresses: list = None
    collaborateurs: list = None
    autres_mandats: list = None
    anciens_autres_mandats: list = None
    anciens_mandats: list
    profession: str
    place_en_hemicycle: str
    url_an: str
    id_an: str
    slug: str
    url_nosdeputes: str
    url_nosdeputes_api: str
    nb_mandats: str
    twitter: str


@dataclass(kw_only=True)
class Organisme(BaseDataType, metaclass=SingletonMeta):
    _keys_name = ("id", "slug")
    id: str
    slug: str
    nom: str
    acronyme: str
    groupe_actuel: str
    couleur: str
    order: str
    type: str
    url_nosdeputes: str
    url_nosdeputes_api: str
