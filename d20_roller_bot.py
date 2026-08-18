import random
import time
import telebot
from flask import Flask
import threading

# Создаем микро-веб-сервер для обмана Render
app = Flask('')

@app.route('/')
def home():
    return "Бот работает стабильно!"

def run_web_server():
    # Запускаем сайт на порту 10000 (стандарт для Render)
    app.run(host='0.0.0.0', port=10000)

# --- НАСТРОЙКИ БОТА ---
# 1. Замените на токен от @BotFather (в кавычках)
TOKEN = "8978654674:AAFief139JWmHrZFwWsV05kvBooRgy_FtIg"
# 2. Замените на цифровой ID игрока (число без кавычек)
TARGET_USER_ID = [6903464097, 7117523150, 7109011464]
# 3. Юзернейм вашего бота с собачкой (в кавычках)
BOT_USERNAME = "@D20rollerforchatbot"

bot = telebot.TeleBot(TOKEN)

# Глобальный множитель проклятия (стартует с 1)
mute_multiplier = 1

# КАРТА ИСХОДОВ КУБИКА (Число: (Текст, Время мута в сек, Ссылка на гифку или None))
# Вы можете менять эти тексты и время прямо тут в любой момент!
D20_CONFIG = {
    1: ("🎲 *1*! ЛОШАРА! \n oткисай в муте, уебок. Сутки пошли", 86400,
        "https://files.catbox.moe/nzjpgo.mp4"),
    2: ("🎲 *2*! Почти единица, потрогай траву, чепушило.. .", 43300, 'https://files.catbox.moe/btlfqv.mp4'),
    3: ("🎲 *3*! Ужасный бросок. Посиди-ка в муте.", 28800, 'https://files.catbox.moe/btlfqv.mp4'),
    4: ("🎲 *4*! Невезение — это не оправдание, а твой образ жизни.", 21600, 'https://files.catbox.moe/m1ro4w.jpeg'),
    5: ("🎲 *5*! Попытка засчитана, но твоя статистика говорит сама за себя. Посиди в муте.", 10800, 'https://files.catbox.moe/btlfqv.mp4'),
    6: ("🎲 *6*! Не повезло. 2 часа мута твои.", 7200, None),
    7: ("🎲 *7*! На грани, но всё ещё провал. Мут.", 3600, 'https://imgflip.com/gif/7abl83'),
    8: ("🎲 *8*! Чуть-чуть не хватило до сейва. Мут.", 1800, 'https://files.catbox.moe/m1ro4w.jpeg'),
    9: ("🎲 *9*! Не повезло! Отдыхаешь в муте.", 900, None),
    10: ("🎲 *10*! Почти получилось, но все еще мут", 300, 'https://files.catbox.moe/m1ro4w.jpeg'),
    11: ("🎲 *11*! Твой бросок — как твоя жизнь: серый и посредственный", 0, None),
    12: ("🎲 *12*! Вот вроде бросок и позорище, а вроде переступил порог", 0, None),
    13: ("🎲 *13*! Чертова дюжина, но тебе повезло, мута нет.", 0, None),
    14: ("🎲 *14*!К всеобщему сожалению у тебя сохранилось право голоса. Пока что....", 0, None),
    15: ("🎲 *15*! Еще немного, и ты станешь кем-то. Но пока ты всего лишь цифра.", 0, None),
    16: ("🎲 *16*! Уверенный успех! Можешь скинуть еще че-нибудь.Вдруг снова повезет", 0, 'https://share.google/J9Rycc3pi1u6PBSGB'),
    17: ("🎲 *17*! Удача сегодня на твоей стороне.", 0, 'https://files.catbox.moe/l8z444.gif'),
    18: ("🎲 *18*! Хороший результат, админы недовольно вздыхают.", 0, 'https://share.google/J9Rycc3pi1u6PBSGB'),
    19: ("🎲 *19*!Критический успех! Звёзды сошлись и судьба наконец намекает: пора купить себе дорогой фурсьют, а не позориться здесь.", 0, 'https://files.catbox.moe/l8z444.gif'),
    20: ("🎲 *20*! Критический успех! Сама Ткань Судьбы сплелась в твою пользу. Жаль только, что боги расточают свои дары на существо с повадками дворняги. Впрочем, носи свой фурри костюмчик с гордостью !", 0,
         "https://files.catbox.moe/kcob7a.gif")
}


# 1. ОБРАБОТЧИК ДЛЯ ГИФОК И ФОТО (Переписан на словари с дилэями)
@bot.message_handler(content_types=["photo", "animation"])
def handle_media_game(message):
    global mute_multiplier

    # Проверяем, что медиа прислал именно наш "целевой" пользователь
    if message.from_user.id in TARGET_USER_ID:
        roll = random.randint(0, 20)
        current_time = int(time.time())

        # Забираем настройки для выпавшего числа из нашего словаря D20_CONFIG
        phrase, base_mute_time, gif_url = D20_CONFIG[roll]

        # Шаг А: Сначала всегда отправляем базовый текст ответа бота
        bot.reply_to(message, phrase, parse_mode="Markdown")

        # Шаг Б: Если для этого числа привязана гифка (например, для 1 или 20) — шлем её
        if gif_url:
            bot.send_animation(
                chat_id=message.chat.id,
                animation=gif_url,
                reply_to_message_id=message.message_id
            )
            time.sleep(1.0)  # Дилэй 3 секунды, чтобы успели посмотреть гифку перед мутом

        # Шаг В: Обрабатываем логику проклятия (для двойки)
        if roll == 0:
            mute_multiplier = 2
            # Дополнительно пишем в чат актуальный уровень проклятия
            bot.send_message(
                message.chat.id,
                f"Порванный туз увеличил время проклятия: **x{mute_multiplier}**!",
                parse_mode="Markdown"
            )
            return  # Выходим из функции, мут давать не нужно

        # Шаг Г: Если число проигрышное — рассчитываем мут с учетом множителя
        if base_mute_time > 0:
            final_duration = base_mute_time * mute_multiplier

            # Если сидим больше суток, пересчитаем красиво для текста
            if final_duration >= 86400:
                time_text = f"**{final_duration // 86400} сут(ок)**"
            else:
                time_text = f"**{final_duration // 60} мин**"

            # Пишем финальное предупреждение перед техническим мутом
            bot.send_message(
                message.chat.id,
                f" Поражение! мут составит: {time_text}.",
                parse_mode="Markdown"
            )
            time.sleep(1.0)

            # Выдаем реальный мут в Telegram
            apply_mute(message.chat.id, message.from_user.id, current_time + final_duration)

            # Сбрасываем множитель обратно в 1
            mute_multiplier = 1


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


# ЗАПУСК БОТА С АВТО-ПОДНЯТИЕМ
if __name__ == "__main__":
    # Запускаем обманный веб-сервер в отдельном фоновом потоке
    server_thread = threading.Thread(target=run_web_server)
    server_thread.daemon = True
    server_thread.start()

    print("Веб-сервер заглушки запущен. Включаем бота...")

    while True:
        try:
            bot.polling(none_stop=True, timeout=60, long_polling_timeout=20)
        except Exception as e:
            print(f"Сетевой лаг замечен: {e}. Переподключение через 5 секунд...")
            time.sleep(5)
