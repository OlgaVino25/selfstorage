from django.shortcuts import render
from django.db.models import Count, Q, Prefetch
from .models import Warehouse, Box


def boxes(request):
    available_boxes_prefetch = Prefetch(
        "boxes",
        queryset=Box.objects.filter(is_available=True),
        to_attr="available_boxes_list",
    )

    warehouses = Warehouse.objects.annotate(
        total_boxes=Count("boxes"),
        available_boxes=Count("boxes", filter=Q(boxes__is_available=True)),
    ).prefetch_related(available_boxes_prefetch)

    return render(request, "boxes.html", {"warehouses": warehouses})
