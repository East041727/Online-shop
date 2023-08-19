from aiogram import types

from loader import dp, db, bot
from data.config import ADMINS
from utils.extra_datas import make_title
from keyboards.default.main import main_markup
from states.main import taklifstate,ShopState
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import ReplyKeyboardRemove






@dp.message_handler(text='✍️ Taklif')
async def taklif(message: types.Message):
    await message.answer('Taklif yoki shikoyatingizni yozing 👇', reply_markup= ReplyKeyboardRemove())
    await taklifstate.taklif.set()


@dp.message_handler(state=taklifstate.taklif)
async def shikoyat(message: types.Message, state:FSMContext):
    username = message.from_user.username
    
     
    full_name = message.from_user.full_name

    takliff = message.text
    if username:
        await bot.send_message(chat_id=6456590794, text=f'<b>Taklif:</b>\n\n<b>Kimdan:  </b> @{username}\n<b>\n\n </b> <i>{takliff}</i>', reply_markup=ReplyKeyboardRemove())
        await message.answer('Rahmat taklif yoki shikoyatingiz qabul qilindi !',reply_markup= main_markup)
        await state.finish()
  
    else:
        await bot.send_message(chat_id=6456590794, text=f'<b>Taklif:</b>\n\n<b>Kimdan:  </b> {full_name}\n<b> \n\n </b> <i>{takliff}</i>', reply_markup=ReplyKeyboardRemove())
        await message.answer('Rahmat taklif yoki shikoyatingiz qabul qilindi !',reply_markup= main_markup)
        await state.finish()