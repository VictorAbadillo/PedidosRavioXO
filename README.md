# PedidosRavioXO
- Bot de pedidos de RavioXO

Este bot recoge los pedidos de las diferentes áreas del restaurante:
- Cuarto frío
- Cocina servicio
- Producción
- Pastelería
- Pruebas

Funciona así:
1. Cada empleado escribe su pedido al bot.
2. Puede editar o eliminar productos antes de las 18:00.
3. A las 18:00, el bot envía un resumen agrupado por proveedor SOLO a los jefes.

Tecnología:
- Python
- SQLite para guardar pedidos
- Telegram Bot
- Render.com para ejecutar el bot 24/7
