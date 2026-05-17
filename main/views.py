from django.shortcuts import render
from .models import Post


def post_list(request):

    posts = Post.objects.all().order_by('-created_at')
    context = {"title": "Home page", "posts": posts}

    return render(request, "main/posts_list.html", context)
    
