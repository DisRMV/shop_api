from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from backend.models import ConfirmEmailToken, User
from orders.celery import app


@app.task
def password_reset_token_created(sender, instance, reset_password_token, **kwargs):
    """
    Отправляем письмо с токеном для сброса пароля
    """

    msg = EmailMultiAlternatives(
        f'Ваш токен для сброса пароля: {reset_password_token.user}',
        reset_password_token.key,
        settings.EMAIL_HOST_USER,
        [reset_password_token.user.email]
    )
    msg.send()


@app.task
def new_user_registered(user_id, **kwargs):
    """
    Отправляем письмо с подтверждением почты
    """
    token, _ = ConfirmEmailToken.objects.get_or_create(user_id=user_id)

    msg = EmailMultiAlternatives(
        f'Ваш токен для подтверждения почты: {token.user.email}',
        token.key,
        settings.EMAIL_HOST_USER,
        [token.user.email]
    )
    msg.send()


@app.task
def new_order(user_id, **kwargs):
    """
    Отправляем письмо при изменении статуса заказа
    """
    user = User.objects.get(id=user_id)

    msg = EmailMultiAlternatives(
        f'Обновление статуса заказа',
        'Заказ сформирован',
        settings.EMAIL_HOST_USER,
        [user.email]
    )
    msg.send()
