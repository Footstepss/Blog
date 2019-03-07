from django.contrib import admin
from .models import Posts, Category, Tag


admin.site.register(Posts)
admin.site.register(Category)
admin.site.register(Tag)