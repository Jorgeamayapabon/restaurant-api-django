import django
import os
import json
os.environ['DJANGO_SETTINGS_MODULE'] = 'restaurant.settings'
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from products.models import Category, Product

TELEGRAM_URL = "https://api.telegram.org/bot"
BOT_TOKEN = "5997463720:AAG_WMB8BOoX97cRc5AE5bfwWZS9N3QFe60"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

OTHERS, CHOICES, PRODUCTS, CART, AMOUNT, SHOPPING= range(6)

literal_start = "^(Start|Inicio)$"
literal_done = "^(Leave|Salir)$"
literal_back = "^(Back|Atras)$"
literal_languaje = "^(Español|English)$"
literal_menu = "^(Ver Menú|Menu)$"
literal_amount = "^(Si|No|Yes)$"
literal_shopping_add = "^(Añadir Producto|Agregar|Add Product|Add)$"
literal_shopping_buy = "^(Comprar|Pagado|Ver Carrito|Borrar|Buy|Paid|Cart|Delete)$"

categories_name = []
categories_num = []
products_category = []

categories = {}
products_selections = {}
category_and_product = {}
shopping_cart = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the conversation, display any stored data and ask user for input."""
    reply_keyboard = [
        ["Español"],
        ["English"],
        ["Salir"],
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard)
    
    reply_text = f"Hi welcome to your Restaurant {update.effective_user.full_name}, select a language.\n"
    await update.message.reply_text(reply_text, reply_markup=markup)

    return OTHERS

async def languaje_selected(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    global data
    text = update.message.text
    if text.lower() == "español":
        with open("./languages/es/botConversation.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    elif text.lower() == "english":
        with open("./languages/en/botConversation.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    reply_text = f"{data['start']['message1']} {update._effective_user.full_name}, {data['start']['message2']}"
    reply_keyboard = [data['start']['reply_keyboard']]
    markup = ReplyKeyboardMarkup(reply_keyboard)
    await update.message.reply_text(reply_text, reply_markup=markup)
    return CHOICES


async def ver_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for info about the selected predefined choice."""
    category_objs = Category.objects.all()
    categories.clear()
    categories_name.clear()
    reply_text = f"{data['menu']['message']}:\n"
    reply_keyboard_category = [categories_name, data['menu']['keyboard_item']]
    for model_obj in category_objs:
        categories.update({model_obj.category_name: model_obj.id})
        categories_name.append(model_obj.category_name)
    for i in range(0,len(categories_name)):
        categories_num.append(str(i+1))
        reply_text += f"{i+1}. {categories_name[i]}.\n"
    category_markup = ReplyKeyboardMarkup(reply_keyboard_category)
    await update.message.reply_text(reply_text, reply_markup=category_markup)
    return PRODUCTS


async def products(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    product_objs = Product.objects.all()
    products_category.clear()
    products_selections.clear()
    d_prod = data['products']
    txt = d_prod['text']
    if text.upper() in categories_name:
        reply_text = f"{d_prod['message1']} {text}:\n"
        for model_obj in product_objs:
            if model_obj.category.id == categories[text]:
                reply_text += f"\n{txt[0]}: {model_obj.product_name} \n"
                reply_text += f"{txt[1]}: {model_obj.description} \n"
                reply_text += f"{txt[2]}: {model_obj.price} \n"
                reply_text += f"{txt[3]}: {model_obj.amount} {txt[4]}\n"
                products_category.append(model_obj.product_name)
                products_selections.update({
                    model_obj.product_name:{
                        "category_name": model_obj.category.category_name,
                        "product_name": model_obj.product_name,
                        "description": model_obj.description,
                        "price": model_obj.price,
                        "amount": model_obj.amount
                    }
                })
        reply_text += f"\n{d_prod['message2']}"
        reply_keyboard_finish = [products_category, d_prod["keyboard_item"]]
        markup = ReplyKeyboardMarkup(reply_keyboard_finish)
        await update.message.reply_text(reply_text, reply_markup=markup)
        return CART
    elif text.lower() == "otros" or text.lower() == "others":
        reply_text = f"{d_prod['message3']}:\n"
        reply_keyboard_others = d_prod['reply_keyboard']
        markup = ReplyKeyboardMarkup(reply_keyboard_others)
        await update.message.reply_text(reply_text, reply_markup=markup)
        return OTHERS


async def cart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    product_selected = text
    selections_dict = products_selections[product_selected]
    amount = 1
    d_cart = data['cart']
    category_and_product.update({'selection': selections_dict["category_name"] + " " + product_selected})
    # if category_and_product['selection'] in shopping_cart.keys():
        # shopping_cart[category_and_product['selection']]["amount"] += 1
    # else:
    shopping_cart.update({
        category_and_product['selection']: {
            "amount": amount,
            "selections_dict": selections_dict
        }
    })
    reply_text = f"{d_cart['message1']} {selections_dict['category_name']} {d_cart['message2']} {product_selected} {d_cart['message3']}.\n\n"
    reply_text += f"{d_cart['message4']} {amount}.\n\n{d_cart['message5']}"
    reply_keyboard_shopping = d_cart['reply_keyboard']
    markup = ReplyKeyboardMarkup(reply_keyboard_shopping)
    await update.message.reply_text(reply_text, reply_markup=markup)
    return AMOUNT


async def amount_product(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    
    d_amount = data['amount']
    text = update.message.text
    reply_keyboard_shopping = d_amount['reply_keyboard']
    if text.lower() == "si" or text.lower() == "yes":
        reply_text = f"{d_amount['message1']}"
        await update.message.reply_text(reply_text, reply_markup=ReplyKeyboardRemove())
        return AMOUNT
    elif text.lower() == "no":
        reply_text = f"{d_amount['message2']}.\n\n{d_amount['message3']}"
        markup = ReplyKeyboardMarkup(reply_keyboard_shopping)
        await update.message.reply_text(reply_text, reply_markup=markup)
        return SHOPPING
    elif text.isdigit():
        _category_product = category_and_product['selection']
        shopping_cart[_category_product]['amount'] = int(text)
        reply_text = f"{d_amount['message4']} {text} {d_amount['message3']}.\n\n"
        markup = ReplyKeyboardMarkup(reply_keyboard_shopping)
        await update.message.reply_text(reply_text, reply_markup=markup)
        return SHOPPING


async def buy_products(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    d_buy = data['buy']
    if text.lower() == "comprar" or text.lower() == "buy":
        reply_text = d_buy['message1']
        reply_keyboard_shopping = d_buy['reply_keyboard1']
        markup = ReplyKeyboardMarkup(reply_keyboard_shopping)
        await update.message.reply_text(reply_text, reply_markup=ReplyKeyboardRemove())
        await update.message.reply_text(show_shopping_cart(), reply_markup=markup)
        return SHOPPING
    elif text.lower() == "pagado" or text.lower() == "paid":
        reply_text = d_buy['message2']
        shopping_cart.clear()
        await update.message.reply_text(reply_text, reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
    elif text.lower() == "ver carrito" or text.lower() == "cart":
        await update.message.reply_text(show_shopping_cart(), reply_markup=ReplyKeyboardRemove())
        reply_text = d_buy['message3']
        reply_keyboard_shopping = d_buy['reply_keyboard2']
        markup = ReplyKeyboardMarkup(reply_keyboard_shopping)
        await update.message.reply_text(reply_text, reply_markup=markup)
        return SHOPPING
    elif text.lower() == "borrar" or text.lower() == "delete":
        reply_text = d_buy['message4']
        reply_keyboard_shopping = [list(shopping_cart.keys())]
        markup = ReplyKeyboardMarkup(reply_keyboard_shopping)
        await update.message.reply_text(reply_text, reply_markup=markup)
        return SHOPPING
    elif text in list(shopping_cart.keys()):
        shopping_cart.pop(text)
        reply_text = f"{d_buy['message5']} {text} {d_buy['message6']}"
        reply_keyboard_shopping = d_buy['reply_keyboard3']
        markup = ReplyKeyboardMarkup(reply_keyboard_shopping)
        await update.message.reply_text(reply_text, reply_markup=markup)
        return SHOPPING


async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Display the gathered info and end the conversation."""
    d_done = data['done']
    if "choice" in context.user_data:
        del context.user_data["choice"]

    await update.message.reply_text(
        d_done['message1'],
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END


def show_shopping_cart() -> str:
    d_show = data['show']
    reply_text = d_show['message1']
    total_price = 0
    for product in list(shopping_cart.values()):
        total_price += product["amount"]*product["selections_dict"]["price"]
        category_namer = product["selections_dict"]["category_name"]
        product_namer = product["selections_dict"]["product_name"]
        pricer = product["selections_dict"]["price"]
        reply_text += f"{d_show['message2']} {category_namer}\n{d_show['message3']}: {product_namer}\n{d_show['message4']}: {pricer}\n{d_show['message5']}: {product['amount']}\n\n"
    reply_text += f"\n{d_show['message6']}: ${total_price}"
    return reply_text


if __name__ == '__main__':

    application = Application.builder().token(BOT_TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            OTHERS:[
                MessageHandler(filters.Regex(literal_start), start),
                MessageHandler(filters.Regex(literal_back), products),
                MessageHandler(filters.Regex(literal_languaje), languaje_selected),
            ],
            CHOICES: [
                MessageHandler(filters.Regex(literal_menu), ver_menu),
            ],
            PRODUCTS: [MessageHandler(filters.TEXT, products),],
            CART: [
                MessageHandler(filters.TEXT & ~filters.Regex(literal_back), cart),
                MessageHandler(filters.Regex(literal_back), ver_menu),
            ],
            AMOUNT:[
                MessageHandler(filters.Regex(literal_amount), amount_product),
                MessageHandler(filters.TEXT & ~filters.Regex(literal_amount), amount_product),
            ],
            SHOPPING: [
                MessageHandler(filters.Regex(literal_shopping_add), ver_menu),
                MessageHandler(filters.Regex(literal_shopping_buy), buy_products),
                MessageHandler(filters.TEXT & ~(filters.Regex(literal_shopping_add) & filters.Regex(literal_shopping_buy)), buy_products),
            ],
        },
        fallbacks=[MessageHandler(filters.Regex(literal_done), done)],
        name="my_conversation",
    )
    application.add_handler(conv_handler)
    
    application.run_polling()