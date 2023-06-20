from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin

from food.models import SearchFood
from .models import Post, Category, Tag ,Comment

# Register your models here.

admin.site.register(Post, MarkdownxModelAdmin)
admin.site.register(Comment)
admin.site.register(SearchFood)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
admin.site.register(Category,CategoryAdmin)

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
admin.site.register(Tag,TagAdmin)
