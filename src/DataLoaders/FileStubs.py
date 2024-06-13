from ..DataTypes import Scrutin, Vote, Depute, Organisme


class StubFileReader:
    """
    All the files we get from the API are jsonified nested dictionaries of the type:
        { key_outer : [
            key_inner : { data we're interested in}
        ]
        }
    We provide a generic class to construct and return a list of objects based on that.
    """
    DataTypeBuilder: type
    key_outer: str
    key_inner: str

    def __init__(self, payload):
        self._payload = payload
        self._is_cached_property = False
        self._cached_property = None

    def _parse_payload(self):
        self._cached_property = []
        if not self._payload:
            return
        for stub in self._payload[self.key_outer]:
            generic_object = self.DataTypeBuilder(**stub[self.key_inner])
            self._cached_property.append(generic_object)

    @property
    def items(self):
        if not self._is_cached_property:
            self._parse_payload()
            self._is_cached_property = True
        return self._cached_property


class ScrutinsFileStub(StubFileReader):
    DataTypeBuilder = Scrutin
    key_outer = "scrutins"
    key_inner = "scrutin"


class ScrutinFileStub(StubFileReader):
    DataTypeBuilder = Vote
    key_outer = "votes"
    key_inner = "vote"


class DeputesFileStub(StubFileReader):
    DataTypeBuilder = Depute
    key_outer = "deputes"
    key_inner = "depute"


class OrganismeFileStub(StubFileReader):
    DataTypeBuilder = Organisme
    key_outer = "organismes"
    key_inner = "organisme"
