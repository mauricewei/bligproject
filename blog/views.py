import markdown
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Post, Category, Tag
from comments.forms import CommentForm
from django.db.models import Q

#def index(request):
#    post_list = Post.objects.all()
#    render(request, 'blog/index.html', {'post_list': post_list})
# 转换为等价的类视图
class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')
        pagination_data = self.pagination_data(paginator, page, is_paginated)
        context.update(pagination_data)
        return context
    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            return {}
        left = []
        right = []
        left_has_more = False
        right_has_more = False
        first = False
        last = False

        page_number = page.number
        total_pages = paginator.num_pages
        page_range = paginator.page_range

        if page_number == 1:
            right = page_range[page_number:page_number + 2]
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
        elif page_number == total_pages:
            left = page_range[(page_number - 3) if (page_number -3) > 0 else 0:page_number -1]
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
        else:
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else
            0:page_number -1]
            right = page_range[page_number:page_number + 2]
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }
        return data

#def detail(request, pk):
#    post = get_object_or_404(Post, pk=pk)
#    post.increase_views()
#    post.body = markdown.markdown(post.body,
#                                  extensions=[
#                                    'markdown.extensions.extra',
#                                    'markdown.extensions.codehilite',
#                                    'markdown.extensions.toc'
#                                  ])
#    form = CommentForm()
#    comment_list = post.comment_set.all()
#    context = {'post': post, 'form': form, 'comment_list': comment_list}
#    return render(request, 'blog/detail.html', context)
# 转换为等价的类视图
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
# DetailView默认使用'post'传递给模版，所以context_object_name可以不指定
#    context_object_name = 'post'

    # 重写get函数，增加阅读量+1的功能 
    def get(self, request, *args, **kwargs):
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        self.object.increase_views()
        return response
    # 重写get_object函数，增加对body的markdown渲染
#    def get_object(self, queryset=None):
#        post = super(PostDetailView, self).get_object(queryset=None)
    def get_object(self):
        post = super().get_object()
        md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite', 
                TocExtension(slugify=slugify),
                ])
        post.body = md.convert(post.body)
        post.toc = md.toc
        return post
    # 重写get_context_date函数，增加表单和评论列表功能
    def get_context_data(self, **kwargs):
#        context = super(PostDetailView, self).get_context_data(**kwargs)
        # 可以简写为
        context = super().get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
                'form': form,
                'comment_list': comment_list,
                })
        return context

#def archives(request, year, month):
#    post_list = Post.objects.filter(created_time__year=year,
#            created_time__month=month).order_by('-created_time')
#    return render(request, 'blog/index.html', {'post_list': post_list})
# 转换为等价的类视图
class ArchivesView(IndexView):
    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')

#        return super(ArchivesView,
#                self).get_queryset().filter(created_time__year=year,
#                    created_time__month=month)
        # 上面一行可以替换为如下简单写法 
        return Post.objects.filter(created_time__year=year,
                created_time__month=month)

#def category(request, pk):
#    cate = get_object_or_404(Category, pk=pk)
#    post_list = Post.objects.filter(category=cate).order_by('-created_time')
#    return render(request, 'blog/index.html', context={'post_list': post_list})
# 转换为等价的类视图
class CategoryView(IndexView):
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
#        return super(CategoryView, self).get_queryset().filter(category=cate)
        # 上面一行可以替换为如下简单写法 
        return Post.objects.filter(category=cate)

#def get_specified_author_posts(request, pk):
#    post = Post.objects.get(pk=pk)
#    post_list = Post.objects.filter(author=post.author)
#    return render(request, 'blog/index.html', {'post_list': post_list})
# 转换为等价的类视图
class AuthorPostView(IndexView):
    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
#        return super(AuthorPostView, self).get_queryset().filter(author=post.author)
        # 上面一行可以替换为如下简单写法 
        return Post.objects.filter(author=post.author)

class TagView(IndexView):
    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return Post.objects.filter(tags=tag)

#def search(request):
#    q = request.GET.get('q')
#    error_msg = ''
#    if not q:
#        error_msg = "请输入关键字"
#    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
#    return render(request, 'blog/index.html', {'error_msg': error_msg,
#            'post_list': post_list})
# 转换为等价的类视图
class SearchView(IndexView):
    keywords = None
    error_msg = ''
    # 复写get函数，获取模版传过来的 keywords 变量
    def get(self, request, *args, **kwargs):
        self.keywords = request.GET.get('keywords')
        # get方法会先执行 get_queryset 和 get_context_data，此时我们复写
        # 的 get_queryset 函数已经可以使用 get 方法中获取到的 keywords 变量
        response = super().get(request, *args, **kwargs)
        return response
    # 根据关键字获取 post_list
    def get_queryset(self):
        keywords = self.keywords
        return Post.objects.filter(Q(title__icontains=keywords) |
                Q(body__icontains=keywords))
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.keywords:
            self.error_msg = '请输入关键字！'
        context.update({'error_msg': self.error_msg})
        return context
