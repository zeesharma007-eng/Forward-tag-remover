from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
import os

BOT_TOKEN = os.getenv("8547575945:AAEklJWLQ8Hml-dzGXY4_ObMEpnYFKyQ9-0")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# Store channel IDs (string format)
sources = set()
destinations = set()

# ---------- START ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✅ Auto Channel Copy Bot\n\n"
        "• Multiple source channels\n"
        "• Multiple destination channels\n"
        "• No sender tag\n"
        "• Inline buttons remain\n\n"
        "Add me as admin in channels.\n"
        "Use admin commands to manage channels."
    )

# ---------- ADMIN CHECK ----------
def is_admin(update):
    return update.effective_user.id == ADMIN_ID

# ---------- COMMANDS ----------
async def addsource(update, context):
    if not is_admin(update): return
    if not context.args:
        return await update.message.reply_text("Usage:\n/addsource -100xxxxxxxxxx")

    cid = context.args[0]
    sources.add(cid)
    await update.message.reply_text(f"✅ Source added:\n{cid}")

async def removesource(update, context):
    if not is_admin(update): return
    cid = context.args[0]
    sources.discard(cid)
    await update.message.reply_text(f"❌ Source removed:\n{cid}")

async def adddest(update, context):
    if not is_admin(update): return
    if not context.args:
        return await update.message.reply_text("Usage:\n/adddest -100xxxxxxxxxx")

    cid = context.args[0]
    destinations.add(cid)
    await update.message.reply_text(f"✅ Destination added:\n{cid}")

async def removedest(update, context):
    if not is_admin(update): return
    cid = context.args[0]
    destinations.discard(cid)
    await update.message.reply_text(f"❌ Destination removed:\n{cid}")

async def listsource(update, context):
    if not is_admin(update): return
    await update.message.reply_text(
        "📥 Source Channels:\n" + ("\n".join(sources) if sources else "None")
    )

async def listdest(update, context):
    if not is_admin(update): return
    await update.message.reply_text(
        "📤 Destination Channels:\n" + ("\n".join(destinations) if destinations else "None")
    )

# ---------- AUTO COPY (INLINE BUTTONS KEPT) ----------
async def channel_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.channel_post:
        return

    source_id = str(update.channel_post.chat.id)
    if source_id not in sources:
        return

    for dest in destinations:
        try:
            await context.bot.copy_message(
                chat_id=dest,
                from_chat_id=update.channel_post.chat.id,
                message_id=update.channel_post.message_id
                # copyMessage keeps inline buttons & removes sender tag
            )
        except Exception as e:
            pass

# ---------- MAIN ----------
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("addsource", addsource))
    app.add_handler(CommandHandler("removesource", removesource))
    app.add_handler(CommandHandler("adddest", adddest))
    app.add_handler(CommandHandler("removedest", removedest))
    app.add_handler(CommandHandler("listsource", listsource))
    app.add_handler(CommandHandler("listdest", listdest))
    app.add_handler(MessageHandler(filters.UpdateType.CHANNEL_POST, channel_post))

    app.run_polling()

if __name__ == "__main__":
    main()
                       
