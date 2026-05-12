import os
import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import database

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def format_ranges(numeros):
    if not numeros: return ""
    numeros.sort()
    rangos = []
    inicio = numeros[0]
    fin = numeros[0]
    for n in numeros[1:]:
        if n == fin + 1:
            fin = n
        else:
            rangos.append(str(inicio) if inicio == fin else f"{inicio}-{fin}")
            inicio = fin = n
    rangos.append(str(inicio) if inicio == fin else f"{inicio}-{fin}")
    return ", ".join(rangos)

def get_user_id(update: Update):
    user = update.effective_user
    # Mapeo manual para mantener tu cuenta principal
    # Si eres tú (tu usuario de Telegram), te asignará a 'MarcosDB12'
    # Como no sé tu username, simplemente usamos 'MarcosDB12' por defecto
    # Si quieres que tus amigos tengan su propia DB, coméntalo y usa la línea de abajo.
    # return user.username or user.first_name
    return 'MarcosDB12'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = get_user_id(update)
    database.inicializar_album_completo(user_id)
    
    keyboard = [
        [InlineKeyboardButton("📊 Estadísticas", callback_data='estadisticas')],
        [InlineKeyboardButton("❌ Ver Faltantes", callback_data='falta'),
         InlineKeyboardButton("🔄 Ver Repetidos", callback_data='repetidos')],
        [InlineKeyboardButton("🌐 Abrir Dashboard Web", callback_data='web')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"¡Hola! Soy tu asistente para la colección Panini Mundial 2026.\n"
        f"👤 Colección Activa: *{user_id}*\n\n"
        "Para añadir cromos usa el comando:\n"
        "`/tengo ESP 1, ARG 5`\n\n"
        "Para borrarlos:\n"
        "`/quitar ESP 1`\n\n"
        "¿Qué quieres consultar ahora?",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = get_user_id(update)
    
    if query.data == 'estadisticas':
        await estadisticas_logic(user_id, query.message.reply_text)
    elif query.data == 'falta':
        await falta_logic(user_id, query.message.reply_text)
    elif query.data == 'repetidos':
        await repetidos_logic(user_id, query.message.reply_text)
    elif query.data == 'web':
        await web_logic(query.message.reply_text)

async def estadisticas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = get_user_id(update)
    await estadisticas_logic(user_id, update.message.reply_text)

async def estadisticas_logic(user_id, reply_func):
    total, faltantes, repetidos = database.get_stats(user_id)
    conseguidos = total - faltantes
    porcentaje = round((conseguidos / total) * 100, 1) if total > 0 else 0
    
    texto = (
        f"📊 *Estadísticas de {user_id}*\n\n"
        f"✅ *Conseguidos:* {conseguidos} / {total} ({porcentaje}%)\n"
        f"❌ *Faltantes:* {faltantes}\n"
        f"🔄 *Repetidos:* {repetidos} cromos extra"
    )
    await reply_func(texto, parse_mode='Markdown')

async def tengo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    user_id = get_user_id(update)
    
    if not args:
        await update.message.reply_text("Por favor, indica los IDs. Ejemplo: /tengo ARG 1, ESP 2")
        return

    texto = " ".join(args)
    cromos = [c.strip().upper() for c in texto.split(',') if c.strip()]
    
    registrados = []
    for cromo_id in cromos:
        database.update_cromo(user_id, cromo_id, 1)
        registrados.append(cromo_id)

    await update.message.reply_text(f"✅ Registrados en {user_id}: {', '.join(registrados)}")

async def quitar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    user_id = get_user_id(update)
    
    if not args:
        await update.message.reply_text("Por favor, indica los IDs. Ejemplo: /quitar ARG 1")
        return

    texto = " ".join(args)
    cromos = [c.strip().upper() for c in texto.split(',') if c.strip()]
    
    borrados = []
    for cromo_id in cromos:
        database.update_cromo(user_id, cromo_id, -1)
        borrados.append(cromo_id)

    await update.message.reply_text(f"🗑️ Borrados de {user_id}: {', '.join(borrados)}")

async def falta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = get_user_id(update)
    await falta_logic(user_id, update.message.reply_text)

async def falta_logic(user_id, reply_func):
    faltantes = database.get_faltantes(user_id)
    if not faltantes:
        await reply_func("¡Felicidades! No tienes cromos registrados como faltantes.")
        return

    agrupados = {}
    for equipo, numero in faltantes:
        if equipo not in agrupados:
            agrupados[equipo] = []
        agrupados[equipo].append(numero)
    
    lineas = []
    for equipo, numeros in agrupados.items():
        rango_str = format_ranges(numeros)
        lineas.append(f"*{equipo}* ({len(numeros)}): {rango_str}")

    texto = "\n".join(lineas)
    if len(texto) > 4000:
        texto = texto[:4000] + "\n... (lista truncada)"
        
    await reply_func(f"❌ *Te faltan {len(faltantes)} cromos:*\n\n{texto}", parse_mode='Markdown')

async def repetidos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = get_user_id(update)
    await repetidos_logic(user_id, update.message.reply_text)

async def repetidos_logic(user_id, reply_func):
    reps = database.get_repetidos(user_id)
    if not reps:
        await reply_func("No tienes cromos repetidos en este momento.")
        return

    agrupados = {}
    for equipo, numero, cantidad in reps:
        if equipo not in agrupados:
            agrupados[equipo] = []
        if cantidad > 2:
            agrupados[equipo].append(f"{numero}(x{cantidad-1})")
        else:
            agrupados[equipo].append(str(numero))
            
    lineas = []
    for equipo, numeros_str in agrupados.items():
        lineas.append(f"*{equipo}*: {', '.join(numeros_str)}")

    texto = "\n".join(lineas)
    if len(texto) > 4000:
        texto = texto[:4000] + "\n... (lista truncada)"
        
    await reply_func(f"🔄 *Cromos repetidos ({len(reps)}):*\n\n{texto}", parse_mode='Markdown')

async def web(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await web_logic(update.message.reply_text)

async def web_logic(reply_func):
    url = os.environ.get('WEB_URL', 'http://localhost:5000')
    await reply_func(
        f"🌐 Puedes gestionar tu colección visualmente en el Dashboard Web:\n\n"
        f"👉 {url}\n\n"
        f"*(Asegúrate de que la aplicación web, app.py, esté corriendo. Si estás en el móvil con la misma WiFi, sustituye localhost por la IP de tu PC)*",
        parse_mode='Markdown'
    )

def main():
    database.init_db()

    token = os.environ.get('TELEGRAM_TOKEN')
    if not token:
        print("ERROR: No se encontró la variable de entorno TELEGRAM_TOKEN.")
        return

    application = ApplicationBuilder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("tengo", tengo))
    application.add_handler(CommandHandler("quitar", quitar))
    application.add_handler(CommandHandler("falta", falta))
    application.add_handler(CommandHandler("repetidos", repetidos))
    application.add_handler(CommandHandler("estadisticas", estadisticas))
    application.add_handler(CommandHandler("web", web))
    
    # Manejador para los botones interactivos
    application.add_handler(CallbackQueryHandler(button_callback))

    print("Bot iniciado. Presiona Ctrl+C para detener.")
    application.run_polling()

if __name__ == '__main__':
    main()
