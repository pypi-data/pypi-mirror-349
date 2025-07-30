from pydantic import BaseModel, Field


class AudioRecordDTO(BaseModel):
    entity_type: str = Field(..., pattern="^(audiorecord)$")
    id: str
    record_name: str
    file_path: str
    storage_id: str
    text: str | None = None
    language: str | None = None
    tags: list[str]
    last_updated: str

    class Config:
        from_attributes = True
