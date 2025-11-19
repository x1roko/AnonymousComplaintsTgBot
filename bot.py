import asyncio
import os
import aiomysql
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from dotenv import load_dotenv

# 1. Загрузка переменных окружения
load_dotenv()

# 2. Конфигурация (данные 'bot_user')
BOT_TOKEN = os.getenv("BOT_TOKEN")
DB_HOST = os.getenv("DB_HOST")
DB_DATABASE = os.getenv("DB_DATABASE")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = int(os.getenv("DB_PORT", 3306))

# Инициализация
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
db_pool = None

async def init_db_pool():
    """Инициализация пула соединений с БД."""
    global db_pool
    print("Попытка инициализации пула соединений с MySQL...")
    try:
        db_pool = await aiomysql.create_pool(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            db=DB_DATABASE,
            autocommit=True, # Включаем автокоммит для простоты
            # Задержка для отладки
            connect_timeout=10 
        )
        print("Пул соединений с MySQL успешно создан.")
    except aiomysql.Error as e:
        print(f"Критическая ошибка подключения к MySQL: {e}")
        # Завершаем работу, если не можем подключиться к БД
        exit(1)


@dp.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    """Обработчик команды /start."""
    await message.answer("Привет! Отправь мне любое сообщение, и я анонимно сохраню его текст в базу данных.")


@dp.message()
async def save_message_handler(message: types.Message) -> None:
    """Обработчик всех текстовых сообщений."""
    if message.text:
        message_text = message.text

        # Сохранение только текста сообщения
        try:
            async with db_pool.acquire() as conn:
                async with conn.cursor() as cur:
                    # Используем %s как плейсхолдер для безопасности
                    await cur.execute(
                        "INSERT INTO anonymous_messages (message_text) VALUES (%s)",
                        (message_text,)
                    )
            await message.answer("Сообщение анонимно сохранено!")
        except Exception as e:
            await message.answer("Произошла ошибка при сохранении данных. Попробуйте позже.")
            print(f"Ошибка БД: {e}")

    else:
        await message.answer("Я могу сохранить только текстовые сообщения.")


async def main() -> None:
    # Инициализация пула соединений
    await init_db_pool()
    # Запуск обработки обновлений
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен.")
    finally:
        if db_pool:
            db_pool.close()
            # Обязательно ждем закрытия пула
            asyncio.run(db_pool.wait_closed())
            print("Соединение с БД закрыто.")
