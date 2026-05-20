from django.shortcuts import render, get_object_or_404
from .models import Post, Category


def post_list(request, category_slug=None):
    posts = Post.objects.all()
    current_category = None

    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        posts = Post.objects.filter(category=current_category)

    sort = request.GET.get('sort', 'new')  # default to 'new'
    if sort == 'new':
        posts = posts.order_by('-created_at')
    elif sort == 'old':
        posts = posts.order_by('created_at')
    elif sort == 'popular':
        posts = posts.order_by('-views')
    
    context = {
        "title": "Home page",
        "current_category": current_category,
        "posts": posts,
        "current_sort": sort
    }

    return render(request, "main/post_list.html", context)


def post_detail(request, id, slug):
    post = get_object_or_404(Post, id=id, slug=slug)
    post.views += 1
    post.save()

    related_posts = Post.objects.filter(category=post.category).exclude(id=post.id)[:4]

    return render(request, 'main/post_details.html', {
        'post': post,
        'related_posts': related_posts,
        'current_category': post.category
    })
