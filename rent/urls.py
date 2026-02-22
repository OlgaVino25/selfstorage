from django.urls import path
from . import views

urlpatterns = [
    path("my-rent/", views.my_rent, name="my_rent"),
    path("my-rent-empty/", views.my_rent_empty, name="my_rent_empty"),
    path("create-order/", views.create_order, name="create_order"),
    path("apply-promo/", views.apply_promo, name="apply_promo"),
    path("check-promo/", views.check_promo, name="check_promo"),
]
