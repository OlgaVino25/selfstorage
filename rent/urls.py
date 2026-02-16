from django.urls import path
from . import views

urlpatterns = [
    path("my-rent/", views.my_rent, name="my_rent"),
    path("my-rent-empty/", views.my_rent_empty, name="my_rent_empty"),
]
