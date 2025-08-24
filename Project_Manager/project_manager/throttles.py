from rest_framework.throttling import UserRateThrottle

class RoleBasedRateThrottle(UserRateThrottle):
    def get_cache_key(self, request, view):
        if not request.user.is_authenticated:
            self.scope = "anon"
        elif request.user.is_superuser:
            self.scope = "superuser"
        elif request.user.is_staff:
            self.scope = "staff"
        else:
            self.scope = "user"

        return super().get_cache_key(request, view)
