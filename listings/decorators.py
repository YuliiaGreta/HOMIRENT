from django.core.exceptions import PermissionDenied

def user_is_landlord(function):
    def wrap(request, *args, **kwargs):
        if request.user.role != 'landlord':
            raise PermissionDenied
        return function(request, *args, **kwargs)
    return wrap

