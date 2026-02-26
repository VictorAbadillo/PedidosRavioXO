# Usamos Python 3.11 oficial
FROM python:3.11-slim

# Carpeta de la app
WORKDIR /app

# Copiamos archivos
COPY requirements.txt .
COPY bot.py .

# Instalamos dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Variable de entorno del token
# (Render permite configurarla en la interfaz de Environment)
ENV BOT_TOKEN=${BOT_TOKEN}

# Comando para iniciar el bot
CMD ["python", "bot.py"]
