# from django.shortcuts import render
from django.http import HttpResponse


def hello_world(request):
    return HttpResponse("Hello world!")


"""
def blog(request):
    return HttpResponse("I am Blog")
"""


def blog(request, **kwargs):
    return HttpResponse(f'{kwargs}')
