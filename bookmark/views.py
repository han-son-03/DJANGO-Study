from django.http import HttpResponse, Http404
from django.shortcuts import render

from bookmark.models import Bookmark


# Create your views here.

def bookmark_list(request):
    bookmarks = Bookmark.objects.filter(id__gte=50)

    context = {
        'bookmarks': bookmarks
    }
    return render(request, 'bookmark_list.html', context)

def bookmark_detail(request, pk):
    try:
        bookmark = Bookmark.objects.get(pk=pk)
    except:
        raise Http404

    context = {'bookmark' : bookmark}
    return render(request, 'bookmark_detail.html', context)