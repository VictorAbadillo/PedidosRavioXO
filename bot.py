import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")

PEDIDOS = {}

# Áreas y empleados
AREAS = {
    "cuarto_frio": ["Pedro", "Lucía"],
    "cocina_servicio": ["Mario", "Elena"],
    "produccion": ["Javier"],
    "pasteleria": ["Sofía"]
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hola, soy PEDIXO 🤖. Escribe tus pedidos línea por línea. Para eliminar, escribe 'No necesito <producto>'")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    text = update.message.text.strip()

    # Detecta área
    area = None
    for k, v in AREAS.items():
        if user in v:
            area = k
            break
    if not area:
        await update.message.reply_text("❌ No estás registrado en ninguna área.")
        return

    if area not in PEDIDOS:
        PEDIDOS[area] = []

    if text.lower().startswith("no necesito "):
        prod = text[11:].strip()
        if prod in PEDIDOS[area]:
            PEDIDOS[area].remove(prod)
            await update.message.reply_text(f"✅ Eliminado: {prod}")
        else:
            await update.message.reply_text(f"❌ {prod} no estaba en tu pedido")
    else:
        PEDIDOS[area].append(text)
        await update.message.reply_text(f"✅ Añadido: {text}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("PEDIXO corriendo...")
    app.run_polling()

if __name__ == "__main__":
    main()
