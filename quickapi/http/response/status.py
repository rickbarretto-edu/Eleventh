import enum


class Status(tuple, enum.Enum):
    Continue            = (100, "Continue")
    SwitchingProtocol   = (101, "Switching Protocol")
    
    Ok                  = (200, "Ok")
    Created             = (201, "Created")
    Accepted            = (202, "Accepted")

    MultipleChoices     = (300, "Multiple Choices")
    MovedPermanently    = (301, "Moved Permanently")
    Found               = (302, "Found")
    SeeOther            = (303, "See Other")
    NotModified         = (304, "Not Modified")
    TemporaryRedirect   = (307, "Temporary Redirect")
    PermanentRedirect   = (308, "Permanent Redirect")

    BadRequest          = (400, "BadRequest")
    Unauthorized        = (401, "Unauthorized")
    PaymentRequired     = (402, "Payment Required")
    Forbiden            = (403, "Forbidden")
    NotFound            = (404, "Not Found")
    MethodNotAllowed    = (405, "Method Not Allowed")
    RequestTimeout      = (408, "Request Timeout")
    LengthRequired      = (411, "Length Required")
    TeaPot              = (418, "I'm a teapot")
    UpgradeRequired     = (426, "Upgrade Required")

    InternalServerError = (500, "Internal Server Error")
    NotImplemented      = (501, "Not Implemented")
    BadGateway          = (502, "Bad Gateway")

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
