from django.contrib import admin
from . models import Category, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('category','product_name', 'price', 'amount', 'modified')


admin.site.register(Category)