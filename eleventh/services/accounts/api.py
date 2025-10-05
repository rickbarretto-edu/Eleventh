from typing_extensions import Literal
from fastapi import APIRouter
from pydantic import BaseModel

from eleventh.services.accounts.repo import Creation, InMemoryAccounts

route = APIRouter(
    prefix="/accounts",
    tags=["accounts", "user"],
)


users = InMemoryAccounts()

class SignupInput(BaseModel):
    email: str
    username: str
    password: str

class SignupOutput(BaseModel):
    status: Literal["success", "username_taken", "email_taken"]

@route.post("/signup/")
async def create_user(user: SignupInput) -> SignupOutput:
    """Create a new user account.
    
    This endpoint returns the status of the creation attempt.
    """
    match await users.new(user.email, user.username, user.password):
        case Creation.SUCCESS:
            return SignupOutput(status="success")
        case Creation.USERNAME_TAKEN:
            return SignupOutput(status="username_taken")
        case Creation.EMAIL_TAKEN:
            return SignupOutput(status="email_taken")
        case _:
            raise RuntimeError("unhandled account creation result")

class LoginInput(BaseModel):
    email: str
    password: str

class ValidLogin(BaseModel):
    uuid: str
    status: Literal["valid"] = "valid"

class InvalidLogin(BaseModel):
    status: Literal["invalid-credentials"] = "invalid-credentials"

type LoginOutput = ValidLogin | InvalidLogin

@route.post("/login/")
async def login_user(user: LoginInput) -> LoginOutput:
    """Authenticate a user by their email and password.
    
    On success, this returns the user's UUID. On failure, it returns an
    invalid credentials message.
    """
    if account := await users.authenticate(user.email, user.password):
        return ValidLogin(uuid=str(account.uuid))
    else:
        return InvalidLogin()
