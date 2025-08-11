from django.shortcuts import redirect, render
from django.contrib import messages

from users.forms import FeedBackForm

def main_page(request):
    return render(request, 'home-page.html')

def feedback(request):
    form = FeedBackForm()
    if request.method == 'POST':
        form = FeedBackForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user if request.user.is_authenticated else None
            form.save()
            messages.success(request, 'Ваше сообщение успешно отправлено!')
            return redirect(request.META.get('HTTP_REFERER'))
    data = {
        'form': form
    }
    return render(request, 'feedback.html', data)


def custom_page_forbidden(request, exception):
    return render(request, "errors/403.html", {}, status=403)

def custom_page_not_found(request, exception):
    return render(request, "errors/404.html", {}, status=404)

def custom_server_error(request):
    return render(request, "errors/500.html", {}, status=500)