from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'image', 'category', 'slug')

        widgets = {
            'category': forms.Select(attrs={
                'class': 'form-input',
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Введіть заголовок публікації',
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Введіть унікальний слаг для URL (наприклад: my-new-post)',
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-input',
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 8,
                'placeholder': 'Напишіть текст публікації тут...',
            }),
        }

        labels = {
            'category': 'Категорія',
            'title': 'Заголовок статті',
            'slug': 'Слаг (URL-ідентифікатор)',
            'image': 'Обкладинка публікації',
            'content': 'Текст публікації',
        }


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label="Ваше ім'я",
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': "Введіть ваше ім'я"
        })
    )
    email = forms.EmailField(
        label="Ваш Email",
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': "name@example.com"
        })
    )
    subject = forms.CharField(
        max_length=200,
        label="Тема повідомлення",
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': "Тема звернення"
        })
    )
    message = forms.CharField(
        label="Текст повідомлення",
        widget=forms.Textarea(attrs={
            'class': 'form-input',
            'rows': 6,
            'placeholder': "Напишіть ваше повідомлення тут..."
        })
    )