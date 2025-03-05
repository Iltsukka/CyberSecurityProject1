from django.shortcuts import render, get_object_or_404

# Create your views here.

from django.http import HttpResponse
from . models import Blogpost, Comment


def index(request):
    return HttpResponse('Blogs index')
