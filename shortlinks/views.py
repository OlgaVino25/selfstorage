from django.shortcuts import render, get_object_or_404, redirect
from .models import ShortLink


def redirect_short(request, slug):
    link = get_object_or_404(ShortLink, slug=slug)
    link.clicks += 1
    link.save(update_fields=["clicks"])
    return redirect(link.target_url)
