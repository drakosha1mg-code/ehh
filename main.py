import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# Токен бота от BotFather
BOT_TOKEN = ""
# Ваш Telegram User ID
OWNER_ID = 6530507181
# ID канала, куда отправлять сообщения (например, -1001234567890 или @channel_username)
TARGET_CHANNEL_ID = "-1003897347296"  # Можно использовать строку для @username

# Включаем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Обработчик для новых сообщений в бизнес-чатах
async def handle_business_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.business_message:
        message = update.business_message
        chat = message.chat
        user = message.from_user
        
        logger.info(f"Получено бизнес-сообщение из чата {chat.id}")
        
        # Определяем, кто написал
        if user.id == OWNER_ID:
            sender = "Вы"
        else:
            sender = "Клиент"
        
        # Формируем текст для отправки в канал
        channel_text = f"**Новое сообщение от {sender}**\n\n"
        channel_text += f"Чат: {chat.title or chat.first_name or 'Личный чат'}\n"
        channel_text += f"Отправитель: {user.first_name} {user.last_name or ''}\n"
        if message.text:
            channel_text += f"Текст: {message.text}"
        
        # Отправляем в канал с помощью контекста бота [2]
        try:
            await context.bot.send_message(
                chat_id=TARGET_CHANNEL_ID,
                text=channel_text,
                parse_mode='Markdown'  # Для красивого форматирования
            )
            logger.info(f"Сообщение переслано в канал {TARGET_CHANNEL_ID}")
        except Exception as e:
            logger.error(f"Ошибка отправки в канал: {e}")

# Обработчик для измененных сообщений
async def handle_edited_business_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.edited_business_message:
        message = update.edited_business_message
        # Можно также отправлять уведомления об изменениях в канал
        await context.bot.send_message(
            chat_id=TARGET_CHANNEL_ID,
            text=f"⚠️ Сообщение отредактировано в чате {message.chat.id}"
        )

def main():
    # Создаем приложение
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Добавляем обработчики
    app.add_handler(MessageHandler(
        filters.ChatType.PRIVATE & filters.BusinessMessage(), 
        handle_business_message
    ))
    app.add_handler(MessageHandler(
        filters.StatusUpdate.EDIT, 
        handle_edited_business_message
    ))
    
    # Запускаем бота
    print(f"Бот запущен. Будет отправлять сообщения в канал {TARGET_CHANNEL_ID}")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
