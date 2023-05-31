from django.urls import path

from . import views
from django.views.decorators.csrf import csrf_exempt


app_name = "products"
urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("products/", views.Products.as_view(), name="products"),
    path("categories/", views.Categories.as_view(), name="categories"),
    path("products/create/", views.CreateProduct.as_view(), name="create_products"),
    path("products/delete/", views.DeleteProduct.as_view(), name="delete_products"),
    path("categories/create/", views.CreateCategory.as_view(), name="create_category"),
]