from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model

User = get_user_model()


@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    """
    Send a welcome email to newly registered users
    """
    if created:
        # Здесь можно добавить логику отправки приветственного письма
        # Например, используя функцию send_mail из Django
        # 
        # from django.core.mail import send_mail
        # 
        # if instance.email:
        #     subject = "Welcome to our shop!"
        #     message = f"Hello {instance.get_full_name()},\n\nThank you for registering with our shop!"
        #     from_email = "noreply@example.com"
        #     recipient_list = [instance.email]
        #     
        #     send_mail(subject, message, from_email, recipient_list)
        pass