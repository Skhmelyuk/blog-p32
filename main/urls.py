# pyrefly: ignore [missing-import]
from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.post_list, name="post_list"),
    path('posts/<slug:category_slug>/', views.post_list, name="post_list_by_category"),
    path('post/create/', views.post_create, name="post_create"),
    path('post/<int:id>/<slug:slug>/', views.post_detail, name="post_detail"),
    path('contact/', views.contact_view, name="contact"),
]

