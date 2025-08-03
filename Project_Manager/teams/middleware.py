import threading

_user = threading.local()

def get_current_user():
    return getattr(_user, 'value', None)

class CurrentUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _user.value = request.user
        response = self.get_response(request)
        return response