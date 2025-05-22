from django import forms

from .widgets import CustomImageField
from .models import Project

class AddModalProjectForm(forms.ModelForm):

    name = forms.CharField( 
        widget=forms.TextInput(
            attrs={'class': 'input input-bordered w-full bg-white text-slate-800 border-1 border-gray-300 focus:border-primary focus:ring-2 focus:ring-primary/50 transition-all'})
    )

    # image = forms.ImageField(widget=forms.FileInput(attrs={'id': 'id_image', 'class': 'hidden w-32 h-32 object-cover border rounded'}))

    class Meta:
        model = Project
        fields = ( 'image', 'name')

        labels = {
            'image': 'Изображение',
            'name': 'Название',
        }

        widgets = {
            'image': CustomImageField(attrs={'class': 'ms'})
        }