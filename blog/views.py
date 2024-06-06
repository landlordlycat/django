from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy,reverse
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from django.db.models import Q
from .forms import PubBlogForm
from .models import BlogCategory, Blog, BlogComment


def index(request):
    blogs = Blog.objects.all()
    return render(request, 'index.html',context={'blogs':blogs})


def blog_details(request, blog_id):
    try:
        blog = Blog.objects.get(pk=blog_id)
    except Exception as e:
        blog = None
    return render(request, 'blog_detail.html', context={'blog': blog})


@require_http_methods(['GET', 'POST'])
@login_required(login_url=reverse_lazy('blogauth:zllogin'))
def pub_blog(request):
    print(request)
    if request.method == 'GET':
        categories = BlogCategory.objects.all()
        return render(request, 'pub_blog.html', context={'categories': categories})
    else:
        form = PubBlogForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            category_id = form.cleaned_data.get('category')
            blog =Blog.objects.create(title=title, content=content, category_id=category_id, author=request.user)
            return JsonResponse({'code': '200','message': '发布成功',"data":{"blog_id":blog.id}})
        else:
            return JsonResponse({'code': '400','message': '发布失败'})


@require_POST
@login_required()
def pub_comment(request):
    blog_id = request.POST.get('blog_id')
    content = request.POST.get('content')
    BlogComment.objects.create(content=content, blog_id=blog_id, author=request.user)
    return redirect(reverse('blog:blog_details',kwargs={'blog_id':blog_id}))

@require_GET
def search(request):
    kw = request.GET.get('q')
    blogs = Blog.objects.filter(Q(title__icontains=kw)|Q(content__icontains=kw)).all()
    return  render(request,'index.html',context={'blogs':blogs})