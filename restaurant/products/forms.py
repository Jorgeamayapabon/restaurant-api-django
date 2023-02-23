from django import forms
from django.forms import ModelForm

from .models import Product, Category

#B
class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['category','product_name', 'description', 'price', 'amount']

#A
class CategoryForm(ModelForm):    
    class Meta:
        model = Category
        fields = ['category_name']