from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return render(request, "base.html")


def about_us(request):
    return HttpResponse("About Us")


def contacts(request):
    return HttpResponse("Contacts")


def authors(request):
    return HttpResponse("Authors")
