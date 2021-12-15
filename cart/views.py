from django.shortcuts import render
from django.views.generic.base import View
from django.template.response import TemplateResponse
from django.http.response import HttpResponse
from .cart import Cart
from courses.models import Course
# Create your views here.

class AddProduct(View):
    def get(self, request, pk):
        cart= Cart(request)
        cart.add(pk)
        return HttpResponse(status=201)

class GetCart(View):
    http_method_names = ['get']
    def get(self, request):
        cart = Cart(request)
        queryset = Course.objects.filter(id__in = cart.cart)
        return TemplateResponse(request=request, template=r'cart\cart_detail.html', context={'queryset':queryset})
