from django.shortcuts import render,get_object_or_404,redirect,reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from .models import Posts,Category,Tag
from comments.models import Comment
from django.views.generic import View
import markdown
import re
from django.db.models import Q

# Create your views here.
class firstView(View):
    def get(self, request):
        all_list = Posts.objects.all().order_by('-create_time')
        paginator = Paginator(all_list, 7)
        pagenum = 1
        try:
            p = paginator.page(pagenum)
        except PageNotAnInteger:
            p = paginator.page(1)
        except EmptyPage:
            # 超过最大的页数显示最后一页
            p = paginator.page(paginator.num_pages)

        post_list = p
        page_range = paginator.page_range
        maxnum = paginator.num_pages

        if maxnum > 7:
            if pagenum - 3 < 1:
                page_range = range(1, 8)
            elif pagenum + 3 > maxnum:
                page_range = range(maxnum - 6, maxnum + 1)
            else:
                page_range = range(pagenum - 2, pagenum + 4)

        return render(request, 'index.html', context={'post_list': post_list, 'range': page_range, 'maxnum': maxnum,'paginator':paginator,'current_page':p,'pagenum':pagenum})

class indexView(View):
    def get(self,request,pagenum):
        all_list = Posts.objects.all().order_by('-create_time')
        paginator = Paginator(all_list,7)
        if pagenum == '':
           pagenum = '1'
        pagenum = int(pagenum)
        try:
            page = paginator.page(pagenum)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            #超过最大的页数显示最后一页
            page = paginator.page(paginator.num_pages)
        post_list = page
        page_range = paginator.page_range
        maxnum = paginator.num_pages
        if maxnum > 7:
            if pagenum - 3 < 1:
                page_range = range(1,8)
            elif pagenum + 3 > maxnum:
                page_range = range(maxnum-6,maxnum+1)
            else:
                page_range = range(pagenum-2,pagenum+4)

        return render(request,'index.html',context={'post_list': post_list,'range':page_range,'maxnum':maxnum,'paginator':paginator,'current_page':page,'pagenum':pagenum})

class singleView(View):
    def get(self,request,pk):
        '''
        从 django.shortcuts 模块导入的 get_object_or_404 方法
        是当传入的 pk 对应的 Post 在数据库存在时，就返回对应的 post，
        如果不存在，就给用户返回一个 404 错误，表明用户请求的文章不存在
        '''
        post = get_object_or_404(Posts, pk=pk)
        post.increase_views()
        comment_list = post.comment_set.all()
        pagenum = 1
        #codehilite为高亮拓展
        #toc为自动生成目录
        md = markdown.Markdown(extensions=[
                                     'markdown.extensions.extra',
                                     'markdown.extensions.codehilite',
                                     'markdown.extensions.toc',
                                     TocExtension(slugify=slugify),
                                  ])
        post.body = md.convert(post.body)
        post.toc = md.toc
        return render(request,'single.html',context={'post':post,'comment_list':comment_list,'pagenum':pagenum})

class archivesView(View):
    def get(self,request,year,month,pagenum):
        all_list = Posts.objects.filter(create_time__year=year,
                                         create_time__month=month
                                         ).order_by('-create_time')
        paginator = Paginator(all_list, 7)
        if pagenum == '':
            pagenum = '1'
        pagenum = int(pagenum)
        try:
            page = paginator.page(pagenum)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            # 超过最大的页数显示最后一页
            page = paginator.page(paginator.num_pages)
        post_list = page
        page_range = paginator.page_range
        maxnum = paginator.num_pages
        if maxnum > 7:
            if pagenum - 3 < 1:
                page_range = range(1, 8)
            elif pagenum + 3 > maxnum:
                page_range = range(maxnum - 6, maxnum + 1)
            else:
                page_range = range(pagenum - 2, pagenum + 4)

        return render(request,'index.html',context={'post_list':post_list,'range':page_range,'maxnum':maxnum,'paginator':paginator,'current_page':page,'pagenum':pagenum})

class first_archivesView(View):
    def get(self, request, year, month):
        all_list = Posts.objects.filter(create_time__year=year,
                                        create_time__month=month
                                        ).order_by('-create_time')
        paginator = Paginator(all_list, 7)

        pagenum = 1
        try:
            page = paginator.page(pagenum)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            # 超过最大的页数显示最后一页
            page = paginator.page(paginator.num_pages)
        post_list = page
        page_range = paginator.page_range
        maxnum = paginator.num_pages
        if maxnum > 7:
            if pagenum - 3 < 1:
                page_range = range(1, 8)
            elif pagenum + 3 > maxnum:
                page_range = range(maxnum - 6, maxnum + 1)
            else:
                page_range = range(pagenum - 2, pagenum + 4)

        return render(request, 'index.html',
                      context={'post_list': post_list, 'range': page_range, 'maxnum': maxnum, 'paginator': paginator,
                               'current_page': page, 'pagenum': pagenum})

class categoryView(View):
    def get(self,request,pk,pagenum):
        cate = get_object_or_404(Category,pk=pk)
        all_list = Posts.objects.filter(category=cate).order_by('-create_time')
        paginator = Paginator(all_list, 7)
        if pagenum == '':
            pagenum = '1'
        pagenum = int(pagenum)
        try:
            page = paginator.page(pagenum)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            # 超过最大的页数显示最后一页
            page = paginator.page(paginator.num_pages)
        post_list = page
        page_range = paginator.page_range
        maxnum = paginator.num_pages
        if maxnum > 7:
            if pagenum - 3 < 1:
                page_range = range(1, 8)
            elif pagenum + 3 > maxnum:
                page_range = range(maxnum - 6, maxnum + 1)
            else:
                page_range = range(pagenum - 2, pagenum + 4)

        return render(request, 'index.html', context={'post_list': post_list, 'range': page_range, 'maxnum': maxnum, 'paginator': paginator,'current_page': page,'pagenum':pagenum})

class first_categoryView(View):
    def get(self,request,pk):
        cate = get_object_or_404(Category,pk=pk)
        all_list = Posts.objects.filter(category=cate).order_by('-create_time')
        paginator = Paginator(all_list, 7)

        pagenum = 1
        try:
            page = paginator.page(1)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            # 超过最大的页数显示最后一页
            page = paginator.page(paginator.num_pages)
        post_list = page
        page_range = paginator.page_range
        maxnum = paginator.num_pages
        if maxnum > 7:
            if pagenum - 3 < 1:
                page_range = range(1, 8)
            elif pagenum + 3 > maxnum:
                page_range = range(maxnum - 6, maxnum + 1)
            else:
                page_range = range(pagenum - 2, pagenum + 4)

        return render(request, 'index.html', context={'post_list': post_list, 'range': page_range, 'maxnum': maxnum, 'paginator': paginator,'current_page': page,'pagenum':1})

class commentView(View):
    def post(self,request,post_pk):
        name = request.POST.get('name')
        email = request.POST.get('email')
        url = request.POST.get('url')
        comment = request.POST.get('comment')
        post = get_object_or_404(Posts,pk=post_pk)

        if not all([name,email,url,comment]):
            return render(request, 'single.html', {'errmsg': '数据不完整'})

        #邮箱校验
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'single.html', {'errmsg': '邮箱格式不正确'})

        com = Comment(name = name,email=email,url=url,text=comment,post=post)
        com.save()

        return redirect(post.get_pk_url())

class tagView(View):
    def get(self,request,pk,pagenum):
        tag = get_object_or_404(Tag,pk=pk)
        all_list = Posts.objects.filter(tags=tag).order_by('-create_time')
        paginator = Paginator(all_list, 7)
        if pagenum == '':
            pagenum = '1'
        pagenum = int(pagenum)
        try:
            page = paginator.page(pagenum)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            # 超过最大的页数显示最后一页
            page = paginator.page(paginator.num_pages)
        post_list = page
        page_range = paginator.page_range
        maxnum = paginator.num_pages
        if maxnum > 7:
            if pagenum - 3 < 1:
                page_range = range(1, 8)
            elif pagenum + 3 > maxnum:
                page_range = range(maxnum - 6, maxnum + 1)
            else:
                page_range = range(pagenum - 2, pagenum + 4)

        return render(request, 'index.html', context={'post_list': post_list, 'range': page_range, 'maxnum': maxnum, 'paginator': paginator,'current_page': page,'pagenum':pagenum})

class firsttagView(View):
    def get(self,request,pk):
        tag = get_object_or_404(Tag,pk=pk)
        all_list = Posts.objects.filter(tags=tag).order_by('-create_time')
        paginator = Paginator(all_list, 7)

        pagenum = 1
        try:
            page = paginator.page(pagenum)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            # 超过最大的页数显示最后一页
            page = paginator.page(paginator.num_pages)
        post_list = page
        page_range = paginator.page_range
        maxnum = paginator.num_pages
        if maxnum > 7:
            if pagenum - 3 < 1:
                page_range = range(1, 8)
            elif pagenum + 3 > maxnum:
                page_range = range(maxnum - 6, maxnum + 1)
            else:
                page_range = range(pagenum - 2, pagenum + 4)

        return render(request, 'index.html', context={'post_list': post_list, 'range': page_range, 'maxnum': maxnum, 'paginator': paginator,'current_page': page,'pagenum':pagenum})

class single_archivesView(View):
    def get(self,request,year,month,pagenum):
        all_list = Posts.objects.filter(create_time__year=year,
                                         create_time__month=month
                                         ).order_by('-create_time')
        paginator = Paginator(all_list, 7)
        if pagenum == '':
            pagenum = '1'
        pagenum = int(pagenum)
        try:
            page = paginator.page(pagenum)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            # 超过最大的页数显示最后一页
            page = paginator.page(paginator.num_pages)
        post_list = page
        page_range = paginator.page_range
        maxnum = paginator.num_pages
        if maxnum > 7:
            if pagenum - 3 < 1:
                page_range = range(1, 8)
            elif pagenum + 3 > maxnum:
                page_range = range(maxnum - 6, maxnum + 1)
            else:
                page_range = range(pagenum - 2, pagenum + 4)

        return render(request,'single.html',context={'post_list':post_list,'range':page_range,'maxnum':maxnum,'paginator':paginator,'current_page':page,'pagenum':pagenum})

class first_single_archivesView(View):
    def get(self,request,year,month):
        all_list = Posts.objects.filter(create_time__year=year,
                                         create_time__month=month
                                         ).order_by('-create_time')
        paginator = Paginator(all_list, 7)

        pagenum = 1
        try:
            page = paginator.page(pagenum)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            # 超过最大的页数显示最后一页
            page = paginator.page(paginator.num_pages)
        post_list = page
        page_range = paginator.page_range
        maxnum = paginator.num_pages
        if maxnum > 7:
            if pagenum - 3 < 1:
                page_range = range(1, 8)
            elif pagenum + 3 > maxnum:
                page_range = range(maxnum - 6, maxnum + 1)
            else:
                page_range = range(pagenum - 2, pagenum + 4)

        return render(request,'single.html',context={'post_list':post_list,'range':page_range,'maxnum':maxnum,'paginator':paginator,'current_page':page,'pagenum':pagenum})

class single_categoryView(View):
    def get(self,request,pk,pagenum):
        cate = get_object_or_404(Category,pk=pk)
        all_list = Posts.objects.filter(category=cate).order_by('-create_time')
        paginator = Paginator(all_list, 7)
        if pagenum == '':
            pagenum = '1'
        pagenum = int(pagenum)
        try:
            page = paginator.page(pagenum)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            # 超过最大的页数显示最后一页
            page = paginator.page(paginator.num_pages)
        post_list = page
        page_range = paginator.page_range
        maxnum = paginator.num_pages
        if maxnum > 7:
            if pagenum - 3 < 1:
                page_range = range(1, 8)
            elif pagenum + 3 > maxnum:
                page_range = range(maxnum - 6, maxnum + 1)
            else:
                page_range = range(pagenum - 2, pagenum + 4)

        return render(request, 'single.html', context={'post_list': post_list, 'range': page_range, 'maxnum': maxnum, 'paginator': paginator,'current_page': page,'pagenum':pagenum})

class first_single_categoryView(View):
    def get(self,request,pk):
        cate = get_object_or_404(Category,pk=pk)
        all_list = Posts.objects.filter(category=cate).order_by('-create_time')
        paginator = Paginator(all_list, 7)
        pagenum = 1
        try:
            page = paginator.page(pagenum)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            # 超过最大的页数显示最后一页
            page = paginator.page(paginator.num_pages)
        post_list = page
        page_range = paginator.page_range
        maxnum = paginator.num_pages
        if maxnum > 7:
            if pagenum - 3 < 1:
                page_range = range(1, 8)
            elif pagenum + 3 > maxnum:
                page_range = range(maxnum - 6, maxnum + 1)
            else:
                page_range = range(pagenum - 2, pagenum + 4)

        return render(request, 'single.html', context={'post_list': post_list, 'range': page_range, 'maxnum': maxnum, 'paginator': paginator,'current_page': page,'pagenum':1})

class single_tagView(View):
    def get(self,request,pk,pagenum):
        tag = get_object_or_404(Tag,pk=pk)
        all_list = Posts.objects.filter(tags=tag).order_by('-create_time')
        paginator = Paginator(all_list, 7)
        if pagenum == '':
            pagenum = '1'
        pagenum = int(pagenum)
        try:
            page = paginator.page(pagenum)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            # 超过最大的页数显示最后一页
            page = paginator.page(paginator.num_pages)
        post_list = page
        page_range = paginator.page_range
        maxnum = paginator.num_pages
        if maxnum > 7:
            if pagenum - 3 < 1:
                page_range = range(1, 8)
            elif pagenum + 3 > maxnum:
                page_range = range(maxnum - 6, maxnum + 1)
            else:
                page_range = range(pagenum - 2, pagenum + 4)

        return render(request, 'single.html', context={'post_list': post_list, 'range': page_range, 'maxnum': maxnum, 'paginator': paginator,'current_page': page,'pagenum':pagenum})

class first_single_tagView(View):
    def get(self,request,pk):
        tag = get_object_or_404(Tag,pk=pk)
        all_list = Posts.objects.filter(tags=tag).order_by('-create_time')
        paginator = Paginator(all_list, 7)

        pagenum = 1
        try:
            page = paginator.page(pagenum)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            # 超过最大的页数显示最后一页
            page = paginator.page(paginator.num_pages)
        post_list = page
        page_range = paginator.page_range
        maxnum = paginator.num_pages
        if maxnum > 7:
            if pagenum - 3 < 1:
                page_range = range(1, 8)
            elif pagenum + 3 > maxnum:
                page_range = range(maxnum - 6, maxnum + 1)
            else:
                page_range = range(pagenum - 2, pagenum + 4)

        return render(request, 'single.html', context={'post_list': post_list, 'range': page_range, 'maxnum': maxnum, 'paginator': paginator,'current_page': page,'pagenum':pagenum})


def search(request):
    q = request.GET.get('q')
    error_msg = ''

    if not q:
        error_msg = "请输入关键词"
        return render(request, 'index.html', {'error_msg': error_msg})

    post_list = Posts.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'index.html', {'error_msg': error_msg,'post_list': post_list,'pagenum':1})
