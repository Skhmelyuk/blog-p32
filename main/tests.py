from django.test import TestCase
from django.template import Context, Template
from django.contrib.auth.models import User
from main.models import Category, Post

class CustomTagsAndFiltersTest(TestCase):

    def setUp(self):
        # Створення тестових даних
        self.user = User.objects.create_user(username='testuser', password='password', first_name='Іван')
        self.category = Category.objects.create(name='Технології', slug='tech')
        self.post = Post.objects.create(
            category=self.category,
            title='Тестова стаття про Django',
            slug='test-django',
            content='Django ' * 250,  # 250 слів
            author=self.user,
            views=21
        )

    def test_reading_time_filter(self):
        """Перевірка обчислення часу читання"""
        template = Template('{% load blog_filters %}{{ content|reading_time }}')
        
        # Тест для 250 слів (повинно бути 1 хвилина)
        context = Context({'content': self.post.content})
        rendered = template.render(context)
        self.assertEqual(rendered, '1 хвилина')

        # Тест для короткого тексту
        context_short = Context({'content': 'Короткий текст'})
        rendered_short = template.render(context_short)
        self.assertEqual(rendered_short, 'менше хвилини')

    def test_uk_plural_filter(self):
        """Перевірка правильного відмінювання українських іменників"""
        template = Template('{% load blog_filters %}{{ views|uk_plural:"перегляд,перегляди,переглядів" }}')
        
        # 21 перегляд
        rendered = template.render(Context({'views': 21}))
        self.assertEqual(rendered, '21 перегляд')

        # 24 перегляди
        rendered = template.render(Context({'views': 24}))
        self.assertEqual(rendered, '24 перегляди')

        # 25 переглядів
        rendered = template.render(Context({'views': 25}))
        self.assertEqual(rendered, '25 переглядів')

    def test_time_of_day_greeting_tag(self):
        """Перевірка роботи Simple Tag без контексту"""
        template = Template('{% load blog_tags %}{% time_of_day_greeting %}')
        rendered = template.render(Context({}))
        # Перевіряємо, чи повертається одне з валідних привітань
        self.assertIn(rendered, ["Доброго ранку", "Доброго дня", "Доброго вечора", "Доброї ночі"])

    def test_welcome_user_tag_authenticated(self):
        """Перевірка привітання для авторизованого користувача"""
        # Створюємо імітований запит
        class MockRequest:
            def __init__(self, user):
                self.user = user

        mock_request = MockRequest(self.user)
        template = Template('{% load blog_tags %}{% welcome_user %}')
        context = Context({'request': mock_request})
        rendered = template.render(context)
        self.assertEqual(rendered, 'Раді бачити, Іван!')

    def test_latest_posts_widget_inclusion_tag(self):
        """Перевірка роботи Inclusion Tag віджета останніх постів"""
        template = Template('{% load blog_tags %}{% show_latest_posts 1 %}')
        rendered = template.render(Context({}))
        self.assertIn('Тестова стаття про Django', rendered)
        self.assertIn('⚡ Останні публікації', rendered)
