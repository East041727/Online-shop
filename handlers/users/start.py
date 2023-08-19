from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from loader import dp, db, bot
from data.config import ADMINS
from aiogram.dispatcher import FSMContext
from utils.extra_datas import make_title
from keyboards.default.main import main_markup

@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: types.Message,state:FSMContext):
    await state.finish()

    full_name = message.from_user.full_name
    user = await db.select_user(telegram_id=message.from_user.id)
    if user is None:
        user = await db.add_user(
            telegram_id=message.from_user.id,
            full_name=full_name,
            username=message.from_user.username,
        )
        # ADMINGA xabar beramiz
        count = await db.count_users()
        msg = f"[{make_title(user['full_name'])}](tg://user?id={user['telegram_id']}) bazaga qo'shildi\.\nBazada {count} ta foydalanuvchi bor\."
        await bot.send_message(chat_id=6456590794, text=msg, parse_mode=types.ParseMode.MARKDOWN_V2)
    else:
        await bot.send_message(chat_id=ADMINS[0], text=f"[{make_title(full_name)}](tg://user?id={message.from_user.id}) bazaga oldin qo'shilgan", disable_web_page_preview=True, parse_mode=types.ParseMode.MARKDOWN_V2)
    await message.answer(f"Xush kelibsiz\! {make_title(full_name)}", parse_mode=types.ParseMode.MARKDOWN_V2,reply_markup=main_markup)
   
