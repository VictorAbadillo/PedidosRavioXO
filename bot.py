# bot.py
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from collections import defaultdict
import asyncio
from datetime import datetime

# ---------------------------
# CONFIGURACIÓN
# ---------------------------

TOKEN = os.environ.get("BOT_TOKEN")  # TOKEN seguro desde Render
GROUP_JEFES_ID = -1001234567890      # Cambia por el ID del chat de jefes

# Definimos áreas y usuarios (ejemplo)
AREAS = {
    "cuarto_frio": ["Ana", "Luis"],
    "cocina_servicio": ["Marta", "Jorge"],
    "produccion": ["Carlos"],
    "pasteleria": ["Sonia"]
}

# Definimos proveedores y días de reparto
PROVEEDORES = {
    "Frutas Eloy": {"dias_reparto": ["martes","jueves","sábado"], "hora_cierre": 18},
    "SOSA": {"dias_reparto": ["miércoles"], "hora_cierre": 16},
    "Carnicería López": {"dias_reparto": ["lunes","miércoles","viernes"], "hora_cierre": 18},
    "Huevos García": {"dias_reparto": ["lunes","martes","miércoles","jueves","viernes"], "hora_cierre": 18}
}

# Guardamos pedidos temporalmente
pedidos = []

# ---------------------------
# FUNCIONES DEL BOT
# ---------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "¡Hola! Soy PEDIXO 🤖\nEscribe tus pedidos línea por línea.\nEj: '2 kg chorizo'\nPuedes editar escribiendo 'No necesito X'")

# Guardar pedidos
async def guardar_pedido(update: Update, context: ContextTypes.DEFAULT_TYPE):
    usuario = update.effective_user.first_name
    texto = update.message.text.strip()

    if texto.lower().startswith("no necesito"):
        producto_eliminar = texto[11:].strip().lower()
        for p in pedidos:
            if p["usuario"] == usuario and p["producto"].lower() == producto_eliminar and p["activo"]:
                p["activo"] = False
        await update.message.reply_text(f"Producto '{producto_eliminar}' eliminado de tu pedido ✅")
        return

    # Intentamos separar cantidad y producto
    partes = texto.split(maxsplit=1)
    if len(partes) == 2 and partes[0].replace("kg","").isdigit():
        cantidad = partes[0]
        producto = partes[1]
    else:
        cantidad = ""
        producto = texto

    pedidos.append({
        "usuario": usuario,
        "producto": producto,
        "cantidad": cantidad,
        "activo": True
    })

    await update.message.reply_text(f"Pedido guardado: {texto} ✅")

# Enviar resumen a jefes
async def enviar_resumen(app):
    if not pedidos:
        mensaje = "Hoy no hay pedidos."
    else:
        # Agrupar por proveedor
        totales = defaultdict(list)
        dia_semana = datetime.now().strftime("%A").lower()
        for p in pedidos:
            if not p["activo"]:
                continue
            for proveedor, info in PROVEEDORES.items():
                if p["producto"].lower() in proveedor.lower() or True:  # Simple, puede mejorar mapeo exacto
                    if dia_semana in [d.lower() for d in info["dias_reparto"]]:
                        totales[proveedor].append(f"{p['cantidad']} {p['producto']}".strip())

        mensaje = "📦 PEDIDOS DEL DÍA\n\n"
        for proveedor, productos in totales.items():
            mensaje += f"---------------------\n{proveedor.upper()}\n---------------------\n"
            for prod in productos:
                mensaje += f"• {prod}\n"
            mensaje += "\n"

    await app.bot.send_message(chat_id=GROUP_JEFES_ID, text=mensaje)
    # Limpiar pedidos para el día siguiente
    pedidos.clear()

# ---------------------------
# MAIN
# ---------------------------

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, guardar_pedido))

    # Programar envío diario a las 18:00
    scheduler = AsyncIOScheduler()
    scheduler.add_job(lambda: enviar_resumen(app), 'cron', hour=18, minute=0)
    scheduler.start()

    await app.run_polling()

if _name_ == "_main_":
    asyncio.run(main())
