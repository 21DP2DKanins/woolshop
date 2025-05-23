# Настройки для Django-проекта

# Добавьте эти настройки в settings.py

# Настройка пользовательской модели
AUTH_USER_MODEL = 'woolshop.CustomUser'  # Замените 'yourapp' на имя вашего приложения

# Настройка аутентификации по email
AUTHENTICATION_BACKENDS = [
    'yourapp.backends.EmailBackend',  # Замените 'yourapp' на имя вашего приложения
    'django.contrib.auth.backends.ModelBackend',
]

# Настройки для отправки email (для сброса пароля)
# Пример настроек для SMTP
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.example.com'  # Замените на ваш SMTP-сервер
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_email@example.com'  # Замените на ваш email
EMAIL_HOST_PASSWORD = 'your_password'  # Замените на ваш пароль
DEFAULT_FROM_EMAIL = 'noreply@example.com'  # Email отправителя по умолчанию

# Для разработки можно использовать имитацию отправки писем в консоль:
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Настройка входа и перенаправлений
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'  # Замените на нужную страницу после входа
LOGOUT_REDIRECT_URL = 'home'  # Замените на нужную страницу после выхода

# Сессии
SESSION_COOKIE_AGE = 1209600  # 2 недели (в секундах) для опции "remember me"

# Настройки сообщений
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'