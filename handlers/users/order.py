from loader import dp,db
from aiogram import types
from states.main import ShopState
from handlers.users.cart import get_cart_info,get_category_markup
from keyboards.default.main import get_phone_number,get_location,main_markup
from aiogram.dispatcher import FSMContext



@dp.message_handler(text="🛒 Rasmiylashtirish",  state="*")
async def make_order(message: types.Message, state: FSMContext):

    user = await db.select_user(telegram_id=message.from_user.id)
    cart_item = await db.select_all_cart_itmes(user_id=user["id"])
    if cart_item:
        markup_in = await get_phone_number()
        mega = await get_cart_info(cart_item=cart_item)
        await state.update_data(data={'total_price': mega[2]})
        await message.answer(text=mega[0], reply_markup=markup_in)
        await ShopState.phone.set()
    else: 
        markup = await get_category_markup()
        await message.answer("Uzr siz buyurtma qila olmaysiz chunki savatingiz bo'sh, savatingizga biror narsa qo'shing !!! ",reply_markup=markup)
        await ShopState.category.set()
        


@dp.message_handler(content_types=["contact"], state=ShopState.phone)
async def get_phone_number_to_add_to_cart(message: types.Message, state: FSMContext):
    phone = message.contact.phone_number
    await state.update_data(data={'phone':phone})
    salom = await get_location()
    await message.answer("Joriy joylashuvingizni kiriting", reply_markup=salom)
    await ShopState.joylashuv.set()




@dp.message_handler(content_types=['location'], state=ShopState.joylashuv)
async def get_location_to_cart(message: types.Message, state: FSMContext ):
    data = await state.get_data()
    user = await db.select_user(telegram_id=message.from_user.id)
    total_price = data.get('total_price')
    phone = data.get('phone')
    lat = message.location.latitude
    lon = message.location.longitude
    orders= await db.select_all_orders(user_id=user['id'])
    print(orders)
    order_id = orders['id']
    print(order_id)
    cart_item = await db.select_all_cart_itmes(user_id=user["id"])
    for item in cart_item:
        product_id = item['product_id']
        amount = item['amount']
        await db.add_order_product(order_id=order_id, product_id=product_id, amount=amount)
    await db.delete_cart_everything(user_id=user['id'])    
    await db.add_order(user_id=user['id'],phone_number=phone, lat=str(lat), lon=str(lon), total_price=total_price,paid=False)
    await message.answer("Buyurtmangiz saqlandi tez orada siz bilan bog'lanamiz",reply_markup=main_markup)
    await state.finish()


