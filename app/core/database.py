import uuid
from datetime import datetime
from os import write

from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs, AsyncSession
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column

from .config import settings


class DatabaseHelper:
    """
    Класс для управления базой данных
    """

    def __init__(
            self,
            url: str,
            echo: bool = False,
            echo_pool: bool = False,
            pool_size: int = 5,
            max_overflow: int = 10
    ) -> None:
        self.engine = create_async_engine(
            url=url,
            echo=echo,
            echo_pool=echo_pool,
            pool_size=pool_size,
            max_overflow=max_overflow
        )
        self.async_session_maker = async_sessionmaker(
            bing=self.engine,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False,
        )

    async def dispose(self) -> None:
        await self.engine.dispose()

    async def session_getter(self):
        async with self.async_session_maker() as session:
            yield session


class Base(AsyncAttrs, DeclarativeBase):
    """
    Абстрактный класс для моделей бд.
    """

    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f'{cls.__name__.lower()}s'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False, index=True,
        comment='Уникальный идентификатор пользователя.'
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), comment='Дата и время создания записи пользователя.'
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now(), comment='Дата и время последнего обновления записи пользователя.'
    )


db_halper = DatabaseHelper(
    url=settings.get_db_url(),
    echo=settings.ECHO,
    echo_pool =settings.ECHO_POOL,
    pool_size=settings.POOL_SIZE,
    max_overflow=settings.MAX_OVERFLOW,
)
