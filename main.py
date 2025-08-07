import logging
import os
from aiogram import Bot, Dispatcher, types, executor
#اینجا هیچ چیزو تغییر نده توکن و ایدیتو باید توی رندر یا سرور اضافه کنی 
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.reply("سلام ! پیامت چیه ؟")

@dp.message_handler(commands=["reply"])
async def reply(message: types.Message):
    args = message.get_args()
    if not args or len(args.split()) < 2:
        await message.reply("فرمت درست : /reply user_id (پیغام شما )")
        return
    try:
        user_id, *reply_text = args.split()
        reply_msg = " ".join(reply_text)
        await bot.send_message(chat_id=int(user_id), text=f"📩 جواب ادمین:\n{reply_msg}")
        await message.reply("✅پیغام ارسال شد مهندس")
    except Exception as e:
        await message.reply(f"❌ مهندس خطا در ارسال پیام داریم ! {e}")

@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def forward_message(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        return
    user = message.from_user
    msg = (
        f"📩 پیام ناشناس:\n"
        f"🧑‍💬 نام: {user.first_name}\n"
        f"🔗 یوزرنیم: @{user.username or 'ندارد'}\n"
        f"🆔 آیدی عددی: {user.id}\n"
        f"📝 پیام: {message.text}\n\n"
        f"برای پاسخ:\n/reply {user.id} پیام شما"
    )
    await bot.send_message(chat_id=ADMIN_ID, text=msg)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
#code by jobay
