from django.db import migrations
from django.contrib.auth.hashers import make_password


def create_sample_users(apps, schema_editor):
    """
    Create initial users including an admin user
    """
    User = apps.get_model('yourapp', 'CustomUser')  # Replace 'yourapp' with your app name
    
    # Create admin user
    admin_user = User(
        email='admin@example.com',
        password=make_password('admin123'),  # ВАЖНО: Поменяйте на безопасный пароль в реальном проекте!
        first_name='Admin',
        last_name='User',
        is_active=True,
        is_staff=True,
        is_superuser=True,
    )
    admin_user.save()
    
    # Create regular user
    user = User(
        email='user@example.com',
        password=make_password('user123'),  # ВАЖНО: Поменяйте на безопасный пароль в реальном проекте!
        first_name='Test',
        last_name='User',
        is_active=True,
    )
    user.save()


class Migration(migrations.Migration):
    dependencies = [
        ('yourapp', '0001_initial'),  # Replace 'yourapp' with your app name and adjust migration number
    ]

    operations = [
        migrations.RunPython(create_sample_users),
    ]