import re
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

from .models import Profile, User

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



class ChangeUserForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email')

        CLASS_FOR_FIELDS = 'input input-bordered w-full focus:ring-2 focus:ring-primary bg-white text-gray-800'
        
        widgets = {
            'username': forms.TextInput(attrs={
                'class': CLASS_FOR_FIELDS,
                'placeholder': 'Имя пользователя',
            }),
            'first_name': forms.TextInput(attrs={
                'class': CLASS_FOR_FIELDS,
                'placeholder': 'Имя'
            }),
            'last_name': forms.TextInput(attrs={
                'class': CLASS_FOR_FIELDS,
                'placeholder': 'Фамилия'
            }),
            'email': forms.EmailInput(attrs={
                'class': CLASS_FOR_FIELDS,
                'placeholder': 'Электронная почта'
            }),
        }

        labels = {
            'username': 'Имя пользователя',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Почта',
        }


class ChangeProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('description', 'short_description', 'phone_number')

        CLASS_FOR_FIELDS = 'p-2 rounded-lg w-full focus:outline-none focus:ring-2 focus:ring-blue-300 bg-white text-gray-800'
        widgets = {
            'description': forms.Textarea(attrs={
                'class': CLASS_FOR_FIELDS,
                'placeholder': 'Описание профиля',
                'rows': '5',
            }),
            'short_description': forms.TextInput(attrs={
                'class': CLASS_FOR_FIELDS,
                'placeholder': 'Имя пользователя',
            }),
            'phone_number': forms.TextInput(attrs={
                'class': CLASS_FOR_FIELDS,
                'placeholder': 'Имя пользователя',
                'type': 'tel'
            }),
        }

        labels = {
            'description': 'Описание',
            'short_description': 'Краткое описание',
            'phone_number': 'Номер телефона',
        }
    
    def clean_phone_number(self):
        phone = self.cleaned_data['phone_number']
        if phone is None:
            return phone
        
        normalized_phone = re.sub(r'[\s\-\(\)]', '', phone)

        # Заменяется первая 8 на +7
        if normalized_phone.startswith('8'):
            normalized_phone = '+7' + normalized_phone[1:]
        elif normalized_phone.startswith('7'):
            normalized_phone = '+7' + normalized_phone[1:]
        elif not normalized_phone.startswith('+7'):
            raise forms.ValidationError('Номер должен начинаться с +7 или 8.')

        if not re.match(r'^\+7\d{10}$', normalized_phone):
            raise forms.ValidationError('Введите корректный номер телефона.')
        
        return phone
