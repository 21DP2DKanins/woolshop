from django.apps import AppConfig


class ShopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shop'

class YourAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'yourapp'  # Замените на имя вашего приложения
    
    def ready(self):
        """
        Импортируйте файл сигналов, чтобы подключить сигналы в Django
        """
        import yourapp.signals  # Замените 'yourapp' на имя вашего приложения