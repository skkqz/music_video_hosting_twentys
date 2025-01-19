from app.modules.db.base import BaseCRUD
from app.modules.user.models import User


class UserDAO(BaseCRUD):
    """
    Класс для работы с объектом пользователя в бд
    """

    model = User
