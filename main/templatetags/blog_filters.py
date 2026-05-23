import re
from django import template

register = template.Library()

# ==========================================
# Кастомні фільтри
# ==========================================

@register.filter(name='reading_time')
def reading_time(value):
    """
    Обчислює приблизний час читання тексту в хвилинах (середня швидкість 200 слів/хв).
    Використання в шаблоні: {{ post.content|reading_time }}
    """
    if not value:
        return "менше хвилини"
    
    # Очищуємо текст від HTML-тегів
    clean_text = re.sub(r'<[^>]+>', '', str(value))
    words_count = len(clean_text.split())
    minutes = round(words_count / 200)
    
    if minutes < 1:
        return "менше хвилини"
    
    # Правильне відмінювання українського слова "хвилина"
    if minutes % 10 == 1 and minutes % 100 != 11:
        suffix = "хвилина"
    elif minutes % 10 in [2, 3, 4] and not (minutes % 100 in [12, 13, 14]):
        suffix = "хвилини"
    else:
        suffix = "хвилин"
        
    return f"{minutes} {suffix}"


@register.filter(name='uk_plural')
def uk_plural(value, arg):
    """
    Повертає правильну форму іменника в залежності від числа.
    Передається 3 форми через кому: "однина,двоїна,множина"
    Використання в шаблоні: {{ post.views|uk_plural:"перегляд,перегляди,переглядів" }}
    """
    try:
        number = int(value)
    except (ValueError, TypeError):
        return f"{value} {arg}"

    forms = arg.split(',')
    if len(forms) != 3:
        return f"{number} {arg}"

    # Логіка відмінювання для української мови
    if number % 10 == 1 and number % 100 != 11:
        chosen_form = forms[0]
    elif number % 10 in [2, 3, 4] and not (number % 100 in [12, 13, 14]):
        chosen_form = forms[1]
    else:
        chosen_form = forms[2]

    return f"{number} {chosen_form}"
