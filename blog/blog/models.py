from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from utils.models import TimeStampedModel

User = get_user_model()

class Blog(TimeStampedModel):
    CATEGORY_CHOICES = (
    ('free', '자유'),
    ('travel', '여행'),
    ('dog', '강아지'),
    ('cat', '고양이'),
    )

    category = models.CharField('카테고리', max_length=10, choices=CATEGORY_CHOICES, default='free')
    title = models.CharField(max_length=100)
    content = models.TextField('본문')
    author = models.ForeignKey(User, on_delete=models.CASCADE)



    def __str__(self):
        return f'[{self.get_category_display()}] {self.title[:10]}'
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk':self.pk})

    class Meta:
        verbose_name = '블로그'
        verbose_name_plural = '블로그 목록'

# 제목 ✅
# 본문 ✅
# 작성자 --> 추후 작성
# 작성일자 ✅
# 수정일자 ✅
# 카테고리✅

class Comment(TimeStampedModel):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    content = models.CharField('본문', max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.blog.title} 댓글'

    class Meta:
        verbose_name = '댓글'
        verbose_name_plural = '댓글 목록'


#블로그 정도
#댓글 내용
#작성자
#작성일자
#수정일자
