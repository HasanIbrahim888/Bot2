import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext
import subprocess

CHANNEL_USERNAME = "@sino2500"
DEVELOPER_NAME = "Eng.hasan.Ib"

async def check_subscription(user_id, context):
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

async def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if not await check_subscription(user_id, context):
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("اشترك في القناة", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")]])
        await update.message.reply_text("يجب عليك الاشتراك في القناة أولاً لاستخدام البوت.", reply_markup=keyboard)
        return
    await update.message.reply_text("أرسل رابط فيديو أو صورة من Instagram أو Facebook...")

async def about(update: Update, context: CallbackContext):
    await update.message.reply_text(f"تم تطوير هذا البوت بواسطة {DEVELOPER_NAME}.")

async def download_media(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if not await check_subscription(user_id, context):
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("اشترك في القناة", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")]])
        await update.message.reply_text("يجب عليك الاشتراك في القناة أولاً لاستخدام البوت.", reply_markup=keyboard)
        return

    url = update.message.text
    await update.message.reply_text("جارٍ التحميل...")

    try:
        output = subprocess.check_output(['yt-dlp', '-f', 'best', '-o', 'downloaded.%(ext)s', url])
        for ext in ['mp4', 'webm', 'mkv', 'mp3', 'jpg', 'png']:
            file_path = f"downloaded.{ext}"
            if os.path.exists(file_path):
                await update.message.reply_document(document=open(file_path, 'rb'))
                os.remove(file_path)
                return
        await update.message.reply_text("لم أتمكن من تحميل الوسائط.")
    except Exception as e:
        await update.message.reply_text(f"حدث خطأ: {e}")

if __name__ == '__main__':
    TOKEN = os.getenv("TOKEN")
    if not TOKEN:
        print("خطأ: لم يتم تعيين التوكن في المتغير البيئي TOKEN")
        exit(1)
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_media))

    app.run_polling()
