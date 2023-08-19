from loader import dp,db
from aiogram import types
from keyboards.default.main import get_category_markup,get_product_markup,numbers_markup
from states.main import ShopState
from aiogram.dispatcher import FSMContext






@dp.message_handler(state=ShopState.product)
async def send_product(message: types.Message, state:FSMContext):

    product = await db.select_product(name=message.text)
    await state.update_data(data={'cat_id': product['cat_id'], 'product_id': product['id']})
    markup =await numbers_markup()
    image = product['image']
    caption = f"<b>{product['name']}</b> ({product['amount']} ta mavjud.)  - <i> {product['price']} so'm </i> <b> \n\n{product['description']} </b>"
    await message.answer_photo(photo=image, caption=caption,reply_markup=markup)
    await ShopState.next()
