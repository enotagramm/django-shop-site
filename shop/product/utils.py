from django.db.models import Count

from .models import *
from cart.forms import CartAddProductForm

menu = [
    {'title': 'Главная', 'url_name': 'home'},
    {'title': 'Доставка', 'url_name': 'delivery'},
    {'title': 'Контакты', 'url_name': 'contacts'},
    {'title': 'О нас', 'url_name': 'about'},
]


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        cats = Category.objects.all()
        cart_product_form = CartAddProductForm()
        context["menu"] = menu
        context["cats"] = cats
        context["cart_product_form"] = cart_product_form
        return context
