
import attrs
from quickapi.http.response.status import Status

class ResponseStatusMixin:
    @property
    def Continue(self):
        return attrs.evolve(self, status=Status.Continue)

    @property
    def SwitchingProtocol(self):
        return attrs.evolve(self, status=Status.SwitchingProtocol)

    @property
    def Ok(self):
        return attrs.evolve(self, status=Status.Ok)

    @property
    def Created(self):
        return attrs.evolve(self, status=Status.Created)

    @property
    def Accepted(self):
        return attrs.evolve(self, status=Status.Accepted)

    @property
    def MultipleChoices(self):
        return attrs.evolve(self, status=Status.MultipleChoices)

    @property
    def MovedPermanently(self):
        return attrs.evolve(self, status=Status.MovedPermanently)

    @property
    def Found(self):
        return attrs.evolve(self, status=Status.Found)

    @property
    def SeeOther(self):
        return attrs.evolve(self, status=Status.SeeOther)

    @property
    def NotModified(self):
        return attrs.evolve(self, status=Status.NotModified)

    @property
    def TemporaryRedirect(self):
        return attrs.evolve(self, status=Status.TemporaryRedirect)

    @property
    def PermanentRedirect(self):
        return attrs.evolve(self, status=Status.PermanentRedirect)

    @property
    def BadRequest(self):
        return attrs.evolve(self, status=Status.BadRequest)

    @property
    def Unauthorized(self):
        return attrs.evolve(self, status=Status.Unauthorized)

    @property
    def PaymentRequired(self):
        return attrs.evolve(self, status=Status.PaymentRequired)

    @property
    def Forbiden(self):
        return attrs.evolve(self, status=Status.Forbiden)

    @property
    def NotFound(self):
        return attrs.evolve(self, status=Status.NotFound)

    @property
    def MethodNotAllowed(self):
        return attrs.evolve(self, status=Status.MethodNotAllowed)

    @property
    def RequestTimeout(self):
        return attrs.evolve(self, status=Status.RequestTimeout)

    @property
    def LengthRequired(self):
        return attrs.evolve(self, status=Status.LengthRequired)

    @property
    def TeaPot(self):
        return attrs.evolve(self, status=Status.TeaPot)

    @property
    def UpgradeRequired(self):
        return attrs.evolve(self, status=Status.UpgradeRequired)

    @property
    def InternalServerError(self):
        return attrs.evolve(self, status=Status.InternalServerError)

    @property
    def NotImplemented(self):
        return attrs.evolve(self, status=Status.NotImplemented)

    @property
    def BadGateway(self):
        return attrs.evolve(self, status=Status.BadGateway)
