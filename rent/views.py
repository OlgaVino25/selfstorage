import json
from datetime import date, timedelta
from decimal import Decimal
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Rent, PromoCode
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
def apply_promo(request):
    data = json.loads(request.body)
    box_id = data.get("box_id")
    promo_code_str = data.get("promo_code", "").strip()

    if not box_id or not promo_code_str:
        return JsonResponse({"success": False, "error": "Не указан бокс или промокод"})

    try:
        box = Box.objects.get(id=box_id, is_available=True)
    except Box.DoesNotExist:
        return JsonResponse({"success": False, "error": "Бокс недоступен"})

    try:
        promo = PromoCode.objects.get(code=promo_code_str, is_active=True)
        if not promo.is_valid():
            return JsonResponse({"success": False, "error": "Промокод недействителен"})
    except PromoCode.DoesNotExist:
        return JsonResponse({"success": False, "error": "Промокод не найден"})

    base_price = box.price_per_month
    start_date = date.today()
    end_date = start_date + timedelta(days=30)
    months = (end_date.year - start_date.year) * 12 + (
        end_date.month - start_date.month
    )
    if months <= 0:
        months = 1
    total = base_price * months
    discount = Decimal(promo.discount_percent) / Decimal(100)
    total_with_discount = total * (Decimal(1) - discount)

    return JsonResponse(
        {
            "success": True,
            "original_price": float(total),
            "discounted_price": float(total_with_discount),
            "discount_percent": promo.discount_percent,
        }
    )


def check_promo(request):
    data = json.loads(request.body)
    promo_code_str = data.get("promo_code", "").strip()

    if not promo_code_str:
        return JsonResponse({"success": False, "error": "Введите промокод"})

    try:
        promo = PromoCode.objects.get(code=promo_code_str, is_active=True)
        if not promo.is_valid():
            return JsonResponse({"success": False, "error": "Промокод недействителен"})
    except PromoCode.DoesNotExist:
        return JsonResponse({"success": False, "error": "Промокод не найден"})

    return JsonResponse(
        {
            "success": True,
            "discount_percent": promo.discount_percent,
        }
    )


def create_order(request):
    data = json.loads(request.body)
    box_id = data.get("box_id")
    delivery = data.get("delivery", False)
    measurements = data.get("measurements", False)
    promo_code_str = data.get("promo_code", "").strip()

    try:
        box = Box.objects.get(id=box_id, is_available=True)
    except Box.DoesNotExist:
        return JsonResponse({"success": False, "error": "Бокс недоступен"})

    promo = None
    if promo_code_str:
        try:
            promo = PromoCode.objects.get(code=promo_code_str, is_active=True)
            if not promo.is_valid():
                promo = None
        except PromoCode.DoesNotExist:
            promo = None

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
        promo_code=promo,
    )

    box.is_available = False
    box.save()

    return JsonResponse({"success": True})
