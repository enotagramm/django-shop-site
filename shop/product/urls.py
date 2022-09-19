from django.urls import path

from .views import *

urlpatterns = [
    path("", ProductHome.as_view(), name="home"),
    path("product/<slug:prod_slug>/", ProductPage.as_view(), name='product'),
    path("<int:pk>/", AddReview.as_view(), name="add_review"),
    path("search/", Search.as_view(), name="search")
]

