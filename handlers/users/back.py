from loader import dp,db
from aiogram import types
from states.main import ShopState
from aiogram.dispatcher import FSMContext
from keyboards.default.main import main_markup,get_category_markup,get_product_markup

@dp.message_handler(text='🏠 Home',state="*")
@dp.message_handler(text='⬅️ Orqaga',state=ShopState.category)
@dp.message_handler(text='⬅️ Orqaga',state=ShopState.cart)

async def main_return(message: types.Message,state: FSMContext):

    await message.answer("Siz asosiy menyuga qaytdingiz kerakli bo'limni tanglang",reply_markup=main_markup)
    await state.finish()



@dp.message_handler(text='⬅️ Orqaga',state=ShopState.product)
async def rediret_category(message: types.Message):
    markup = await get_category_markup()
    await message.answer("Kerakli kategoriyani tanglang",reply_markup=markup )
    await ShopState.category.set()
    
@dp.message_handler(text='⬅️ Orqaga',state=ShopState.amount)
async def product_rediredct(message: types.Message, state: FSMContext):
    data = await state.get_data()
    salom = data.get('cat_id')

    products = await db.select_products_by_category(cat_id = salom)

    markup = await get_product_markup(products=products)
    await message.answer("Ushbu bo'limdan kerakli mahsulotni tanglang",reply_markup=markup)
    await ShopState.product.set()




@dp.message_handler(text='♻️ Tozalash',state=ShopState.cart)
async def clear_items(message: types.Message):
    user = await db.select_user(telegram_id=message.from_user.id)
    await db.delete_cart_everything(user_id=user['id'])
    markup = await  get_category_markup()
    await message.answer("Sizning savatingiz bo'shatildi !!! ",reply_markup=markup)
    await ShopState.category.set()

