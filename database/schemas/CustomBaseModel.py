from pydantic import BaseModel


class CustomBaseModel(BaseModel):
    class Config:
        from_attributes = True


__all__ = ["CustomBaseModel"]
