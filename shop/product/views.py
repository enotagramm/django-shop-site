from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView

from .models import *
from .utils import *
from .forms import *
from cart.forms import CartAddProductForm
from cart.cart import Cart


class ProductHome(DataMixin, ListView):
    """Главная страница"""
    model = ProductImage
    template_name = "product/home.html"
    context_object_name = "products"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="larEk")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return ProductImage.objects.order_by("-id").filter(is_published=True, is_main=True)[:4]


class ProductPage(DataMixin, DetailView):
    """Страница продукта"""
    model = Product
    template_name = "product/product.html"
    slug_url_kwarg = "prod_slug"
    context_object_name = "product"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context["product"])
        return dict(list(context.items()) + list(c_def.items()))


class CategoryPage(DataMixin, ListView):
    """Категории"""
    template_name = "product/product_search.html"
    slug_url_kwarg = "cat_slug"
    context_object_name = "products"

    def get_queryset(self):
        return Product.objects.filter(cat__slug=self.kwargs["cat_slug"], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=f'Категория - {str(context["products"][0].cat)}')
        return dict(list(context.items()) + list(c_def.items()))


class AddReview(View):
    """Отзывы"""
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        product = Product.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.product = product
            form.save()
        return redirect(product.get_absolute_url())


class Search(DataMixin, ListView):
    """Поиск товаров"""
    template_name = "product/product_search.html"
    context_object_name = "products"

    def get_queryset(self):
        return Product.objects.filter(name__iregex=self.request.GET.get("q"))

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = self.request.GET.get("q")
        c_def = self.get_user_context(title=f"Вы искали {context['q']}")
        return dict(list(context.items()) + list(c_def.items()))


def order_create(request):
    cart = Cart(request)
    cats = Category.objects.all()
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                ProductInOrder.objects.create(order=order,
                                              product=item["product"],
                                              total_price=item["price"],
                                              number=item["quantity"],
                                              )
            cart.clear()
            return render(request, 'product/order_created.html', {"order": order,
                                                                  "menu": menu,
                                                                  "cats": cats,
                                                                  })
    else:
        form = OrderCreateForm
    return render(request, 'product/order_create.html', {"cart": cart,
                                                         "form": form,
                                                         "menu": menu,
                                                         "cats": cats,
                                                         })
