import json
from .utils import utf8_string_to_bytes, utf8_bytes_to_string
from semver_range import Range

class JSONDatagram:
    """
    A class to handle JSON datagrams with versioning and type information.

    Attributes:
        type (str): The type of the datagram.
        version (str): The version of the datagram.
        version_constraint (Range): The version constraint for the datagram.
    """
    def __init__(self, type: str, version: str = "0.0.1", version_constraint: Range = Range("<=0.1.0")):
        """
        Initialize a JSONDatagram instance.

        :param type: The type of the datagram.
        :param version: The version of the datagram.
        :param version_constraint: The version constraint for the datagram.
        """
        # The version constraint is not used (currently)
        self.type = type
        self.version = version
        self.version_constraint = version_constraint

    def serialize(self, data) -> bytes:
        """
        Serialize the datagram to a JSON byte array.

        :param data: The data to be serialized.
        :return: The serialized data as a byte array.
        """
        return utf8_string_to_bytes(json.dumps({"version":self.version, "type": self.type, "data": data},separators=(',', ':')))
        
    def deserialize(self, data: bytes) -> str:
        """
        Deserialize the JSON byte array to retrieve the data.

        :param data: The byte array to be deserialized.
        :return: The deserialized data as a string.
        """
        parsed = json.loads(utf8_bytes_to_string(data))

        return parsed["data"]