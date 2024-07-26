import sqlalchemy as sa
from sqlalchemy import orm as so

from .base import Base


class Image(Base):
    __tablename__ = "images"

    id: so.Mapped[int] = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    image: so.Mapped[bytes] = sa.Column(sa.LargeBinary, nullable=False)

    def __init__(self, image):
        self.image = image


__all__ = ["Image"]
