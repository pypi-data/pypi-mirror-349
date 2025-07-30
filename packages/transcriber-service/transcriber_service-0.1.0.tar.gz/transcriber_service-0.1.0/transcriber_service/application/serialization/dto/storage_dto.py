from pydantic import BaseModel, Field


class StorageDTO(BaseModel):
    entity_type: str = Field(..., pattern="^(storage)$")
    id: str
    user_id: str
    audio_record_ids: list[str]

    class Config:
        from_attributes = True
