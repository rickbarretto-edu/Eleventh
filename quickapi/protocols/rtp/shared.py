

from quickapi.protocols.generic import Version


class RTPVersion(Version):
    
    def __str__(self) -> str:
        return f"RTP/{self.number}"
