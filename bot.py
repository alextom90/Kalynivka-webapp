from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
)

TYPE, ISSUE, NAME, PHONE = range(4)
clients = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("📝 Залишити заявку", web_app=WebAppInfo(url="https://alextom90.github.io/kalynivka-webapp/new-request.html"))]
    ]
    await update.message.reply_text(
        "👋 Привіт! Я бот майстерні з ремонту техніки.\nНатисни кнопку нижче, щоб залишити заявку або введи вручну.",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )
    await update.message.reply_text("➡️ Введи тип пристрою (наприклад, смартфон):")
    return TYPE

async def get_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["type"] = update.message.text
    await update.message.reply_text("🔧 Опиши проблему:")
    return ISSUE

async def get_issue(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["issue"] = update.message.text
    await update.message.reply_text("👤 Введи своє ім'я:")
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("📞 Введи номер телефону:")
    return PHONE

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["phone"] = update.message.text
    order_id = f"ORD{len(clients)+1:03}"
    clients[order_id] = context.user_data.copy()
    await update.message.reply_text(f"✅ Дякуємо! Заявку прийнято.\nНомер замовлення: {order_id}")
    return ConversationHandler.END

async def check_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    code = update.message.text.strip().upper()
    if code in clients:
        data = clients[code]
        await update.message.reply_text(
            f"🔎 Статус заявки {code}:\nТип: {data['type']}\nПроблема: {data['issue']}\nІм’я: {data['name']}"
        )
    else:
        await update.message.reply_text("⚠️ Заявку не знайдено. Перевір номер.")
    return ConversationHandler.END

if __name__ == "__main__":
    app = ApplicationBuilder().token("7715128894:AAFaA0ZGlroyEDkZAB13iEvpGhoIqk8mqk4").build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_type)],
            ISSUE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_issue)],
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
        },
        fallbacks=[]
    )

    app.add_handler(conv)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_status))
    app.run_polling()
