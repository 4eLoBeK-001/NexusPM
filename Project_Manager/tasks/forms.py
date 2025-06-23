from django import forms

from .models import Status, Tag, Task


class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('name', 'status', 'priority')

        widgets = {
            'name': forms.TextInput(attrs={
                'class': (
                    'input w-full bg-white text-gray-800 border border-gray-300 '
                    'focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition duration-200'
                ),
                'placeholder': 'Введите название задачи'
            }),
            'status': forms.Select(attrs={
                'class': (
                    'select w-full bg-white text-gray-800 border border-gray-300 '
                    'focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition duration-200'
                )
            }),
            'priority': forms.Select(attrs={
                'class': (
                    'select w-full bg-white text-gray-800 border border-gray-300 '
                    'focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition duration-200'
                )
            }),
        }

        labels = {
            'name': 'Название',
            'status': 'Статус',
            'priority': 'Приоритет'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Устанавливает отображение приоритетов label как value (вместо англ - русский)
        self.fields['priority'].choices = [
            (choice.value, choice.value) for choice in Task.PriprityChoices
        ]



class UpdateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('name', 'description')

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'text-xl font-bold w-full border-none focus:ring-0 bg-transparent p-0',
            }),
            'description': forms.Textarea(attrs={
                'class': 'mt-2 w-full text-gray-700 border border-gray-300 rounded-md p-2 resize-none focus:outline-none focus:ring-1 focus:ring-blue-400 focus:border-blue-400 bg-gray-100', 
                'rows': '6'
            }),
        }

        labels = {
            'name': 'Название',
            'description': 'Описание'
        }



class UpdateTagForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('tag',)

        widgets = {
            'tag': forms.CheckboxSelectMultiple(),
        }

    
    def __init__(self, *args, **kwargs):
        project = kwargs.pop('project', None)
        super().__init__(*args, **kwargs)
        if project:
            self.fields['tag'].queryset = Tag.objects.filter(project=project)


class CreateTagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ('name', 'color')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'input input-bordered input-primary text-lg text-gray-600 bg-gray-50 w-full'}),
            'color': forms.RadioSelect
        }
        labels = {
            'name': 'Название',
            'color': 'Цвет'
        }
    

class CreateStatusForm(forms.ModelForm):
    is_completed = forms.TypedChoiceField(
        label='Состояние задачи',
        choices=[(False, 'Не завершена'), (True, 'Завершена')],
        coerce=lambda x: x == 'True',
        widget=forms.Select(attrs={
            'class': 'select select-bordered w-full text-gray-600 bg-gray-50'
        })
    )

    class Meta:
        model = Status
        fields = ('name', 'color', 'is_completed')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'input input-bordered input-primary text-lg text-gray-600 bg-gray-50 w-full'
            }),
            'color': forms.RadioSelect,
        }
        labels = {
            'name': 'Название',
            'color': 'Цвет',
            'is_completed': 'Состояние задачи'
        }