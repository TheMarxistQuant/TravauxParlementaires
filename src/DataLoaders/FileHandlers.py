import urllib.request
from pathlib import Path
import json

from .common import DataFileFormat
from .Legislature import LegislatureEnum, LegislatureType
from .FileStubs import ScrutinsFileStub, ScrutinFileStub, DeputesFileStub, OrganismeFileStub


class NosDeputesAbstractFileHandler:
    _root_url = r"https://{prefix}.nosdeputes.fr"
    legislature: LegislatureType
    _root_cache_path = Path.home() / "NosDeputesCache"
    file_format: DataFileFormat = DataFileFormat.JSON
    data_title : str
    stub_reader: type

    def __init__(self, legislature: LegislatureEnum = LegislatureEnum.XV):
        self.legislature = legislature.value

    @property
    def url(self):
        raise NotImplementedError()

    @property
    def root_url(self):
        return self._root_url.format(prefix=self.legislature.url_prefix)

    def load_data(self, force_download=False):
        path_with_extension = f"{self.url}/{self.file_format.value}"
        remote_path_with_extension = f"{self.root_url}/{path_with_extension}"
        local_path_with_extension = self._root_cache_path / f"{self.legislature.name}" / path_with_extension.replace('\\', '/').lstrip('/')
        if force_download or not local_path_with_extension.exists():
            # we download the file from source
            local_path_with_extension.parent.mkdir(parents=True, exist_ok=True)
            urllib.request.urlretrieve(remote_path_with_extension, local_path_with_extension)
        with open(local_path_with_extension, 'r') as local_file:
            data = json.load(local_file)
        return self.stub_reader(data)


class NosDeputesScrutinsFileHandler(NosDeputesAbstractFileHandler):
    data_title = 'Scrutins'
    stub_reader = ScrutinsFileStub

    @property
    def url(self):
        return f"{self.legislature.url_suffix}/scrutins"



class NosDeputesScrutinFileHandler(NosDeputesAbstractFileHandler):
    scrutin_id: int
    data_title = 'Scrutin'
    stub_reader = ScrutinFileStub

    def __init__(self, legislature: LegislatureEnum, scrutin_id:int):
        super().__init__(legislature=legislature)
        self.scrutin_id = scrutin_id

    @property
    def url(self):
        return f"{self.legislature.url_suffix}/scrutin/{self.scrutin_id}"


class NosDeputesDeputesFileHandler(NosDeputesAbstractFileHandler):
    data_title = 'Deputes'
    stub_reader = DeputesFileStub

    @property
    def url(self):
        return f"deputes"

class NosDeputesGroupsFileHandler(NosDeputesAbstractFileHandler):
    data_title = 'Groups'
    stub_reader = OrganismeFileStub

    @property
    def url(self):
        return f"organismes/groupe"
