from io import BytesIO
from pathlib import Path

from PIL import Image
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

    image = models.ImageField('이미지', null=True, blank=True, upload_to='blog/%Y/%m/%d')
    thumbnail = models.ImageField('썸네일', null=True, blank=True,
                                  upload_to='blog/%Y/%m/%d/thumbnail')
    # 2024/4/23일
    # blog/2024/4/23/이미지파일.jpg
    # ImageField, FileField 와 같기만 이미지만 업로드하게 되어있다.
    # varchar => 경로만 저장을 함



    def __str__(self):
        return f'[{self.get_category_display()}] {self.title[:10]}'
    # get_thumbnail_image 썸네일과 이미지를 출력하는 함수 원래는 blog_list에 있었으나 여기에 작성
    def get_thumbnail_image(self):
        if self.thumbnail:
            return self.thumbnail.url
        elif self.image:
            return self.image.url
        return None


    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'blog_pk':self.pk})

    def save(self, *args, **kwargs):
        if not self.image:
            return super().save(*args, **kwargs)

        image = Image.open(self.image)
        image.thumbnail((300, 300))

        image_path = Path(self.image.name) # Path 라이브러리를 사용해 이미지 경로를 가져옵니다

        thumbnail_name = image_path.stem # /blog/2024/8/13/database.png -> database
        thumbnail_extension = image_path.suffix # /blog/2024/8/13/database.png -> .png
        thumbnail_filename = f'{thumbnail_name}_thumb{thumbnail_extension}'
        #확장자에 맞춰 처리해 주는 알고리즘
        if thumbnail_extension in ['.jpg', 'jpeg']:
            file_type = 'JPEG'
        elif thumbnail_extension == '.gif':
            file_type = 'GIF'
        elif thumbnail_extension == '.png':
            file_type = 'PNG'
        else:
            return super().save(*args, **kwargs)
        # BytesIO라는 인메모리에 저장
        temp_thumb = BytesIO()
        image.save(temp_thumb, file_type)
        temp_thumb.seek(0)
        # 장고에 있는 썸네일 필드에 이름과 인메모리 대체를 바로 디비콘 하지 않는다.
        self.thumbnail.save(thumbnail_filename, temp_thumb, save=False)
        temp_thumb.close()
        return super().save(*args, **kwargs)



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
        ordering = ['-created_at', '-id']


#블로그 정도
#댓글 내용
#작성자
#작성일자
#수정일자
