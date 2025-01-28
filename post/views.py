from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from urllib.parse import urlencode
from .models import Post, Tag
from django.db.models import Q





from django.utils import timezone
from collections import deque
from user.models import UserSession, Post

# Global memory store
session_cache = deque(maxlen=20)

def get_or_create_user_session(request, post=None):
    ip_address = request.META.get('REMOTE_ADDR') or request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0].strip()

    if not ip_address:
        # Handle cases where no IP address is available
        raise ValueError("No IP address found")

    # Check in the global memory store
    for cached_session in session_cache:
        if cached_session.ip == ip_address:
            if post and post not in cached_session.visited_posts.all():
                cached_session.visited_posts.add(post)
                cached_session.save()
            return cached_session

    # Check the database if not found in cache
    existing_session = UserSession.objects.filter(ip=ip_address).first()

    if existing_session:
        if post and post not in existing_session.visited_posts.all():
            existing_session.visited_posts.add(post)
            existing_session.save()
        # Update cache
        session_cache.append(existing_session)
        return existing_session

    # Create a new session if not found
    new_session = UserSession.objects.create(
        ip=ip_address
    )
    if post:
        new_session.visited_posts.add(post)
    new_session.save()

    # Update cache
    session_cache.append(new_session)

    return new_session
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
#    session = get_or_create_user_session(request,post)
#    print(session)
    return render(request, 'post_detail.html', {'post': post,"dev":"конец",},)


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

    paginator = Paginator(posts, 9)
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


def privacy(request):
    return render(request, 'privacy.html')


def tiktok(request):
    return render(request, 'tiktok.html')



def custom_404_view(request, exception):
    return render(request, '404.html', status=404)
