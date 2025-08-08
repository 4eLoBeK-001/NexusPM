from django.shortcuts import render

from users.forms import FeedBackForm

def main_page(request):
    return render(request, 'home-page.html')

def feedback(request):
    form = FeedBackForm()
    data = {
        'form': form
    }
    return render(request, 'feedback.html', data)