from enum import Enum
from collections import namedtuple

LegislatureType = namedtuple("Legislature", ("name", "url_prefix", "url_suffix"))


class LegislatureEnum(Enum):
    XIII = LegislatureType("XIII", "2007-2012", "13")
    XIV = LegislatureType("XIV", "2012-2017", "14")
    XV = LegislatureType("XV", "2017-2022", "15")
    XVI = LegislatureType("XVI", "www", "16")
