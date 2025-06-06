from django import forms

from .models import Task


class UpdateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('description',)

        widgets = {
            'description': forms.Textarea(attrs={'class': 'mt-2 w-full text-gray-700 border border-gray-300 rounded-md p-2 resize-none focus:outline-none focus:ring-1 focus:ring-blue-400 focus:border-blue-400 bg-gray-100', 'rows': '6'})
        }

        labels = {
            'description': 'Описание'
        }