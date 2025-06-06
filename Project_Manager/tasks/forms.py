from django import forms

from .models import Task


class UpdateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('name', 'description')