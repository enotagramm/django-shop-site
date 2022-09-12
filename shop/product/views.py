from django.shortcuts import render

from .models import *


def home(request):
    products_images = ProductImage.objects.order_by("-id").filter(is_published=True, is_main=True)[:4]
    return render(request, "product/home.html", locals())

