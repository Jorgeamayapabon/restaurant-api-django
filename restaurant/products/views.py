from django.shortcuts import render, redirect
from django.views import generic
from django.utils import timezone

from .models import Product, Category
from .forms import ProductForm, CategoryForm


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