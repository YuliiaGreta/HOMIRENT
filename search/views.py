from django.shortcuts import render
from .models import SearchHistory, ViewHistory

def search_history(request):
    # Получаем историю поиска для текущего пользователя
    history = SearchHistory.objects.filter(user=request.user)
    return render(request, 'search/search_history.html', {'history': history})

def view_history(request):
    # Получаем историю просмотров для текущего пользователя
    viewed = ViewHistory.objects.filter(user=request.user)
    return render(request, 'search/view_history.html', {'viewed': viewed})