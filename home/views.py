from django.shortcuts import render, redirect
from django.http import HttpRequest


# Create your views here.
def home(request: HttpRequest):
    return redirect("blog/")
