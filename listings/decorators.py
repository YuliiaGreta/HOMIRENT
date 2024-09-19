from django.core.exceptions import PermissionDenied  # Импортирую исключение, которое вызываю, если у пользователя нет прав

# Создаю декоратор, чтобы проверять, что текущий пользователь — арендодатель
def user_is_landlord(function):
    def wrap(request, *args, **kwargs):
        # Проверяю, что роль пользователя — арендодатель
        if request.user.role != 'landlord':
            # Если это не арендодатель, выбрасываю исключение PermissionDenied
            raise PermissionDenied
        # Если проверка пройдена, выполняю основную функцию
        return function(request, *args, **kwargs)
    return wrap  # Возвращаю обернутую функцию
