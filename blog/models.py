import os.path

from django.contrib.auth.models import User
from django.db import models
from markdown import markdown
from markdownx.models import MarkdownxField


class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=50, unique=True, allow_unicode=True)

    def get_absolute_url(self):
        return f'/blog/tag/{self.slug}'

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=20,unique=True)
    #slug 읽을수 있는 텍스트로 된 url사용하고 싶을때 사용
    slug = models.SlugField(max_length=50, unique=True , allow_unicode=True)

    def get_absolute_url(self):
        return f'/blog/category/{self.slug}'

    def __str__(self):
     return self.name

    class Meta:
        verbose_name_plural = 'Categories'

#요거 건들면 makemigrations 해야함

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=30)
    content = MarkdownxField()

    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/',blank=True)
    img1 = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)
    img2 = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)
    img3 = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)
    file_upload = models.FileField(upload_to='blog/filems/%Y/%m/%d/',blank=True)
    hook_message = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    calorie = models.DecimalField(max_digits=10,decimal_places=2,null=True)
    cm = models.DecimalField(max_digits=10,decimal_places=2,null=True)
    kg = models.DecimalField(max_digits=5,decimal_places=2,null=True)
    GENDERS = (
        ('M', '남성(Man)'),
        ('W', '여성(Woman)'),
    )
    gender = models.CharField(verbose_name='성별', max_length=1, choices=GENDERS,null=True)

    author=models.ForeignKey(User,null=False,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,null=True,on_delete=models.SET_NULL)
    tag=models.ManyToManyField(Tag)

    def __str__(self):
        return f'[{self.pk}] {self.title} - {self.author}'

    def get_absolute_url(self):
        return f'/blog/{self.pk}'

    def get_file_name(self):
        return os.path.basename(self.file_upload.name)

    def get_content_markdown(self):
        return markdown(self.content)

    #비만도 계산
    def get_calculate_pibw(self):
        if self.gender == 'M':
            pibw = self.kg/ (self.cm/100 * self.cm/100 * 22) * 100
        elif self.gender =='W':
            pibw = self.kg/ (self.cm/100 * self.cm/100 * 21) * 100
        pibw=round(pibw,2)
        if pibw<90:
            grade="저체중"
        elif pibw>=90 and pibw<110:
            grade="정상체중"
        elif pibw>=110 and pibw<120:
            grade="과체중"
        elif pibw>=120 and pibw<130:
            grade="경도비만"
        elif pibw>=130 and pibw<160:
            grade="중도체중"
        else:
            grade="고도비만"
        return grade


    #bmi 지수 계산
    def get_calculate_bmi(self):
        bmi=self.kg/(self.cm/100 * self.cm/100)
        return round(bmi,2)

    #권장 섭취 칼로리 계산
    def get_recommend_kcal(self):
        if self.gender == 'M':
            recommend_kcal = self.cm/100 * self.cm/100 * 22 * 30
        elif self.gender =='W':
            recommend_kcal = self.cm/100 * self.cm/100 * 21 * 30
        return round(recommend_kcal,2)

    #표준 체중 계산
    def get_recommend_kg(self):
        if self.gender == 'M':
            recommend_kg = self.cm / 100 * self.cm / 100 * 22
        elif self.gender == 'W':
            recommend_kg = self.cm / 100 * self.cm / 100 * 21
        return round(recommend_kg,2)

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author} -{self.content}'

    def get_absolute_url(self):
        return f'{self.post.get_absolute_url()}#comment-{self.pk}'
