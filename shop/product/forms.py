from django import forms

from .models import *


class ReviewForm(forms.ModelForm):
    """Форма отзывов"""
    class Meta:
        model = Review
        fields = ("name", "email", "comment")
