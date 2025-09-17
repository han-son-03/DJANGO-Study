from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def bookmark_list(request):
    return render(request, 'bookmark_list.html')

def bookmark_detail(request, number):
    return render(request, 'bookmark_detail.html', {'number': number})