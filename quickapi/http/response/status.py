import enum


class Status(tuple, enum.Enum):
    Ok          = (200, "Ok")
    NotFound    = (400, "Not Found")
    ServerError = (500, "Internal Server Error")

    @property
    def code(self) -> int:
        return self.value[0]
    
    @property
    def reason(self) -> str:
        return self.value[1]
    
    @property
    def description(self) -> str:
        return self.reason

    def __str__(self) -> str:
        return f"{self.code} {self.reason}"
