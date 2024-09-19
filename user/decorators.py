from django.shortcuts import redirect
from functools import wraps

# Декоратор для перенаправления аутентифицированного пользователя
# Я хочу сделать так, чтобы аутентифицированные пользователи не могли зайти на страницы, где они не должны быть (например, на страницу регистрации или входа)
def redirect_authenticated_user(view_func):
    @wraps(view_func)  # Этот декоратор сохраняет оригинальные метаданные функции
    def _wrapped_view(request, *args, **kwargs):
        # Проверяю, аутентифицирован ли пользователь
        if request.user.is_authenticated:
            # Если пользователь уже вошел в систему, перенаправляю её на домашнюю страницу
            return redirect('user:homepage')  # Здесь я задаю URL, куда перенаправлять пользователя
        # Если пользователь не аутентифицирован, то функция продолжается как обычно
        return view_func(request, *args, **kwargs)
    return _wrapped_view  # Возвращаю новую "обернутую" функцию
