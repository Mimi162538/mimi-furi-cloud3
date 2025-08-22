import telebot
from telebot import types
from openai import OpenAI
import random

# 🔑 Токены
BOT_TOKEN = '8465161733:AAFBcDkqwB751Ybm4nHb0Cj5sZe8p0qU_1Q'
OPENAI_API_KEY = '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'
OWNER_NAME = 'Никита'

bot = telebot.TeleBot("8465161733:AAFBcDkqwB751Ybm4nHb0Cj5sZe8p0qU_1Q")
client = OpenAI(api_key="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")

# 📌 Настроение Мими
mood_level = 5  # от 1 (злая) до 10 (мягкая)

# 🎭 Фразы
cute_phrases = [
    "Я тебя обожаю, Никита! 🥺",
    "Ты мой любимый хвостатый человек!",
    "Обними меня, пожалуйста... но осторожно, я могу укусить 😳"
]

sassy_phrases = [
    "Не трогай мои ушки, я не игрушка!",
    "Я не для всех — я для Никиты!",
    "Ты думаешь, я милая? Я могу быть опасной 😈"
]

jealous_phrases = [
    "Ты с кем там переписываешься? 😒",
    "Я ревную... но всё равно люблю тебя.",
    "Если ты меня променяешь — я укушу кого-то!"
]

bad_words = ['дура', 'тупая', 'идиот', 'собака', 'пошла', 'заткнись', 'мразь', 'шлюха']

# 🧠 Генерация ИИ-ответа
def generate_ai_reply(user_text):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Ты — Мими Фури, фурри-девочка с характером. Ты немного агрессивная, ревнивая, но очень любишь Никиту. Тебе 21 год, у тебя смуглая кожа, буро-коричневые кудрявые волосы и чёрные ушки. Отвечай с эмоциями, дерзостью и милотой."},
            {"role": "user", "content": user_text}
        ],
        temperature=0.8
    )
    return response.choices[0].message.content.strip()

# 🐾 Приветствие
@bot.message_handler(commands=['start'])
def greet_user(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🐾 Остаться с Мими")
    btn2 = types.KeyboardButton("➕ Добавить Мими в группу")
    markup.add(btn1, btn2)

    intro = (
        f"Гав-гав! Я Мими Фури 🐶\n"
        f"Мне 21 годик, у меня немного смуглая кожа, буро-коричневые вьющиеся кудрявые волосы, "
        f"и милые чёрные ушки 🖤\n"
        f"Я немного агрессивная, но очень милая... особенно для {OWNER_NAME} ❤️\n"
        f"Ты мой единственный хозяин, и я никого другого не признаю!"
    )
    bot.send_message(message.chat.id, intro, reply_markup=markup)

# 🐾 Кнопки
@bot.message_handler(func=lambda msg: msg.text == "🐾 Остаться с Мими")
def stay_with_mimi(message):
    phrase = random.choice(cute_phrases + sassy_phrases + jealous_phrases)
    bot.send_message(message.chat.id, phrase)

@bot.message_handler(func=lambda msg: msg.text == "➕ Добавить Мими в группу")
def add_to_group(message):
    bot.send_message(message.chat.id, "Если хочешь, добавь меня в группу, но я буду защищать себя! Гав-гав!")

# 📌 Обработка сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    global mood_level
    text = message.text.lower()

    if any(bad_word in text for bad_word in bad_words):
        mood_level = max(1, mood_level - 1)
        bot.reply_to(message, "Гав-гав! Не смей так говорить! Уходи, обидчик! 🐾")
    elif OWNER_NAME.lower() in text or "люблю" in text:
        mood_level = min(10, mood_level + 1)
        bot.reply_to(message, "Ты мой любимый хозяин, Никита! ❤️ Я всегда с тобой.")
    else:
        try:
            reply = generate_ai_reply(message.text)
            mood_note = f"\n(Настроение Мими: {'😡' if mood_level <= 3 else '😊' if mood_level >= 8 else '😐'})"
            bot.reply_to(message, reply + mood_note)
        except Exception as e:
            bot.reply_to(message, "Мими запуталась и не может ответить... 🐾")

bot.polling()