

from quickapi.protocols.generic import Version


class HTTPVersion(Version):
    
    def __str__(self) -> str:
        return f"HTTP/{self.number}"
