from django.urls import path

from .views import *

urlpatterns = [
    path("", home, name="home"),
    path('product/<slug:prod_slug>/', product, name='product'),
]

