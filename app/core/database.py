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
    Класс для управления подключением к базе данных и создания асинхронных сессий.
    """

    def __init__(
            self,
            url: str,
            echo: bool = False,
            echo_pool: bool = False,
            pool_size: int = 5,
            max_overflow: int = 10
    ) -> None:
        """
        Инициализирует DatabaseHelper.

        :param url: URL для подключения к базе данных.
        :param echo: Если True, SQLAlchemy будет выводить все SQL-запросы в консоль.
        :param echo_pool: Если True, SQLAlchemy будет выводить информацию о пуле соединений.
        :param pool_size: Количество соединений в пуле.
        :param max_overflow: Максимальное количество соединений, которые могут быть созданы сверх pool_size.
        """
        self.engine = create_async_engine(
            url=url,
            echo=echo,
            echo_pool=echo_pool,
            pool_size=pool_size,
            max_overflow=max_overflow
        )
        self.async_session_maker = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False,
        )

    async def dispose(self) -> None:
        """
        Закрывает все соединения с базой данных.
        """
        await self.engine.dispose()

    async def session_getter(self):
        """
        Генератор для получения асинхронной сессии.

        :yield: Асинхронная сессия для работы с базой данных.
        """
        async with self.async_session_maker() as session:
            yield session


class Base(AsyncAttrs, DeclarativeBase):
    """
    Абстрактный базовый класс для всех моделей базы данных.

    Этот класс предоставляет общие поля и методы для всех моделей, такие как:
    - Автоматическое создание имени таблицы.
    - Уникальный идентификатор (UUID).
    - Временные метки создания и обновления.
    """

    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """
        Автоматически генерирует имя таблицы на основе имени класса.
        :return: Имя таблицы в нижнем регистре с добавлением 's' в конце.
        """
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
    echo_pool=settings.ECHO_POOL,
    pool_size=settings.POOL_SIZE,
    max_overflow=settings.MAX_OVERFLOW,
)
