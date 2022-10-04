from django import forms

from .models import *


class ReviewForm(forms.ModelForm):
    """Форма отзывов"""
    class Meta:
        model = Review
        fields = ("name", "email", "comment")


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["name", "email", "phone", "address", "comments"]
