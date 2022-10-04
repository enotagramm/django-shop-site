from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0
    max_num = 5
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.photo.url} width="100" height="100"')

    get_image.short_description = "Фото"


class ProductInOrderInline(admin.TabularInline):
    model = \
        ProductInOrder
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Product._meta.fields
                    if field.name != 'slug' and field.name != "description"]
    list_display_links = ("id", "name")
    search_fields = ("title",)
    list_editable = ("is_published",)
    list_filter = ("is_published", "time_create")
    prepopulated_fields = {"slug": ("name",)}
    save_on_top = True
    inlines = [ProductImageInline]

    class Meta:
        model = Product


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "image")
    list_display_links = ("id", "name")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}  # указывает автоматическое заполнение поле slug
    save_on_top = True


class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("id", "get_image", "product", "time_create", "is_published")
    list_display_links = ("id",)
    search_fields = ("time_create",)
    list_editable = ("is_published",)
    list_filter = ("is_published", "time_create")
    save_on_top = True

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.photo.url} width="50" height="50"')

    get_image.short_description = "Фото"


class OrderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Order._meta.fields]
    list_display_links = ("id", "total_price", "name")
    search_fields = ("name", "comments")
    ordering = ('-id',)
    list_filter = ("time_create",)
    save_on_top = True
    inlines = [ProductInOrderInline]

    class Meta:
        model = Order


class ProductInOrderAdmin(admin.ModelAdmin):
    list_display = ("id", "time_create")
    list_display_links = ("time_create",)
    save_on_top = True


class StatusAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "time_create", "is_published")
    list_display_links = ("id", "name")
    save_on_top = True


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "time_create", "is_published")
    list_display_links = ("id", "name")
    save_on_top = True


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(ProductInOrder, ProductInOrderAdmin)
admin.site.register(Review, ReviewAdmin)
