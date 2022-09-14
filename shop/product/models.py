from django.db import models
from django.db.models.signals import post_save


class Product(models.Model):
    """Товары магазина"""
    name = models.CharField('Наименование товара', max_length=50)
    description = models.TextField('Описание товара')
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    discount = models.IntegerField('Cкидка', default=0)
    is_published = models.BooleanField('В наличии', default=True)
    time_create = models.DateTimeField('Время создания', auto_now_add=True)
    time_update = models.DateTimeField('Время редактирования', auto_now=True)
    slug = models.SlugField('URL', max_length=50, unique=True, db_index=True)
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категории')

    def __str__(self):
        return f'{self.name}, {self.price}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-id']


class Category(models.Model):
    """Категории товара"""
    name = models.CharField('Категория', max_length=50)
    slug = models.SlugField('URL', max_length=50, unique=True, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class ProductImage(models.Model):
    """Фото товара"""
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name='Товар')
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото товара")
    is_main = models.BooleanField('Главное фото', default=False)
    is_published = models.BooleanField('Активен', default=True)
    time_create = models.DateTimeField('Время создания', auto_now_add=True)
    time_update = models.DateTimeField('Время редактирования', auto_now=True)

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'


class Order(models.Model):
    """Заказ"""
    total_price = models.DecimalField('Общая цена на товары', max_digits=10, decimal_places=2, null=True, blank=True)
    name = models.CharField('Имя покупателя', max_length=50)
    email = models.EmailField('Почта покупателя', blank=True)
    phone = models.CharField('Телефон покупателя', max_length=50)
    address = models.CharField('Адрес покупателя', max_length=150, null=True, blank=True)
    comments = models.TextField('Комментарии к заказу', blank=True)
    time_create = models.DateTimeField('Время создания', auto_now_add=True)
    time_update = models.DateTimeField('Время редактирования', auto_now=True)
    status = models.ForeignKey("Status", on_delete=models.PROTECT, verbose_name='Статус заказа')

    def __str__(self):
        return f'Заказ № {self.id}'

    def save(self, *args, **kwargs):
        super(Order, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class ProductInOrder(models.Model):
    """Товар в заказе"""
    order = models.ForeignKey(Order, on_delete=models.PROTECT, verbose_name='Заказ')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name='Товар')
    number = models.IntegerField('Количество', default=1)
    price_per_item = models.DecimalField('Цена', max_digits=10, decimal_places=2, null=True, blank=True)
    total_price = models.DecimalField('Общая цена на товар', max_digits=10, decimal_places=2, null=True, blank=True)
    time_create = models.DateTimeField('Время создания', auto_now_add=True)
    time_update = models.DateTimeField('Время редактирования', auto_now=True)
    is_active = models.BooleanField('Активен', default=True)

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары в заказе'

    def save(self, *args, **kwargs):  # шаблон для переопределения модели
        price_per_item = self.product.price
        self.price_per_item = price_per_item

        self.total_price = self.number * self.price_per_item

        super(ProductInOrder, self).save(*args, **kwargs)


def product_in_order_post_save(sender, instance, created, **kwargs):  # пост сигнал
    order = instance.order
    all_products_in_order = ProductInOrder.objects.filter(order=order, is_active=True)
    order_total_price = 0
    for i in all_products_in_order:
        order_total_price += i.total_price

    instance.order.total_price = order_total_price
    instance.order.save(force_update=True)


post_save.connect(product_in_order_post_save, sender=ProductInOrder)


class Status(models.Model):
    """Статус заказа"""
    name = models.CharField('Название статуса', max_length=30)
    is_published = models.BooleanField('Активен', default=True)
    time_create = models.DateTimeField('Время создания', auto_now_add=True)
    time_update = models.DateTimeField('Время редактирования', auto_now=True)

    def __str__(self):
        return f'Статус: {self.name}'

    class Meta:
        verbose_name = 'Cтатус'
        verbose_name_plural = 'Статусы'
