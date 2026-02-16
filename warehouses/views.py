from django.shortcuts import render


def boxes(request):
    return render(request, "boxes.html")
