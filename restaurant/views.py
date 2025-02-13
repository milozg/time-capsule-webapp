# restaurant/views.py

from django.shortcuts import render, redirect
import random
import time


# Create your views here.

allItems = {
    'Lobster $90' : 90,
    'Big Lobster $140' : 140,
    'MEGA Lobster $299' : 299,
    'Bread $1' : 1,
    'Lobster stock $80' : 80,
    'Empty lobster shells $30' : 30,
    'Essence of lobster $15' : 15,
    'Extra Butter $40' : 40
}

specials = [
    'Lobster stock $80',
    'Empty lobster shells $30',
    'Essence of lobster $15'
]

def main(request):
    '''Process a request for the '' url annd delegate tasks to a template'''

    template_name="restaurant/main.html"

    return render(request, template_name)

def order(request):
    '''Process a request for the 'order' url annd delegate tasks to a template'''
    print(request)

    template_name="restaurant/order.html"

    context = {
        'special' : specials[random.randint(0,2)]
    }

    return render(request, template_name, context)

def confirmation(request):
    '''Process the form submittion and generate a confirmation page, or redirect to the order page if it is not a POST'''

    if request.POST:
        template_name = "restaurant/confirmation.html"
        print(request.POST)
        items = []

        if 'item' in request.POST:
            items += request.POST.getlist('item')
        if 'special' in request.POST:
            items += request.POST.getlist('special')

        total = sum(list(map(lambda x : allItems[x],items)))

        context = {
            'items' : items,
            'total' : total,
            'name' : request.POST['Name'],
            'phone' : request.POST['Phone'],
            'email' : request.POST['Email'],
            'instructions' : request.POST['instructions'],
            'readytime' : time.ctime(time.time() + random.uniform(1800.0, 3600.0))
        }
        return render(request, template_name, context)
    else:
        return redirect('/restaurant/order')