from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, BOOLEAN, Text

from app.core.database import Base


class User(Base):
    """
    Класс пользователя.
    """

    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False, comment='Электронная почта пользователя.'
    )
    hashed_password: Mapped[str] = mapped_column(
        String(255), nullable=False, comment='Хэшированный пароль пользователя.'
    )
    name: Mapped[str] = mapped_column(
        String(255), nullable=False, comment='Имя пользователя.'
    )
    last_name: Mapped[str] = mapped_column(
        String(255), nullable=True, comment='Фамилия пользователя'
    )

    def __repr__(self):
        """
        Возвращает строковое представление объекта пользователя.
        :return: Строка в формате <User(id=..., email=..., full_name=...)>
        :rtype: str
        """
        return f"<User(id={self.id}, email={self.email}, name={self.name})>"
