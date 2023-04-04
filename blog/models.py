import os.path

from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=20,unique=True)
    #slug 읽을수 있는 텍스트로 된 url사용하고 싶을때 사용
    slug = models.SlugField(max_length=50, unique=True , allow_unicode=True)

    def __str__(self):
     return self.name

    class Meta:
        verbose_name_plural = 'Categories'

#요거 건들면 makemigrations 해야함

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()

    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/',blank=True)
    file_upload = models.FileField(upload_to='blog/filems/%Y/%m/%d/',blank=True)
    hook_message = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author=models.ForeignKey(User,null=True,on_delete=models.SET_NULL)
    category = models.ForeignKey(Category,null=True,on_delete=models.SET_NULL)

    def __str__(self):
        return f'[{self.pk}] {self.title} - {self.author}'

    def get_absolute_url(self):
        return f'/blog/{self.pk}'

    def get_file_name(self):
        return os.path.basename(self.file_upload.name)