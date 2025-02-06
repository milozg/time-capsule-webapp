from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
import random

# Create your views here.

def home_page(request):
    '''Respond to url '', delegate work to a template'''
    template_name = 'hw/home.html'

    context = {
        "time" : time.ctime(),
        'letter1' : chr(random.randint(65,90)),
        'letter2' : chr(random.randint(65,90)),
        'number' : random.randint(1,10),
    }

    return render(request, template_name, context)

def about(request):
    '''Respond to url 'about', delegate work to a template'''
    template_name = 'hw/about.html'

    context = {
        "time" : time.ctime(),
        'letter1' : chr(random.randint(65,90)),
        'letter2' : chr(random.randint(65,90)),
        'number' : random.randint(1,10),
    }

    return render(request, template_name, context)