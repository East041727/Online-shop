from loader import dp,db
from aiogram import types
from keyboards.default.main import get_category_markup,get_product_markup,get_phone_number
from states.main import ShopState


@dp.message_handler(state=ShopState.cart)
@dp.message_handler(state=ShopState.category)
async def get_products(message: types.Message):
    category = await db.select_category(name=message.text)
    if category:
       
        products = await db.select_products_by_category(cat_id =category['id'])
        if products:
            markup = await get_product_markup(products=products)
            await message.answer(f"{category['name']} bo'limidan kerakli mahsulotni tanglang",reply_markup=markup)
            await ShopState.next()
        else: 
            await message.answer(f"{category['name'] } bu kategoriyada mahsulot mavjud emas")
            await message.answer('😭')
    else:
        markup = await get_category_markup()
      
        await message.answer("Rasmiylashtirish qismiga o'tdingiz ", reply_markup= markup)
      


