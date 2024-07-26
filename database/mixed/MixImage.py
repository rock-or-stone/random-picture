from ..models import session
from ..models import Image
from ..schemas import SImage

from sqlalchemy import func, select


class MixImage:
    @staticmethod
    async def save(data: SImage) -> None:
        async with session() as s:
            s.add(Image(**data.model_dump(exclude_none=True)))

    @staticmethod
    async def get_random() -> SImage:
        async with session() as s:
            q = select(Image).order_by(func.random())

            return SImage.model_validate((await s.execute(q)).scalar_one())


__all__ = ["MixImage"]
