def headers_data(request):
    return {
        'site_name': 'My Awesome Site',
        'menu_items': [
            {'name': 'Мои объявления', 'url': 'listings:my'},
            {'name': 'Создать объявление', 'url': 'create_listing'},
            {'name': 'Выйти', 'url': 'listings:logout'}
        ]
    }
