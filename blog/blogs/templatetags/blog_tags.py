from ..models import Posts,Category,Tag
from django import template
from django.db.models.aggregates import Count

register = template.Library()
@register.simple_tag
def get_recent_post(num=5):
    '''获取数据库中前 num 篇文章'''
    return Posts.objects.all().order_by('-create_time')[:num]

@register.simple_tag
def archives():
    '''归档'''
    #这里 dates 方法会返回一个列表，列表中的元素为每一篇文章（Post）的创建时间，且是 Python 的 date 对象，精确到月份，降序排列
    return Posts.objects.dates('create_time', 'month', order='DESC')

@register.simple_tag
def get_categories():
    '''
    return:Category.objects.annotate 方法和 Category.objects.all 有点类似，
    它会返回数据库中全部 Category 的记录，但同时它还会做一些额外的事情，
    在这里我们希望它做的额外事情就是去统计返回的 Category 记录的集合中每条记录下的文章数
    使用 filter 方法把 num_posts 的值小于 1 的分类过滤掉
    '''
    #Count('posts')  Posts必须小写 不能Count('Posts')
    return Category.objects.annotate(num_posts=Count('posts')).filter(num_posts__gt=0)

@register.simple_tag
def get_tags():
    # 记得在顶部引入 Tag model
    return Tag.objects.annotate(num_posts=Count('posts')).filter(num_posts__gt=0)
