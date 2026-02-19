from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Rent


@login_required
def my_rent(request):
    rents = (
        Rent.objects.filter(user=request.user, is_active=True)
        .select_related("box__warehouse")
        .prefetch_related("items")
    )
    return render(request, "my-rent.html", {"rents": rents})


def my_rent_empty(request):
    return render(request, "my-rent-empty.html")
