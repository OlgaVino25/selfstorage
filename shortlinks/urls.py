from django.urls import path
from . import views

urlpatterns = [
    path("<slug:slug>/", views.redirect_short, name="redirect_short"),
]
