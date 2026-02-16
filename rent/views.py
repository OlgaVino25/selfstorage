from django.shortcuts import render


def my_rent(request):
    return render(request, "my-rent.html")


def my_rent_empty(request):
    return render(request, "my-rent-empty.html")
