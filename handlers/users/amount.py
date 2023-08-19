from loader import db,dp
from states.main import ShopState
from aiogram import types
from aiogram.dispatcher import FSMContext 
from keyboards.default.main import get_category_markup


@dp.message_handler(lambda message: message.text.isdigit(),state=ShopState.amount)
async def get_amount(message: types.Message, state:FSMContext):
    data =await state.get_data()
    product_id =data.get('product_id')
    user = await db.select_user(telegram_id=message.from_user.id)
    user_id = user['id']

    await message.answer(f"{message.text} ta mahsulot savatingizga qo'shildi !")
    
    
    cart_item = await db.select_cart_product(user_id=user_id, product_id=product_id)
   
    if cart_item:
         await db.update_product_to_cart(user_id=user_id, product_id=product_id,amount= cart_item['amount'] + int(message.text))
        
  
    else:
        await db.add_product_to_cart(user_id=user_id,product_id=product_id, amount=int(message.text))
    
    markup = await get_category_markup()
    await message.answer("Ushbu kategoriyalardan birini tanglang", reply_markup=markup)
    await ShopState.category.set()
    
