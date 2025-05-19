from django import forms
from django.contrib.auth import get_user_model
from .models import Team


class AddModalTeamForm(forms.ModelForm):
    name = forms.CharField(
        label='Название команды', 
        widget=forms.TextInput(
            attrs={
            'class': 'input input-bordered w-full bg-white text-slate-800 border-1 border-gray-300 focus:border-primary focus:ring-2 focus:ring-primary/50 transition-all',
            'id': 'id_name'})
    )


    class Meta:
        model = Team
        fields = ('image', 'name')


class AddTeamForm(forms.ModelForm):

    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered text-lg w-full bg-white text-gray-800 focus:outline-none focus:ring-2 focus:ring-sky-500 focus:border-transparent',
            'placeholder': 'Имя проекта'
        }),
        label='Название'
    )
    
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'textarea textarea-bordered text-base w-full bg-white text-gray-800 focus:outline-none focus:ring-2 focus:ring-sky-500 focus:border-transparent h-24',
            'placeholder': 'Описание проекта',
            'rows': 5,
            'cols': 40
        }),
        label='Описание',
        required=False
    )
    
    # team_member = forms.ModelMultipleChoiceField(
    #     widget=forms.SelectMultiple(attrs={
    #         'class': 'select select-primary select-bordered w-full bg-white text-gray-800 focus:outline-none focus:ring-2 focus:ring-sky-500 focus:border-transparent h-auto min-h-12 py-2',
    #         'multiple': 'multiple',
    #         'data-placeholder': 'Выбор участников команды'
    #     }),
    #     queryset=get_user_model().objects.all(),
    #     label='Участники команды',
    #     help_text='С зажатым Ctrl/Cmd выберите несколько человек'
    # )

    class Meta:
        model = Team
        fields = ('name', 'description')
