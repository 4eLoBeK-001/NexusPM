from django import forms

from .models import Status, Tag, Task


class UpdateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('description', 'tag')

        widgets = {
            'description': forms.Textarea(attrs={'class': 'mt-2 w-full text-gray-700 border border-gray-300 rounded-md p-2 resize-none focus:outline-none focus:ring-1 focus:ring-blue-400 focus:border-blue-400 bg-gray-100', 'rows': '6'}),
            'tag': forms.CheckboxSelectMultiple(),
        }

        labels = {
            'description': 'Описание'
        }
    
    def __init__(self, *args, **kwargs):
        project = kwargs.pop('project', None)
        super().__init__(*args, **kwargs)
        if project:
            self.fields['tag'].queryset = Tag.objects.filter(project=project)


class SidebarForm(forms.ModelForm):
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