"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.urls import path

baseball_lists = [
    {'team': '한화 이글스', 'local' : '대전광역시'},
    {'team': 'KIA 타이거즈', 'local' : '광주광역시'},
    {'team': '삼성 라이온즈', 'local' : '대구광역시'},
    {'team': '롯데 자이언츠', 'local' : '부산광역시'},
    {'team': '두산 베어스', 'local' : '서울특별시'},
]


def index(request):
    return HttpResponse('<h1>Hello</h1>')

def book_list(request):
    book_text = ''

    for i in range(0, 10):
        book_text += f'book {i}<br>'
    return HttpResponse(book_text)

def book(request, num):
    book_text = f'book {num}번 페이지 입니다.'
    return HttpResponse(book_text)

def language(request, lang):
    return HttpResponse(f'<h1>{lang} 언어 페이지입니다.</h1>')

def python(request):
    return HttpResponse('python 페이지 입니다.')

def baseball_team(request):
    # team_ranks = [
    #     f'<a href="/baseball/{index}">{baseball['team']}</a><br>'
    #     for index, baseball in enumerate(baseball_lists)
    # ]
    # response_text = '<br>'.join(team_ranks)
    #
    # return HttpResponse(response_text)
    return render(request, 'baseball.html', {'baseball_lists': baseball_lists})


def team_local(request, index):
    if index > len(baseball_lists) - 1:
        raise Http404

    baseball = baseball_lists[index]

    response_text = f'<h1>{baseball["team"]}</h1> <p>지역: {baseball["local"]}</p>'
    return HttpResponse(response_text)





urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index),
    path('book_list', book_list),
    path('book_list/<int:num>', book),
    path('language/python', python),
    path('language/<str:lang>/', language),
    path('baseball/', baseball_team),
    path('baseball/<int:index>', team_local),

]
