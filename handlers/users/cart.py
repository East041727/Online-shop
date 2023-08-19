from loader import db,dp

from aiogram import types

from states.main import ShopState

from keyboards.default.main import cart_items_markup,get_category_markup



async def get_cart_info(cart_item):
    total_price = 0
    msg =f'📥 Sizning savatda: \n\n  '
    products = [] 
    for item in cart_item:
          product_id = item['product_id']
          product = await db.select_product(id=product_id)
          result =item['amount'] * product['price']
          total_price+=result
          products.append(product['name'])
          msg += f"{product['name']}\n{item['amount']} x {product['price']} = {result} so'm \n" 
    markup = await cart_items_markup(products=products)
    msg +=f"\n\nUmumiy summa: {total_price} so'm"
    return msg,markup,total_price



@dp.message_handler(text = '📥 Savat', state="*")
async def get_cart_item(message: types.Message):
    user =await db.select_user(telegram_id=message.from_user.id)
    cart_item = await db.select_all_cart_itmes(user_id=user['id'])
    if cart_item:
   
     msg, markup, total_price = await get_cart_info(cart_item=cart_item)
     await message.answer("❌ Mahsulot nomi - savatdan o'chirish \n 🔗 Tozalash - savatni butunlay tozalash ")
     await message.answer(text=msg, reply_markup=markup)
     await ShopState.cart.set()
    else: 
        await message.answer("Sizning savatingiz hozircha bo'sh !!! ")









@dp.message_handler(lambda message: "❌" in message.text,  state=ShopState.cart)
async def delete_cart_items(message: types.Message):
    user =await db.select_user(telegram_id=message.from_user.id)
    product_name = " ".join(message.text.split()[1:-1])
    product = await db.select_product(name=product_name)
    await db.delete_cart(product_id= product["id"], user_id =user["id"] )
    cart_item = await db.select_all_cart_itmes(user_id=user['id'])
    if cart_item:
     
          msg, markup, total_price = await get_cart_info(cart_item=cart_item)
          await message.answer(" ❌  Mahsulot nomi  - savatdan o'chirish \n  🔗  Tozalash- savatni butunlay tozalash ")
          await message.answer(msg,reply_markup=markup)
          await ShopState.cart.set()
    else: 
        markup = await  get_category_markup()
        await message.answer("Afsuski savatingiz hozircha bo'shab qoldi !!! ", reply_markup=markup)
        await ShopState.category.set()



