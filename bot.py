import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")

PEDIDOS = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hola, soy PEDIXO 🤖. Escribe tus pedidos.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    text = update.message.text

    if user not in PEDIDOS:
        PEDIDOS[user] = []

    if text.lower().startswith("no necesito "):
        producto = text[11:]
        if producto in PEDIDOS[user]:
            PEDIDOS[user].remove(producto)
            await update.message.reply_text(f"Eliminado: {producto}")
        else:
            await update.message.reply_text("Ese producto no estaba en tu lista.")
    else:
        PEDIDOS[user].append(text)
        await update.message.reply_text(f"Añadido: {text}")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("PEDIXO corriendo...")
    app.run_polling()

if __name__ == "__main__":
    main()