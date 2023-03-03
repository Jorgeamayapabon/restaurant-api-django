import json
import requests

from django.shortcuts import render, redirect
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.http import HttpResponse, JsonResponse

from .models import Product, Category
from .forms import ProductForm, CategoryForm

TELEGRAM_URL = "https://api.telegram.org/bot"
BOT_TOKEN = "5997463720:AAG_WMB8BOoX97cRc5AE5bfwWZS9N3QFe60"


class ChatBot(generic.View):
    """"""
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        print(data)
        productos = Product.objects.all()
        categorias = Category.objects.all()
        categoria_list = []
        categoria_id_list = []
        text = data["message"]["text"]
        chat = data["message"]["chat"]["id"]
        chat = str(chat)
        text = text.upper()

        general="¿Que quieres hacer? 😊\n"

        if text == "/START":
            msg1 = "Escribe 'Productos' para ver los Productos 🍔🍟\n"
            
            self.enviar_mensaje(general, chat)
            self.enviar_mensaje(msg1, chat)

        elif text == "PRODUCTOS":
            msg2 = "Estos son los productos disponibles 😊\n"
            categoria_id_list.clear()
            categoria_list.clear()

            self.enviar_mensaje(msg2, chat)
            for categoria in categorias:
                categoria_list.append(categoria.category_name)
                categoria_id_list.append(categoria.id)
                self.enviar_mensaje(categoria.category_name, chat)


        elif text in categoria_list:
            msg2 = f"Est@s son l@s {text} 😍 \n"
            self.enviar_mensaje(msg2, chat)
            idx = categoria_list.index(text)
            print(idx)
            for producto in productos:
                if producto.category.id == categoria_id_list[idx]:
                    self.enviar_mensaje(producto.product_name, chat)
                    self.enviar_mensaje(producto.description, chat)
                    self.enviar_mensaje(f"${producto.price}", chat)

        return JsonResponse({"ok": "request processed"})

    @staticmethod
    def enviar_mensaje(message, chat_id):
        data = {
            "text": message,
            "chat_id": chat_id,
        }
        response = requests.post(
            TELEGRAM_URL + BOT_TOKEN + "/sendMessage?", data=data
        )
class Home(generic.ListView):
    template_name = "products/home.html"
   
    def get_queryset(self):
        return Product.objects.filter(created__lte=timezone.now()).order_by("-created")[:5]


class Products(generic.ListView):
    template_name = "products/products.html"
    context_object_name = 'products'
        
    def get_queryset(self):
        return Product.objects.all()


class Categories(generic.ListView):
    template_name = "products/categories.html"
    context_object_name = 'categories'
        
    def get_queryset(self):
        return Category.objects.all()
    

class CreateProduct(generic.CreateView):
    template_name = "products/create_products.html"
    form_class = ProductForm
    success_url = '/products/'
    
class CreateCategory(generic.CreateView):
    template_name = "products/create_category.html"
    form_class = CategoryForm
    success_url = '/categories/'

class DeleteProduct(generic.DeleteView):
    model = Product
    success_url = "/products/"