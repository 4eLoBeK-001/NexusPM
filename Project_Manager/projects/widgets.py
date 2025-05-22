from django.forms import FileInput

class CustomImageField(FileInput):
    template_name = 'projects/includes/custom-image-field.html'