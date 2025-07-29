from abc import ABC


class MightyClient(ABC):
    def get_info(self):
        # TODO: Implement return Mighty Info from the server
        pass

class MightyDefaultClient(MightyClient):
    def __init__(self):
        pass

    def get_data(self) -> str:
        raise NotImplementedError("Not available")
    
