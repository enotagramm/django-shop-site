from django.shortcuts import render

from .models import *


def home(request):
    products_images = ProductImage.objects.order_by("-id").filter(is_published=True,
                                                                  is_main=True)[:3]
    products_images_phones = ProductImage.objects.filter(product__cat__id=1,
                                                         is_main=True,
                                                         is_published=True)[:3]

    return render(request, "product/home.html", locals())


def product(request, prod_slug):
    product_one = Product.objects.get(slug=prod_slug)
    return render(request, "product/product.html", locals())


