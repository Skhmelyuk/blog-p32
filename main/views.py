from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category
from .forms import PostForm, ContactForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail


def post_list(request, category_slug=None):

    posts = Post.objects.all()
    categories = Category.objects.all()
    current_category = None

    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        posts = Post.objects.filter(category=current_category)

    sort = request.GET.get('sort', 'new')

    if sort == 'new':
        posts = posts.order_by('-created_at')
    elif sort == 'old':
        posts = posts.order_by('created_at')
    elif sort == 'popular':
        posts = posts.order_by('-views')

    context = {
        "title": "Home page",
        "current_category": current_category,
        "categories": categories,
        "posts": posts,
        "current_sort": sort
    }

    return render(request, "main/post_list.html", context)


def post_detail(request, id, slug):

    post = get_object_or_404(Post, id=id, slug=slug)
    post.views += 1
    post.save()

    related_posts = Post.objects.filter(category=post.category).exclude(id=post.id)[:4]
    categories = Category.objects.all()
    

    return render(request, 'main/post_details.html', {
        "title": post.title,
        'post': post,
        'related_posts': related_posts,
        'current_category': post.category,
        "categories": categories,
    })

@login_required(login_url='accounts:login')
def post_create(request):
        # Перевіряємо, чи є авторизований користувач адміністратором (суперкористувачем)
    if not request.user.is_superuser:
        raise PermissionDenied("У вас немає прав для створення публікації.")

    categories = Category.objects.all()

    if request.method == 'POST':
        # Передаємо POST-дані та завантажені файли (FILES) у форму
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            # Зберігаємо об'єкт у пам'яті, але не записуємо в БД відразу (commit=False)
            post = form.save(commit=False)
            # Призначаємо поточного користувача автором поста
            post.author = request.user
            # Тепер остаточно зберігаємо запис у базу даних
            post.save()
            # Перенаправляємо на детальну сторінку новоствореного поста
            return redirect(post.get_absolute_url())
    else:
        # При GET-запиті ініціалізуємо порожню форму
        form = PostForm()

    return render(request, 'main/post_create.html', {
        'form': form,
        'categories': categories,
        'title': 'Створення публікації'
    })


def contact_view(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Отримуємо валідовані дані з форми
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message_text = form.cleaned_data['message']
            
            # Формуємо вміст листа для адміністратора
            email_subject = f"Нове повідомлення: {subject}"
            email_message = f"Отримано нове звернення через контактну форму сайту.\n\n" \
                            f"Від кого: {name}\n" \
                            f"Email відправника: {email}\n\n" \
                            f"Текст повідомлення:\n{message_text}"
            
            # Спроба надіслати лист
            try:
                send_mail(
                    subject=email_subject,
                    message=email_message,
                    from_email=email,  # Email відправника (або DEFAULT_FROM_EMAIL)
                    recipient_list=['skhmelyuk1985@gmail.com'],  # Введіть реальну пошту адміністратора
                    fail_silently=False,
                )
                
        
                messages.success(
                    request, 
                    "Дякуємо! Ваше повідомлення успішно надіслано на пошту адміністратора."
                )
                return redirect('main:contact')
                
            except Exception as e:
                # Обробка помилки у разі проблем зі зв'язком/сервером
                messages.error(
                    request, 
                    "Виникла помилка при відправленні листа. Будь ласка, спробуйте пізніше."
                )
                # Також можна вивести помилку в логи для діагностики:
                print(f"Помилка відправлення пошти: {e}")
    else:
        form = ContactForm()

    return render(request, 'main/contact.html', {
        'form': form,
        'categories': categories,
        'title': 'Контакти'
    })


    



