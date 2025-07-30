from pydantic import BaseModel, validator
from typing import Optional

class Client(BaseModel):
    id: int
    name: str
    email: str
    age: Optional[int]

    @validator("email")
    def email_must_contain_at(cls, v):
        if "@" not in v:
            raise ValueError("Email invalide")
        return v

    @validator("age")
    def age_must_be_positive(cls, v):
        if v is not None and v < 0:
            raise ValueError("L'âge doit être positif")
        return v
