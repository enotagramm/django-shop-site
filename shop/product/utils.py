from django.db.models import Count

from .models import *

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
        context["menu"] = menu
        context["cats"] = cats
        return context
