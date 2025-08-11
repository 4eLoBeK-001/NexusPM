import re
from django import forms
from django.contrib.auth import get_user_model, login, authenticate
from django.contrib.auth.forms import AuthenticationForm

from users.widgets import CustomImageField

from .models import Feedback, Profile, SocialNetwork, Tag, User

CLASS_FOR_FIELDS = 'w-full px-4 py-3 text-slate-200 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition'

class LoginUserForm(AuthenticationForm):
    
    username = forms.CharField(
        label='Логин или email', 
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

    def clean(self):
        username_or_email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
    
        if username_or_email and '@' in username_or_email:
            try:
                user = User.objects.get(email=username_or_email)
                self.cleaned_data['username'] = user.username
            except User.DoesNotExist:
                raise forms.ValidationError("Пользователь с таким email не найден.")

        return super().clean()



class RegisterUserForm(forms.ModelForm):

    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'w-full px-4 py-3 text-slate-200 input-field rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition', 'fas': 'fa-lock'}))
    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput(attrs={'class': 'w-full px-4 py-3 text-slate-200 input-field rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition', 'fas': 'fa-lock'}))
    email = forms.EmailField(label='Почта', required=True, widget=forms.TextInput(attrs={'class': CLASS_FOR_FIELDS + ' input-field', 'id': 'email', 'fas': 'fa-envelope', 'placeholder': 'Введите почту'}))
    
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
        }

        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'username': 'Логин',
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
        fields = ('profile_picture', 'description', 'short_description', 'phone_number')

        CLASS_FOR_FIELDS = 'p-2 rounded-lg w-full focus:outline-none focus:ring-2 focus:ring-blue-300 bg-white text-gray-800'
        widgets = {
            'profile_picture': forms.FileInput(attrs={'class': 'hidden'}),
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
            'profile_picture': 'Аватарка',
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


class AddTagForm(forms.ModelForm):
    name = forms.CharField(label='Название тега', max_length=25, widget=forms.TextInput(attrs={'class': 'input input-bordered w-full focus:ring-2 focus:ring-primary bg-white text-gray-800'}))
    class Meta:
        model = Tag
        fields = ('name',)


class AddSocialnetworkForm(forms.Form):
    network = forms.ChoiceField(
        choices=SocialNetwork.SOCIAL_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'bg-white radio radio-info radio-sm'
        }),
        label='Выберите социальную сеть:'
    )
    username = forms.CharField(
        label='Ваш ник или ID',
        widget=forms.TextInput(attrs={'class': 'w-full px-4 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-blue-400'})
    )

    def __init__(self, *args, **kwargs):
        self.profile = kwargs.pop('profile', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        network = cleaned_data['network']

        if SocialNetwork.objects.filter(profile=self.profile, network=network).exists():
            raise forms.ValidationError(f'{network} уже привязан к вашему профилю')
        return cleaned_data




class PrivateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('hide_number', 'hide_email')

        labels = {
            'hide_number': 'Скрыть номер телефона',
            'hide_email': 'Скрыть электронную почту',
        }

        widgets = {
            'hide_number': forms.CheckboxInput(attrs={
                'class': 'form-checkbox h-5 w-5 text-indigo-600 transition duration-150 ease-in-out'
            }),
            'hide_email': forms.CheckboxInput(attrs={
                'class': 'form-checkbox h-5 w-5 text-indigo-600 transition duration-150 ease-in-out'
            }),
        }


class FeedBackForm(forms.ModelForm):
    class Meta:
        CLASS_FOR_FIELDS = 'w-full px-4 py-3 text-slate-700 bg-transparent border-b-2 border-gray-300 outline-none peer transition-colors'
        model = Feedback
        fields = ('username', 'email', 'content')

        widgets = {
            'username': forms.TextInput(attrs={'class': f'{CLASS_FOR_FIELDS} focus:border-purple-500', 'placeholder': ' '}),
            'email': forms.EmailInput(attrs={'class': f'{CLASS_FOR_FIELDS} focus:border-cyan-500', 'placeholder': ' '}),
            'content': forms.Textarea(attrs={'rows': 4, 'class': 'w-full px-4 py-3 text-slate-700 bg-transparent border-b-2 border-gray-300 focus:border-blue-500 outline-none peer transition-colors resize-none'}),
        }

        labels = {
            'username': 'Ваше имя',
            'email': 'Ваш email',
            'content': 'Ваше сообщение',
        }