import asyncio
from app.modules.user.dao import UserDAO

async def main():
    # Создаем пользователя
    user = await UserDAO.create(
        email='qwe@qwe.com',
        hashed_password='123123123',
        name='Dava',
        last_name='Koko'
    )
    print(f"Пользователь создан: {user}")

# Запускаем асинхронную функцию
if __name__ == "__main__":
    asyncio.run(main())