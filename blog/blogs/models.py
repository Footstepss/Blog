from django.db import models
from db.base_model import BaseModel
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.html import strip_tags #去掉html标签
import markdown
# Create your models here.

class Category(BaseModel):
    '''文章种类'''
    #与post一对多得关系
    name = models.CharField(max_length=100)

class Tag(BaseModel):
    '''文章标签'''
    #与post为多对多得关系
    name = models.CharField(max_length=100)

class Posts(BaseModel):
    '''文章'''
    #文章标题
    title = models.CharField(max_length=70)

    #文章正文
    body = models.TextField()

    #文章摘要
    excerpt = models.CharField(max_length=200,blank=True)

    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag,blank=True)

    #django.contrib.auth 是 Django 内置的应用，专门用于处理网站用户的注册、登录等流程，User 是 Django 为我们已经写好的用户模型
    ## 文章作者，这里 User 是从 django.contrib.auth.models 导入的
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    #该类型只能是0或正整数
    views = models.PositiveIntegerField(default=0)

    def get_absolute_url(self):
        return reverse('blogs:single', kwargs={'pk': self.pk})

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def save(self, *args, **kwargs):
        if not self.excerpt:
            # 首先实例化一个 Markdown 类，用于渲染 body 的文本
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            # 先将 Markdown 文本渲染成 HTML 文本
            # strip_tags 去掉 HTML 文本的全部 HTML 标签
            # 从文本摘取前 54 个字符赋给 excerpt
            self.excerpt = strip_tags(md.convert(self.body))[:54]

            # 调用父类的 save 方法将数据保存到数据库中
        super(Posts, self).save(*args, **kwargs)