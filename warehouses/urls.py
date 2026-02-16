from django.urls import path
from . import views

urlpatterns = [
    path("boxes/", views.boxes, name="boxes"),
]
