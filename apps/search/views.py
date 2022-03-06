from django.shortcuts import render
from django.contrib import messages


# Create your views here.


# @login_required(login_url='accounts/login_user')
def search_gene(request):
    context = {
        'segment': 'search'
    }
    return render(request, 'home/search.html', context)
