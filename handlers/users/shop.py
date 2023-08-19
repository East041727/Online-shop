from loader import dp,db
from aiogram import types
from keyboards.default.main import get_category_markup
from states.main import ShopState


@dp.message_handler(text='🛍 Katalog')
async def get_catalog(message: types.Message):
    markup = await get_category_markup()
    await message.answer("Kerakli kategoriyani tanglang",reply_markup=markup )
    await ShopState.category.set()