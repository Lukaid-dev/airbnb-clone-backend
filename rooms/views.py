from django.shortcuts import render
from django.http import HttpResponse


def test_hello(request):
    return HttpResponse("Hello World")
