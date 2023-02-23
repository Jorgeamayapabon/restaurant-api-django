from django.db import models


class Category(models.Model):
    category_name = models.CharField(max_length=50, verbose_name='Nombre de categoria', unique=True)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        db_table = 'Category'
        ordering = ['category_name']


class Product(models.Model):
    category = models.ForeignKey(Category, null=False, blank=False, on_delete=models.CASCADE, verbose_name='Categoria')
    product_name = models.CharField(max_length=50, verbose_name='Nombre del producto')
    description = models.TextField(max_length=200, blank=True, verbose_name='Descripcion')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    price = models.IntegerField(default=0, verbose_name='Precio')
    amount = models.IntegerField(default=0, verbose_name='Cantidad')

    def __str__(self):
        return self.product_name

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        db_table = 'Product'
        ordering = ['category','price']