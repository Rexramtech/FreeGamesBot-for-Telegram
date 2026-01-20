import os
import re
import json
import asyncio
import logging
from datetime import datetime, timezone
from typing import Dict, List, Set, Tuple

import aiosqlite
import feedparser
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes

# ----------------------------
# Logging (menos ruido)
# ----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
log = logging.getLogger("free-games-bot")
logging.getLogger("httpx").setLevel(logging.WARNING)

# ----------------------------
# Config
# ----------------------------
BOT_TOKEN = os.environ.get("BOT_TOKEN", "").strip()
DB_PATH = os.environ.get("DB_PATH", "bot.db").strip()
POLL_SECONDS = int(os.environ.get("POLL_SECONDS", "900"))  # 15 min

# RSS feeds (puedes añadir más si quieres)
FEEDS = [
    "https://www.gamerpower.com/rss",
    "https://www.gamerpower.com/rss/giveaways",
    "https://www.gamerpower.com/rss/steam",
    "https://www.gamerpower.com/rss/pc",
]

# Detección de tienda por patrones en título/enlace
STORE_PATTERNS: Dict[str, List[re.Pattern]] = {
    "epic":  [re.compile(r"\bepic\b", re.I), re.compile(r"epicgames", re.I)],
    "steam": [re.compile(r"\bsteam\b", re.I), re.compile(r"store\.steampowered\.com", re.I)],
    "gog":   [re.compile(r"\bgog\b", re.I), re.compile(r"gog\.com", re.I)],
    "prime": [re.compile(r"\bprime\b", re.I), re.compile(r"primegaming", re.I), re.compile(r"gaming\.amazon", re.I)],
}

DEFAULT_STORES = {"epic", "steam"}  # por defecto


# ----------------------------
# Helpers
# ----------------------------
def now_ts() -> int:
    return int(datetime.now(tz=timezone.utc).timestamp())


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip())


def detect_store(title: str, link: str) -> str:
    hay = f"{title} {link}"
    for store, pats in STORE_PATTERNS.items():
        if any(p.search(hay) for p in pats):
            return store
    return "otra"


def entry_key(entry) -> str:
    # clave estable para dedupe
    link = clean(entry.get("link", ""))
    guid = clean(entry.get("id", "")) or clean(entry.get("guid", ""))
    title = clean(entry.get("title", ""))
    return guid or link or title


def offer_keyboard(link: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[InlineKeyboardButton("🔗 Abrir oferta", url=link)]])


def format_message(title: str, store: str, link: str) -> str:
    store_name = store.upper() if store else "OTRA"
    return (
        f"🎁 <b>JUEGO GRATIS</b>\n"
        f"🏪 <b>Tienda:</b> {store_name}\n"
        f"🕹️ <b>Título:</b> {title}\n"
        f"🔗 {link}"
    )


# ----------------------------
# DB
# ----------------------------
async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                chat_id INTEGER PRIMARY KEY,
                stores_json TEXT NOT NULL,
                muted_until_ts INTEGER DEFAULT 0
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS sent_items (
                key TEXT PRIMARY KEY,
                first_seen_ts INTEGER NOT NULL
            )
        """)
        await db.commit()


async def ensure_user(db: aiosqlite.Connection, chat_id: int):
    cur = await db.execute("SELECT chat_id FROM users WHERE chat_id=?", (chat_id,))
    row = await cur.fetchone()
    if not row:
        await db.execute(
            "INSERT INTO users(chat_id, stores_json, muted_until_ts) VALUES(?,?,?)",
            (chat_id, json.dumps(sorted(list(DEFAULT_STORES))), 0),
        )


async def get_user_prefs(db: aiosqlite.Connection, chat_id: int) -> Tuple[Set[str], int]:
    await ensure_user(db, chat_id)
    cur = await db.execute("SELECT stores_json, muted_until_ts FROM users WHERE chat_id=?", (chat_id,))
    stores_json, muted_until = await cur.fetchone()
    stores = set(json.loads(stores_json or "[]"))
    return stores, int(muted_until or 0)


async def set_user_stores(db: aiosqlite.Connection, chat_id: int, stores: Set[str]):
    await ensure_user(db, chat_id)
    await db.execute(
        "UPDATE users SET stores_json=? WHERE chat_id=?",
        (json.dumps(sorted(list(stores))), chat_id),
    )


async def set_mute(db: aiosqlite.Connection, chat_id: int, muted_until_ts: int):
    await ensure_user(db, chat_id)
    await db.execute(
        "UPDATE users SET muted_until_ts=? WHERE chat_id=?",
        (muted_until_ts, chat_id),
    )


async def was_sent(db: aiosqlite.Connection, key: str) -> bool:
    cur = await db.execute("SELECT 1 FROM sent_items WHERE key=?", (key,))
    return (await cur.fetchone()) is not None


async def mark_sent(db: aiosqlite.Connection, key: str, ts: int):
    await db.execute(
        "INSERT OR IGNORE INTO sent_items(key, first_seen_ts) VALUES(?,?)",
        (key, ts),
    )


# ----------------------------
# Feed fetch
# ----------------------------
def fetch_items() -> List[Tuple[str, str, str, str]]:
    """
    Devuelve lista de (key, title, store, link)
    """
    items: List[Tuple[str, str, str, str]] = []
    for url in FEEDS:
        parsed = feedparser.parse(url)
        for e in (parsed.entries or [])[:50]:
            title = clean(e.get("title", ""))
            link = clean(e.get("link", ""))
            if not title or not link:
                continue
            store = detect_store(title, link)
            key = entry_key(e)
            items.append((key, title, store, link))
    return items


# ----------------------------
# Commands
# ----------------------------
async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    async with aiosqlite.connect(DB_PATH) as db:
        stores, muted_until = await get_user_prefs(db, chat_id)
        await db.commit()

    muted = muted_until > now_ts()
    stores_txt = ", ".join(sorted(s.upper() for s in stores)) if stores else "NINGUNA"

    await update.message.reply_text(
        "✅ Bot de juegos gratis activado.\n\n"
        f"Tiendas activas: {stores_txt}\n"
        f"Silenciado: {'Sí' if muted else 'No'}\n\n"
        "Comandos:\n"
        "/stores — ver tiendas\n"
        "/enable epic steam gog prime — activar\n"
        "/disable epic steam gog prime — desactivar\n"
        "/mute 1h|12h|24h — silenciar\n"
        "/unmute — quitar silencio\n"
        "/status — ver estado\n"
        "/free — ver gratis ahora mismo\n"
        "/forcecheck — revisar ahora y enviar lo nuevo\n"
        "/test — prueba\n"
    )


async def cmd_stores(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    available = ", ".join(sorted(STORE_PATTERNS.keys()))
    async with aiosqlite.connect(DB_PATH) as db:
        stores, _ = await get_user_prefs(db, chat_id)
        await db.commit()

    stores_txt = ", ".join(sorted(s.upper() for s in stores)) if stores else "NINGUNA"
    await update.message.reply_text(
        f"Tiendas activas: {stores_txt}\n"
        f"Disponibles: {available}\n\n"
        "Ejemplos:\n"
        "/enable epic steam\n"
        "/disable prime\n"
    )


async def cmd_enable(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    to_enable = set(s.lower() for s in context.args if s.lower() in STORE_PATTERNS)
    if not to_enable:
        await update.message.reply_text("Usa: /enable epic steam gog prime")
        return

    async with aiosqlite.connect(DB_PATH) as db:
        stores, _ = await get_user_prefs(db, chat_id)
        stores |= to_enable
        await set_user_stores(db, chat_id, stores)
        await db.commit()

    await update.message.reply_text(f"✅ Activadas: {', '.join(sorted(to_enable)).upper()}")


async def cmd_disable(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    to_disable = set(s.lower() for s in context.args if s.lower() in STORE_PATTERNS)
    if not to_disable:
        await update.message.reply_text("Usa: /disable epic steam gog prime")
        return

    async with aiosqlite.connect(DB_PATH) as db:
        stores, _ = await get_user_prefs(db, chat_id)
        stores -= to_disable
        await set_user_stores(db, chat_id, stores)
        await db.commit()

    await update.message.reply_text(f"✅ Desactivadas: {', '.join(sorted(to_disable)).upper()}")


async def cmd_mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    arg = (context.args[0] if context.args else "").lower()
    seconds = {"1h": 3600, "12h": 12 * 3600, "24h": 24 * 3600}.get(arg, 0)
    if not seconds:
        await update.message.reply_text("Usa: /mute 1h | 12h | 24h")
        return

    until = now_ts() + seconds
    async with aiosqlite.connect(DB_PATH) as db:
        await set_mute(db, chat_id, until)
        await db.commit()

    await update.message.reply_text(f"🔕 Silenciado durante {arg}.")


async def cmd_unmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    async with aiosqlite.connect(DB_PATH) as db:
        await set_mute(db, chat_id, 0)
        await db.commit()
    await update.message.reply_text("🔔 Silencio quitado.")


async def cmd_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot OK. Usa /free o /forcecheck.")


async def cmd_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    async with aiosqlite.connect(DB_PATH) as db:
        stores, muted_until = await get_user_prefs(db, chat_id)
        await db.commit()

    muted = muted_until > now_ts()
    stores_txt = ", ".join(sorted(s.upper() for s in stores)) if stores else "NINGUNA"
    await update.message.reply_text(
        "📌 Estado\n"
        f"Tiendas: {stores_txt}\n"
        f"Silenciado: {'Sí' if muted else 'No'}\n"
        f"Intervalo: {POLL_SECONDS}s\n"
        f"Feeds: {len(FEEDS)}"
    )


async def cmd_free(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Lista lo que está gratis AHORA MISMO (sin dedupe).
    No marca como enviado y no depende del historial.
    """
    chat_id = update.effective_chat.id
    await update.message.reply_text("🎁 Buscando juegos gratis ahora mismo…")

    items = fetch_items()
    if not items:
        await update.message.reply_text("No he encontrado items en los feeds.")
        return

    async with aiosqlite.connect(DB_PATH) as db:
        stores, muted_until = await get_user_prefs(db, chat_id)
        await db.commit()

    # Si está silenciado, igual dejamos consultar /free (es una consulta manual).
    

    filtered = [(title, store, link) for _, title, store, link in items if store in stores]

    if not filtered:
        await update.message.reply_text("No hay ofertas en tus tiendas activas. Usa /stores para revisarlas.")
        return

    MAX_ITEMS = 15
    filtered = filtered[:MAX_ITEMS]

    lines = []
    for title, store, link in filtered:
        lines.append(f"• <b>{title}</b> ({store.upper()})\n{link}")

    msg = "🎁 <b>Gratis ahora mismo</b>\n\n" + "\n\n".join(lines)
    await update.message.reply_text(
        msg,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True
    )

    if len(items) > MAX_ITEMS:
        await update.message.reply_text(
            f"ℹ️ Hay más ofertas en el feed, pero te muestro solo {MAX_ITEMS}."
        )


async def cmd_forcecheck(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Revisa AHORA y envía solo lo que sea nuevo según dedupe (sent_items).
    """
    chat_id = update.effective_chat.id
    await update.message.reply_text("🔎 Revisando ofertas ahora mismo…")

    items = fetch_items()
    if not items:
        await update.message.reply_text("No he encontrado items en los feeds.")
        return

    async with aiosqlite.connect(DB_PATH) as db:
        stores, muted_until = await get_user_prefs(db, chat_id)

        # Si está silenciado, no enviamos (pero /free sí funciona).
        if muted_until > now_ts():
            await update.message.reply_text("🔕 Estás silenciado. Usa /unmute.")
            return

        sent_count = 0
        skipped_sent = 0
        skipped_store = 0

        for key, title, store, link in items:
            if store not in stores:
                skipped_store += 1
                continue

            if await was_sent(db, key):
                skipped_sent += 1
                continue

            text = format_message(title, store, link)
            await context.bot.send_message(
                chat_id=chat_id,
                text=text,
                parse_mode=ParseMode.HTML,
                reply_markup=offer_keyboard(link),
                disable_web_page_preview=False,
            )
            await mark_sent(db, key, now_ts())
            sent_count += 1

        await db.commit()

    await update.message.reply_text(
        "✅ Forcecheck terminado.\n"
        f"Enviados: {sent_count}\n"
        f"Omitidos (ya enviados): {skipped_sent}\n"
        f"Omitidos (tienda no activa): {skipped_store}"
    )


# ----------------------------
# Background poller
# ----------------------------
async def poll_and_notify(app: Application):
    """
    Revisa feeds cada POLL_SECONDS y notifica a usuarios según sus preferencias.
    Dedup global: no repite un item ya enviado anteriormente a nadie.
    """
    while True:
        try:
            items = fetch_items()
            if items:
                ts = now_ts()
                async with aiosqlite.connect(DB_PATH) as db:
                    cur = await db.execute("SELECT chat_id, stores_json, muted_until_ts FROM users")
                    users = await cur.fetchall()

                    for key, title, store, link in items:
                        if await was_sent(db, key):
                            continue

                        sent_any = False
                        for chat_id, stores_json, muted_until in users:
                            if int(muted_until or 0) > ts:
                                continue

                            stores = set(json.loads(stores_json or "[]"))
                            if store not in stores:
                                continue

                            text = format_message(title, store, link)
                            try:
                                await app.bot.send_message(
                                    chat_id=int(chat_id),
                                    text=text,
                                    parse_mode=ParseMode.HTML,
                                    reply_markup=offer_keyboard(link),
                                    disable_web_page_preview=False,
                                )
                                sent_any = True
                            except Exception as ex:
                                log.warning("No pude enviar a %s: %s", chat_id, ex)

                        if sent_any:
                            await mark_sent(db, key, ts)

                    await db.commit()

        except Exception as e:
            log.exception("Error en polling: %s", e)

        await asyncio.sleep(POLL_SECONDS)


async def on_startup(app: Application):
    await init_db()
    app.create_task(poll_and_notify(app))
    log.info("Bot arrancado. Poll cada %ss. Feeds=%s", POLL_SECONDS, len(FEEDS))


def main():
    if not BOT_TOKEN:
        raise SystemExit("Falta BOT_TOKEN en variables de entorno.")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("stores", cmd_stores))
    app.add_handler(CommandHandler("enable", cmd_enable))
    app.add_handler(CommandHandler("disable", cmd_disable))
    app.add_handler(CommandHandler("mute", cmd_mute))
    app.add_handler(CommandHandler("unmute", cmd_unmute))
    app.add_handler(CommandHandler("test", cmd_test))
    app.add_handler(CommandHandler("status", cmd_status))
    app.add_handler(CommandHandler("free", cmd_free))
    app.add_handler(CommandHandler("forcecheck", cmd_forcecheck))

    app.post_init = on_startup
    app.run_polling(close_loop=False)


if __name__ == "__main__":
    main()


