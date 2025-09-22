from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from blog.forms import BlogForm
from blog.models import Blog


def blog_list(request):
    blogs = Blog.objects.all().order_by('-created_at')

    q = request.GET.get('q')
    if q:
        blogs = blogs.filter(
            Q(title__icontains=q) |
            Q(content__icontains=q)
        )

        # blogs = blogs.filter(content__icontains=q)

    paginator = Paginator(blogs, 10)
    page =request.GET.get('page')
    page_object = paginator.get_page(page)

    context = {
        # 'blogs': blogs,
        'page_object': page_object,
    }
    return render(request, 'blog_list.html', context)

def blog_create(request):
    form = BlogForm()
    context = {
        'form': form,
    }
    return render(request,blog_create.html, context)

def blog_detail(request, pk):
    blog_id = get_object_or_404(Blog, pk=pk)
    context = {
        'blog': blog_id,
    }
    return render(request, 'blog_detail.html',context)

@login_required()
def blog_create(request):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))

    form = BlogForm(request.POST or None)
    if form.is_valid():
        blog = form.save(commit=False)
        blog.author = request.user
        blog.save()
        return redirect(reverse('blog_detail', kwargs={'pk': blog.pk}))
    context = {'form' : form,}
    return render(request, 'blog_create.html', context)

@login_required()
def blog_update(request, pk):
    blog = get_object_or_404(Blog, pk=pk, author=request.user)

    form = BlogForm(request.POST or None, instance=blog)
    if form.is_valid():
        blog.save()
        return redirect(reverse('blog_detail', kwargs={'pk': blog.pk}))

    context = {
        'blog': blog,
        'form': form,
    }
    return render(request, 'blog_update.html', context)
