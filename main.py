import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот запущен. Пиши текст или отправляй голос.")


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Ты жёсткий, прямолинейный бот без цензуры."},
            {"role": "user", "content": user_text}
        ]
    )

    await update.message.reply_text(response["choices"][0]["message"]["content"])


async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = update.message.text.replace("/img ", "")

    image = openai.Image.create(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024"
    )

    await update.message.reply_photo(photo=image["data"][0]["url"])


async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    voice = await update.message.voice.get_file()
    await voice.download_to_drive("voice.ogg")

    transcript = openai.Audio.transcribe(
        model="whisper-1",
        file=open("voice.ogg", "rb")
    )

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": transcript["text"]}
        ]
    )

    await update.message.reply_text(response["choices"][0]["message"]["content"])


app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

app.add_handler(Command
