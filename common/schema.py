from pydantic import BaseModel


class SignInRequest(BaseModel):
    email: str
    password: str


class CreateStoryRequest(BaseModel):
    prompt: str
    response: str = ''


class UpdateStoryRequest(BaseModel):
    response: str
