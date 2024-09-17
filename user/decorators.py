from django.shortcuts import redirect
from functools import wraps

def redirect_authenticated_user(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('user:homepage')  # Замените на нужный вам URL
        return view_func(request, *args, **kwargs)
    return _wrapped_view
