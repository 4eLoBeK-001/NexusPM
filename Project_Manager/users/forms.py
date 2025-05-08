from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

from .models import User

CLASS_FOR_FIELDS = 'w-full px-4 py-3 text-slate-200 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition'

class LoginUserForm(AuthenticationForm):
    
    username = forms.CharField(
        label='Логин', 
        max_length=150, 
        widget=forms.TextInput(attrs=
            {'class': CLASS_FOR_FIELDS,
             'id': 'login',
             'placeholder': 'Введите логин',
             'fas': 'fa-user'
             })
    )

    password = forms.CharField(
        label='Пароль', 
        widget=forms.PasswordInput(attrs=
            {'class': CLASS_FOR_FIELDS,
             'id': 'password',
             'placeholder': '••••••••',
             'fas': 'fa-lock'
             })
    )

class RegisterUserForm(forms.ModelForm):

    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'w-full px-4 py-3 text-slate-200 input-field rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition', 'fas': 'fa-lock'}))
    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput(attrs={'class': 'w-full px-4 py-3 text-slate-200 input-field rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition', 'fas': 'fa-lock'}))

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password2']

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

        widgets = {
            'first_name': forms.TextInput(attrs=
                {'class': CLASS_FOR_FIELDS + ' input-field',
                 'id': 'first-name',
                 'placeholder': 'Имя',
            }),
            'last_name': forms.TextInput(attrs=
                {'class': CLASS_FOR_FIELDS + ' input-field',
                 'id': 'last-name',
                 'placeholder': 'Фамилия',
            }),
            'username': forms.TextInput(attrs=
                {'class': CLASS_FOR_FIELDS + ' input-field',
                 'id': 'login',
                 'fas': 'fa-user-edit',
                 'placeholder': 'Введите логин',
            }),
            'email': forms.TextInput(attrs=
                {'class': CLASS_FOR_FIELDS + ' input-field',
                 'id': 'email',
                 'fas': 'fa-envelope',
                 'placeholder': 'Введите почту',
            }),
        }

        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'username': 'Логин',
            'email': 'Почта'
        }