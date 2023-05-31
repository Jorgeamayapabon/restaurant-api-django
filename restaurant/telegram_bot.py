import django
import os
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

reply_keyboard = [
    ["Ver Menú", "Crear Producto"],
    ["Editar Producto", "Eliminar Producto"],
    ["Salir"],
]
markup = ReplyKeyboardMarkup(reply_keyboard)

literal_done = "^Salir$"
literal_back = "^Atras$"

categories_name = []
products_category = []

categories = {}
products_selections = {}
category_and_product = {}
shopping_cart = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # await context.bot.send_message(chat_id=update.effective_chat.id, text="Bienvenido(a) a tu restaurante, conoces nuestro menú?")
    """Start the conversation, display any stored data and ask user for input."""
    
    reply_text = f"Hola Bienvenido a tu Restaurante {update.effective_user.full_name}, ¿Que quieres hacer el dia de hoy?"
    await update.message.reply_text(reply_text, reply_markup=markup)

    return CHOICES


async def ver_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for info about the selected predefined choice."""
    category_objs = Category.objects.all()
    categories.clear()
    categories_name.clear()
    reply_text = "Este es el Menú, Elige una categoria 🍔🌭🍟:\n"
    reply_keyboard_category = [categories_name, ["Otros"]]
    for model_obj in category_objs:
        categories.update({model_obj.category_name: model_obj.id})
        categories_name.append(model_obj.category_name)
    category_markup = ReplyKeyboardMarkup(reply_keyboard_category)
    await update.message.reply_text(reply_text, reply_markup=category_markup)
    return PRODUCTS


async def products(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    product_objs = Product.objects.all()
    products_category.clear()
    products_selections.clear()
    if text.upper() in categories_name:
        reply_text = f"Estos son los productos de la categoria {text}:\n"
        for model_obj in product_objs:
            if model_obj.category.id == categories[text]:
                reply_text += f"\nProducto: {model_obj.product_name} \n"
                reply_text += f"Descripción: {model_obj.description} \n"
                reply_text += f"Precio: {model_obj.price} \n"
                reply_text += f"Disponibles: {model_obj.amount} unidades\n"
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
        reply_text += "\n¿Cual producto te gustaria agregar?"
        reply_keyboard_finish = [products_category, ["Atras"]]
        markup = ReplyKeyboardMarkup(reply_keyboard_finish)
        await update.message.reply_text(reply_text, reply_markup=markup)
        return CART
    elif text.lower() == "otros":
        reply_text = "Estas son las otras opciones:\n"
        reply_keyboard_others = [["Inicio"], ["Salir"]]
        markup = ReplyKeyboardMarkup(reply_keyboard_others)
        await update.message.reply_text(reply_text, reply_markup=markup)
        return OTHERS


async def cart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    product_selected = text
    selections_dict = products_selections[product_selected]
    amount = 1
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
    reply_text = f"Agregaste de la categoria {selections_dict['category_name']} el producto {product_selected} al carrito de compras.\n\n"
    reply_text += f"Hasta el momento tienes agregados {amount}.\n\n¿Quieres agregar mas?"
    reply_keyboard_shopping = [["Si"],["No"]]
    markup = ReplyKeyboardMarkup(reply_keyboard_shopping)
    await update.message.reply_text(reply_text, reply_markup=markup)
    return AMOUNT


async def amount_product(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    reply_keyboard_shopping = [["Añadir Producto"],["Comprar"], ["Ver Carrito"]]
    if text.lower() == "si":
        reply_text = "¿Cuantos productos deseas agregar?"
        await update.message.reply_text(reply_text, reply_markup=ReplyKeyboardRemove())
        return AMOUNT
    elif text.lower() == "no":
        reply_text = "Producto agregado al carrito de compras.\n\n¿Que quieres hacer ahora?"
        markup = ReplyKeyboardMarkup(reply_keyboard_shopping)
        await update.message.reply_text(reply_text, reply_markup=markup)
        return SHOPPING
    elif text.isdigit():
        _category_product = category_and_product['selection']
        shopping_cart[_category_product]['amount'] = int(text)
        reply_text = f"Agregaste {text} productos al carrito de compras.\n\n¿Que quieres hacer ahora?"
        markup = ReplyKeyboardMarkup(reply_keyboard_shopping)
        await update.message.reply_text(reply_text, reply_markup=markup)
        return SHOPPING


async def buy_products(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if text.lower() == "comprar":
        reply_text = "Ya casi terminamos, dejame te muestro nuestras opciones de pago.\n- Nequi: 3004669165\n- Efectivo."
        reply_keyboard_shopping = [["Pagado"],["Salir"]]
        markup = ReplyKeyboardMarkup(reply_keyboard_shopping)
        await update.message.reply_text(reply_text, reply_markup=ReplyKeyboardRemove())
        await update.message.reply_text(show_shopping_cart(), reply_markup=markup)
        return SHOPPING
    elif text.lower() == "pagado":
        reply_text = "Pago realizado\nMuchas gracias por tu compra. Vuelve pronto.\nSi me necesitas dale al comando /start"
        shopping_cart.clear()
        await update.message.reply_text(reply_text, reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
    elif text.lower() == "ver carrito":
        await update.message.reply_text(show_shopping_cart(), reply_markup=ReplyKeyboardRemove())
        reply_text = "Te gustaría borrar o agregar algun producto al carrito?"
        reply_keyboard_shopping = [["Agregar"],["Borrar"],["Comprar"]]
        markup = ReplyKeyboardMarkup(reply_keyboard_shopping)
        await update.message.reply_text(reply_text, reply_markup=markup)
        return SHOPPING
    elif text.lower() == "borrar":
        reply_text = "¿Cual producto deseas borrar del carrito de compras?"
        reply_keyboard_shopping = [list(shopping_cart.keys())]
        markup = ReplyKeyboardMarkup(reply_keyboard_shopping)
        await update.message.reply_text(reply_text, reply_markup=markup)
        return SHOPPING
    elif text in list(shopping_cart.keys()):
        shopping_cart.pop(text)
        reply_text = f"Fue borrado el producto {text} del carrito de compras"
        reply_keyboard_shopping = [["Añadir Producto"],["Comprar"], ["Ver Carrito"]]
        markup = ReplyKeyboardMarkup(reply_keyboard_shopping)
        await update.message.reply_text(reply_text, reply_markup=markup)
        return SHOPPING
 
in_developing = "Aun en desarrollo comienza de nuevo /start"
async def create_product(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_text = in_developing
    await update.message.reply_text(reply_text, reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


async def update_product(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_text = in_developing
    await update.message.reply_text(reply_text, reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


async def delete_product(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_text = in_developing
    await update.message.reply_text(reply_text, reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Display the gathered info and end the conversation."""
    if "choice" in context.user_data:
        del context.user_data["choice"]

    await update.message.reply_text(
        "Hasta pronto, si necesitas algo solo escribe el comando\n /start",
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END


def show_shopping_cart() -> str:
    reply_text = "Esto es lo que tienes en el carrito de compras\n\n"
    total_price = 0
    for product in list(shopping_cart.values()):
        total_price += product["amount"]*product["selections_dict"]["price"]
        categoria_nombre = product["selections_dict"]["category_name"]
        producto_nombre = product["selections_dict"]["product_name"]
        precio = product["selections_dict"]["price"]
        reply_text += f"De la categoria {categoria_nombre}\nProducto: {producto_nombre}\nPrecio: {precio}\nCantidad: {product['amount']}\n\n"
    reply_text += f"\nPrecio total de la compra: ${total_price}"
    return reply_text


if __name__ == '__main__':
    application = Application.builder().token(BOT_TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            OTHERS:[
                MessageHandler(filters.Regex("^Inicio$"), start),
                MessageHandler(filters.Regex(literal_back), products),
            ],
            CHOICES: [
                MessageHandler(filters.Regex("^Ver Menú$"), ver_menu),
                MessageHandler(filters.Regex("^Crear Producto$"), create_product),
                MessageHandler(filters.Regex("^Editar Producto$"), update_product),
                MessageHandler(filters.Regex("^Eliminar Producto$"), delete_product),
            ],
            PRODUCTS: [MessageHandler(filters.TEXT, products),],
            CART: [
                MessageHandler(filters.TEXT & ~filters.Regex(literal_back), cart),
                MessageHandler(filters.Regex(literal_back), ver_menu),
            ],
            AMOUNT:[
                MessageHandler(filters.Regex("^(Si|No)$"), amount_product),
                MessageHandler(filters.TEXT & ~filters.Regex("^(Si|No)$"), amount_product),
            ],
            SHOPPING: [
                MessageHandler(filters.Regex("^(Añadir Producto|Agregar)$"), ver_menu),
                MessageHandler(filters.Regex("^(Comprar|Pagado|Ver Carrito|Borrar)$"), buy_products),
                MessageHandler(filters.TEXT & ~(filters.Regex("^(Añadir Producto|Agregar|Comprar|Pagado|Ver Carrito|Borrar)$")), buy_products),
            ],
        },
        fallbacks=[MessageHandler(filters.Regex(literal_done), done)],
        name="my_conversation",
    )
    application.add_handler(conv_handler)
    
    application.run_polling()