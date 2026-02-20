import json
from datetime import date, timedelta
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Rent
from warehouses.models import Box


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


@login_required
@require_POST
def create_order(request):
    data = json.loads(request.body)
    box_id = data.get("box_id")
    delivery = data.get("delivery", False)
    measurements = data.get("measurements", False)

    try:
        box = Box.objects.get(id=box_id, is_available=True)
    except Box.DoesNotExist:
        return JsonResponse({"success": False, "error": "Бокс недоступен"})

    start_date = date.today()
    end_date = start_date + timedelta(days=30)
    deposit = 0

    rent = Rent.objects.create(
        user=request.user,
        box=box,
        start_date=start_date,
        end_date=end_date,
        deposit=deposit,
        is_active=False,
        delivery_required=delivery,
        measurements_required=measurements,
    )

    box.is_available = False
    box.save()

    return JsonResponse({"success": True})
