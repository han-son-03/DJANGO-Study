from django.db import models

class blog(models.Model):
    CATEGORY_CHOICES = (
    ('free', '자유'),
    ('travel', '여행'),
    ('dog', '강아지'),
    ('cat', '고양이'),
    )

    category = models.CharField('카테고리', max_length=10, choices=CATEGORY_CHOICES)
    title = models.CharField(max_length=100)
    content = models.TextField('본문')

    created_at = models.DateTimeField('작성일자', auto_now_add=True)
    updated_at = models.DateTimeField('수정일자', auto_now=True)


# 제목 ✅
# 본문 ✅
# 작성자 --> 추후 작성
# 작성일자 ✅
# 수정일자 ✅
# 카테고리

