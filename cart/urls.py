
from django.urls import path, include
from .views import AddProduct, GetCart

urlpatterns = [
    path('add-product/<int:pk>/', AddProduct.as_view(), name = "product_add"),
    path('my-cart/', GetCart.as_view(), name = "cart_get")
    ]