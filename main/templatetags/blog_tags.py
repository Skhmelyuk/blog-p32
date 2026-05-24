from datetime import datetime
from urllib.parse import quote
from django import template
from main.models import Post

register = template.Library()

# ==========================================
# Simple Tags (Прості теги)
# ==========================================

@register.simple_tag
def time_of_day_greeting():
    """
    Повертає привітання в залежності від поточного часу доби (без контексту).
    Використання в шаблоні: {% time_of_day_greeting %}
    """
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "Доброго ранку"
    elif 12 <= hour < 18:
        return "Доброго дня"
    elif 18 <= hour < 23:
        return "Доброго вечора"
    else:
        return "Доброї ночі"


@register.simple_tag(takes_context=True)
def welcome_user(context):
    """
    Повертає персоналізоване привітання для авторизованого користувача на основі контексту запиту.
    Використання в шаблоні: {% welcome_user %}
    """
    request = context.get('request')
    if not request or not request.user.is_authenticated:
        return "Вітаємо, гостю!"
    
    user = request.user
    name = user.get_full_name() or user.username
    role = " (Адміністратор)" if user.is_staff else ""
    return f"Раді бачити, {name}{role}!"


# ==========================================
# Inclusion Tags (Теги включення)
# ==========================================

@register.inclusion_tag('main/components/latest_posts_widget.html')
def show_latest_posts(limit=3):
    """
    Відображає віджет останніх публікацій сайту.
    Використання в шаблоні: {% show_latest_posts 3 %}
    """
    posts = Post.objects.all().order_by('-created_at')[:limit]
    return {'latest_posts': posts}



