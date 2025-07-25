from django.forms import FileInput


class CustomImageField(FileInput):
    template_name = 'users/custom.html'