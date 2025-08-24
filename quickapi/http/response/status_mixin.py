import attrs
from quickapi.http.response.status import Status

_status_map = {
    'Continue': Status.Continue,
    'SwitchingProtocol': Status.SwitchingProtocol,
    'Ok': Status.Ok,
    'Created': Status.Created,
    'Accepted': Status.Accepted,
    'MultipleChoices': Status.MultipleChoices,
    'MovedPermanently': Status.MovedPermanently,
    'Found': Status.Found,
    'SeeOther': Status.SeeOther,
    'NotModified': Status.NotModified,
    'TemporaryRedirect': Status.TemporaryRedirect,
    'PermanentRedirect': Status.PermanentRedirect,
    'BadRequest': Status.BadRequest,
    'Unauthorized': Status.Unauthorized,
    'PaymentRequired': Status.PaymentRequired,
    'Forbiden': Status.Forbiden,
    'NotFound': Status.NotFound,
    'MethodNotAllowed': Status.MethodNotAllowed,
    'RequestTimeout': Status.RequestTimeout,
    'LengthRequired': Status.LengthRequired,
    'TeaPot': Status.TeaPot,
    'UpgradeRequired': Status.UpgradeRequired,
    'InternalServerError': Status.InternalServerError,
    'NotImplemented': Status.NotImplemented,
    'BadGateway': Status.BadGateway,
}

def inject_status_mixin(cls):
    for name, status in _status_map.items():
        def prop(self, _status=status):
            return attrs.evolve(self, status=_status)
        setattr(cls, name, property(prop))
    return cls
