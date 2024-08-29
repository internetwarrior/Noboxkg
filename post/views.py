from django.shortcuts import render,  get_object_or_404
from django.core.paginator import Paginator
from .models import Post, Tag


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'post_detail.html', {'post': post})





from django.db.models import Q
from django.core.paginator import Paginator

def home_view(request):
    # Fetch all tags
    tags = Tag.objects.all()

    # Retrieve selected tag IDs from query parameters
    tag_ids = request.GET.getlist('filter')  # 'filter' is the query parameter name

    if tag_ids:
        # Convert tag_ids to integers
        tag_ids = [int(tag_id) for tag_id in tag_ids]

        # Start with all posts
        posts = Post.objects.filter(state__in=["active", "archived"]).order_by('-date')

        # Apply filtering to only include posts with all selected tags
        for tag_id in tag_ids:
            posts = posts.filter(tags__id=tag_id)

        posts = posts.distinct()
    else:
        posts = Post.objects.filter(state__in=["active", "archived"]).order_by('-date')

    # Paginate the posts
    paginator = Paginator(posts, 6)  # Show 6 posts per page
    page_number = request.GET.get('page')  # Get the current page number from the query parameters
    page_obj = paginator.get_page(page_number)  # Get the page object for the current page

    # Prepare the context
    context = {
        'posts': page_obj.object_list,  # Paginated posts
        'page_obj': page_obj,  # Page object for pagination controls
        'tags': tags,  # Include tags in the context for filtering options
        'filter_params': request.GET.urlencode()  # Preserve query parameters for pagination links
    }

    return render(request, 'home.html', context)