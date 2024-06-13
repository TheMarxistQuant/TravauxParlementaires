from .DataLoaders.FileHandlers import (
    NosDeputesScrutinsFileHandler,
    NosDeputesScrutinFileHandler,
    NosDeputesDeputesFileHandler,
    NosDeputesGroupsFileHandler,
    LegislatureEnum)
from .DataTypes import Scrutin, Depute, Organisme, Vote

from typing import Tuple, List
from dataclasses import dataclass
from multiprocessing.pool import ThreadPool
import itertools

@dataclass
class LegislatureData:
    scrutins: List[Scrutin]
    deputes: List[Depute]
    groupes: List[Organisme]
    votes: List[Vote]

def get_all_legislature_data(legislature: LegislatureEnum, force_download:bool=False) -> LegislatureData:
    """
    This is main entry point for getting live or cached data
    :param legislature: The legislature number we want to get data for
    :param force_download: ignores and overwrites any cached data
    :return: a LegislatureData object containing all the data.
    """
    def download_and_parse_votes(scrutin_id):
        stub = NosDeputesScrutinFileHandler(legislature=legislature,
                                            scrutin_id=scrutin_id).load_data(force_download=force_download)
        return stub.items

    all_scrutins = NosDeputesScrutinsFileHandler(legislature=legislature).load_data(force_download=force_download).items
    all_deputes = NosDeputesDeputesFileHandler(legislature=legislature).load_data(force_download=force_download).items
    all_groupes = NosDeputesGroupsFileHandler(legislature=legislature).load_data(force_download=force_download).items

    with ThreadPool(16) as pool:
        results = pool.map(download_and_parse_votes,
                        [s.numero for s in all_scrutins])
        all_votes = list(itertools.chain.from_iterable(results))
    return LegislatureData(scrutins=all_scrutins, deputes=all_deputes, groupes=all_groupes, votes=all_votes)


