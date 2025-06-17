
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

clients = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Я бот сервісу. Щоб залишити заявку, натисни кнопку нижче.")

async def handle_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.message.from_user.id
    clients[user_id] = text
    print("chat_id:", update.message.chat_id)
    await update.message.reply_text("✅ Заявку отримано. Ми зателефонуємо найближчим часом!")

app = ApplicationBuilder().token("7715128894:AAFaA0ZGlroyEDkZAB13iEvpGhoIqk8mqk4").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_request))

app.run_polling()

