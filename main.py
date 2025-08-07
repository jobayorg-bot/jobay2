import logging
import os
from aiogram import Bot, Dispatcher, types, executor

#اینجا نباید هیچ توکنی بنویسی مهندس همشو باید توی سرور اپلود کنی 
#########################################################################
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
#########################################################################
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
        await bot.send_message(chat_id=int(user_id), text=f"📩 جواب ادمین :
{reply_msg}")
        await message.reply("✅پیغام ارسال شد مهندس")
    except Exception as e:
        await message.reply(f"❌ مهندس خطا در ارسال پیام داریم !{e}")

@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def forward_message(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        return  # پیام‌های ادمین رو فوروارد نکن
    user = message.from_user
    msg = (
        f"📩 پیام ناشناس:
"
        f"🧑‍💬 نام: {user.first_name}
"
        f"🔗 یوزرنیم: @{user.username or 'ندارد'}
"
        f"🆔 آیدی عددی: {user.id}
"
        f"📝 پیام: {message.text}

"
        f"برای پاسخ:
/reply {user.id} پیام شما"
    )
    await bot.send_message(chat_id=ADMIN_ID, text=msg)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
