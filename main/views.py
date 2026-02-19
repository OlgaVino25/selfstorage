from django.shortcuts import render
from .models import FAQCategory


def index(request):
    return render(request, "index.html")


def faq(request):
    categories = FAQCategory.objects.prefetch_related("items").all()
    return render(request, "faq.html", {"categories": categories})
