from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistrationForm


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            from django.contrib.auth import login

            login(request, user)
            messages.success(request, "Регистрация прошла успешно!")
            return redirect("my_rent")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            return redirect(request.META.get("HTTP_REFERER", "index"))
    return redirect("index")
