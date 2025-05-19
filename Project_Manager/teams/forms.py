from django import forms

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

    class Meta:
        model = Team
        fields = ('name', 'description', 'team_member')