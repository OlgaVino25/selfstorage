from django.urls import path
from . import views

urlpatterns = [
    path("", views.boxes, name="boxes"),
]
