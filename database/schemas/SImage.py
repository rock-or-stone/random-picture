from .CustomBaseModel import CustomBaseModel
from typing import Optional


class SImage(CustomBaseModel):
    id: Optional[int] = None
    image: bytes


__all__ = ["SImage"]
