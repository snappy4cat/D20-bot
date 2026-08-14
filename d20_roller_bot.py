import random
import time
import telebot

# --- НАСТРОЙКИ БОТА ---
# 1. Замените на токен от @BotFather (в кавычках)
TOKEN = "8978654674:AAFief139JWmHrZFwWsV05kvBooRgy_FtIg"
# 2. Замените на цифровой ID фурри-игрока (число без кавычек)
TARGET_USER_ID = 6903464097
# 3. Юзернейм вашего бота с собачкой (в кавычках)
BOT_USERNAME = "@D20rollerforchatbot"

bot = telebot.TeleBot(TOKEN)

# Глобальный множитель проклятия (стартует с 1)
mute_multiplier = 1


# ОБРАБОТЧИК ДЛЯ ГИФОК И ФОТО
@bot.message_handler(content_types=["photo", "animation"])
def handle_media_game(message):
    global mute_multiplier  # Разрешаем изменять глобальную переменную

    # Проверяем, что медиа прислал именно наш "целевой" пользователь
    if message.from_user.id == TARGET_USER_ID:

        roll = random.randint(0, 20)
        current_time = int(time.time())

        # ИСХОД 1: Выпала двойка — Множитель растет, мута нет
        if roll == 0:
            mute_multiplier += 1
            bot.reply_to(
                message,
                f"🎲 Выпало: *0*! Мута нет, но тебе порвали туз... Следующий мут будет дольше обычного.... 🔮\n\n"
                f"Твой следующий мут будет умножен на x{mute_multiplier}! Пока живи.",
                parse_mode="Markdown",
            )

        # ИСХОД 2: Критический провал (Единица) — Сутки * Множитель
        elif roll == 1:
            base_duration = 86400  # 24 часа в секундах
            final_duration = base_duration * mute_multiplier
            days = mute_multiplier  # сколько суток сидеть в муте

            bot.reply_to(
                message,
                f"🎲 НА КУБИКЕ 1! КРИТИЧЕСКИЙ ПРОВАЛ! 💀🦊\n\n"
                f"Проклятие сработало на максимум! Твой мут умножен на x{mute_multiplier}.\n\n"
                f"🔇 Ты отправляешься в изгнание на {days} сут(ок)!",
                parse_mode="Markdown",
            )

            apply_mute(
                message.chat.id,
                message.from_user.id,
                current_time + final_duration,
            )
            mute_multiplier = 1  # Сбрасываем множитель после наказания

        # ИСХОД 3: Обычный провал (от 3 до 10) — 1 минута * Множитель
        elif 3 <= roll <= 10:
            base_duration = 60  # 1 минута в секундах
            final_duration = base_duration * mute_multiplier
            minutes = mute_multiplier

            bot.reply_to(
                message,
                f"🎲 Выпало: *{roll}*.\n\n"
                f"Не повезло! С учетом проклятия x{mute_multiplier} отдыхаешь в муте {minutes} мин.",
                parse_mode="Markdown",
            )

            apply_mute(
                message.chat.id,
                message.from_user.id,
                current_time + final_duration,
            )
            mute_multiplier = 1  # Сбрасываем множитель после наказания

        # ИСХОД 4: Обычный успех (от 11 до 19) — Просто красивый сейв
        elif 11 <= roll <= 19:
            bot.reply_to(
                message,
                f"🎲 Выпало: *{roll}*.\n\n"
                f"Проверка пройдена! В этот раз тебе повезло, живи. Чат замер до следующей гифки...",
                parse_mode="Markdown",
            )

        # ИСХОД 5: Критический успех (Двадцать) — Триумф фурри-искусства
        elif roll == 20:
            bot.reply_to(
                message,
                f"🎲 Выпало: *20*! КРИТИЧЕСКИЙ УСПЕХ! ✨🦊\n\n"
                f"Мастер кубика! Твоя гифка великолепна, никаких наказаний, чат признает твое величие!",
                parse_mode="Markdown",
            )


# ОБРАБОТЧИК ДЛЯ СТАНДАРТНОГО РОЛЛА ПО ПИНГУ В ЧАТЕ
@bot.message_handler(content_types=["text"])
def handle_text_ping(message):
    text = message.text.lower()
    if (
        BOT_USERNAME.lower() in text
        or "ролл" in text
        or "кубик" in text
        or "d20" in text
    ):
        roll = random.randint(1, 20)
        bot.reply_to(message, f"🎲 На d20 выпадает: {roll}")

# ВСПОМОГАТЕЛЬНАЯ ФУНКЦИЯ ДЛЯ ВЫДАЧИ МУТА
def apply_mute(chat_id, user_id, until_date):
    try:
        bot.restrict_chat_member(
            chat_id=chat_id,
            user_id=user_id,
            until_date=until_date,
            can_send_messages=False,
            can_send_media_messages=False,
            can_send_other_messages=False,
        )
    except Exception as e:
        print(f"Ошибка мута (проверьте права админа у бота): {e}")

# ЗАПУСК (Всегда в самом конце кода)
print("Бот бдит.......")
bot.polling(none_stop=True, timeout = 60, long_polling_timeout=20)
