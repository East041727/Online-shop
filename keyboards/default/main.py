from aiogram.types import ReplyKeyboardMarkup,KeyboardButton
from loader import db,dp



buttons_in_first = [ '🛍 Katalog',  ' ✍️ Taklif', '📥 Savat','🛒 Rasmiylashtirish' ]

main_markup = ReplyKeyboardMarkup(resize_keyboard=True)

back_button = KeyboardButton(text='⬅️ Orqaga')
home = KeyboardButton(text='🏠 Home')
cart = KeyboardButton(text='🛒 Rasmiylashtirish')
check = KeyboardButton(text='📥 Savat')
clear_button = KeyboardButton(text='♻️ Tozalash')

for item in buttons_in_first:
    main_markup.insert(KeyboardButton(text=item))


async def get_category_markup():
    categories = await db.select_all_categories()
    markup = ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
    for category in categories:
        markup.insert(KeyboardButton(text=category['name']))
    markup.add(check)
    markup.add(back_button,home)
    return markup



async def get_product_markup(products):
     markup = ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
     for product in products:
        markup.insert(KeyboardButton(text=product['name']))
     markup.add(check)
     markup.add(back_button,home)
     return markup






async def get_phone_number():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(KeyboardButton(text='📞 Telefon raqamni tasdiqlang',request_contact=True))

    return markup


async def get_location():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(KeyboardButton(text=' 📍 Joylashuvingizni  tasdiqlang',request_location=True))
    return markup
    








async def numbers_markup(number=9):
    markup = ReplyKeyboardMarkup(resize_keyboard=True,row_width=3)
    for i in range(1,number+1):
        markup.insert(KeyboardButton(text=str(i)))
    markup.add(check,back_button)
    return markup



async def cart_items_markup(products):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for product in products:
        markup.insert(KeyboardButton(text=f"❌ {product} ❌"))
    markup.add(clear_button)
    markup.add(back_button)
    return markup