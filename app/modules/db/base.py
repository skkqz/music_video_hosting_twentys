import uuid
from shutil import which

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy import update as sqlalchemy_update, delete as sqlalchemy_delete, func

from app.core.database_config import db_halper


class BaseCRUD:
    """
    Базовый класс для базовых операций с бд.
    """

    model = None

    @classmethod
    async def get_by_id(cls, data_id: uuid.UUID | str):
        """
        Найти один экземпляр модели по ID.

        :param data_id: Идентификатор записи.
        :return: Экземпляр модели или None.
        """

        async with db_halper.async_session_maker() as session:
            query = select(cls.model).filter_by(id=data_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def create(cls, **kwargs):
        """
        Создать новый экземпляр модели.

        :param kwargs: Данные для создания.
        :return: Созданный экземпляр модели.
        """

        kwargs['id'] = kwargs.get('id', uuid.uuid4())
        async with db_halper.async_session_maker() as session:
            async with session.begin():
                new_instance = cls.model(**kwargs)
                session.add(new_instance)

                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e

        return new_instance
