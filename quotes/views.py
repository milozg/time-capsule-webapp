from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import random

quotes = [
    "An assist makes two people happy. A point make one guy happy.",
    "I played in Serbia, brother.",
    "In high school, I couldn't do one pushup.",
]

images = [
    "https://static01.nyt.com/athletic/uploads/wp/2023/10/07085025/231007-Nikola-Jokic-scaled-e1696683052376.jpg",
    "https://media.cnn.com/api/v1/images/stellar/prod/210609043854-01-nikola-jokic.jpg?q=w_3000,h_2045,x_0,y_0,c_fill",
    "https://phantom-marca.unidadeditorial.es/4dc1223b1b80b7a9d4b98260f1675c84/crop/0x0/2044x1363/resize/828/f/jpg/assets/multimedia/imagenes/2024/12/05/17334379480370.jpg",
]

def quote(request):
    '''Respond to url '', delegate work to a template'''

    template = 'quotes/quote.html'

    context = {
        "randQuote" : quotes[random.randint(0,2)],
        "randImage" : images[random.randint(0,2)]
    }

    return render(request, template, context)

def show_all(request):
    '''Respond to url 'show_all', delegate work to a template'''

    template = 'quotes/show_all.html'

    context = {
        "zip" : zip(quotes, images)
    }

    return render(request, template, context)

def about(request):
    '''Respond to url 'show_all', delegate work to a template'''
    template = 'quotes/about.html'
    return render(request, template)