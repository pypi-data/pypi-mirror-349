from pydantic import BaseModel, Field


class UserDTO(BaseModel):
    entity_type: str = Field(..., pattern="^(authuser|admin)$")
    id: str
    email: str
    password_hash: str
    registration_date: str
    last_updated: str
    is_blocked: bool
    temp_password_hash: str | None = None

    class Config:
        from_attributes = True
