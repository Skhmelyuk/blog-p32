from django.shortcuts import render, HttpResponse


def post_list(request):

    posts = [
        {
            "id": "1",
            "title": "Django install",
            "content": "With Django, you can take web applications from concept to launch in a matter of hours. Django takes care of much of the hassle of web development, so you can focus on writing your app without needing to reinvent the wheel. It’s free and open source.",
        },
        {
            "id": "2",
            "title": "Python install",
            "content": "With Django, you can take web applications from concept to launch in a matter of hours. Django takes care of much of the hassle of web development, so you can focus on writing your app without needing to reinvent the wheel. It’s free and open source.",
        },
        {
            "id": "3",
            "title": "HTML shablon",
            "content": "With Django, you can take web applications from concept to launch in a matter of hours. Django takes care of much of the hassle of web development, so you can focus on writing your app without needing to reinvent the wheel. It’s free and open source.",
        }
    ]

    context = {"title": "Home page", "posts": posts}

    # return render(request, "main/posts_list.html", context)
    return HttpResponse("Привіт юзер! Чим я можу вам допомогти?")
