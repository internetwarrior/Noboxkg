from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from urllib.parse import urlencode
from .models import Post, Tag
from django.db.models import Q


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'post_detail.html', {'post': post})


def home_view(request):
    tags = Tag.objects.all()
    tag_ids = request.GET.getlist('filter')

    if tag_ids:
        tag_ids = [int(tag_id) for tag_id in tag_ids]
        posts = Post.objects.filter(state__in=["active", "archived"])
        for tag_id in tag_ids:
            posts = posts.filter(tags__id=tag_id)
        posts = posts.distinct()
    else:
        posts = Post.objects.filter(state__in=["active", "archived"])

    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    query_params = request.GET.dict()
    if 'page' in query_params:
        del query_params['page']

    context = {
        'posts': page_obj.object_list,
        'page_obj': page_obj,
        'tags': tags,
        'filter_params': urlencode(query_params)
    }

    return render(request, 'home.html', context)


def tiktok(request):
    return render(request, 'tiktok.html')