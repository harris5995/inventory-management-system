from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden

def manager_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.userprofile.role == 'manager':
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("You do not have permission to access this page.")
    return wrapper