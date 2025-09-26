from django.db.models import Q
from django.template.defaulttags import querystring
from django.views.generic import ListView, DetailView

from blog.models import Blog


class BlogListView(ListView):
    model = Blog
    queryset = Blog.objects.all()
    template_name = 'blog_list.html'
    paginate_by = 10
    ordering = ('-created_at', )

    def get_queryset(self):
        queryset = super().get_queryset()

        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) |
                Q(content__icontains=q)
            )
        return queryset

class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog_detail.html'
    # id가 50 이하인 항목들만 반환
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     return queryset.filter(id__lte=50)

    #URL의 pk에 해당하는 객체를 필터된 queryset에서 찾아 반환(없으면 404)
    # def get_object(self):
    #     object = super().get_queryset()
    #     object = self.model.objects.get(pk=self.kwargs('pk'))
    #
    #     return object

    # get_context_data: 템플릿에 전달되는 데이터에 'test': 'CBV' 값 추가
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['test'] = 'CBV'
    #     return context
