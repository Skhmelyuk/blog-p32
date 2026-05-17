

from django.shortcuts import render, get_object_or_404
from .models import Post, Category


def post_list(request, category_slug=None):
    posts = Post.objects.all()
    categories = Category.objects.all()

    category = None

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        posts = Post.objects.filter(category=category)

    
    context = {
        "title": "Home page",
        "categories": categories,
        "category": category,
        "posts": posts
    }

    return render(request, "main/post_list.html", context)
    



