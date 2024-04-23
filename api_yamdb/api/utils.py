from django.core.mail import send_mail


def send_code(user, confirmation_code):
    send_mail(
        subject='Код подтверждения',
        message=(f'Ваш код подтверждения для доступа - {confirmation_code}'),
        recipient_list=[user.email],
        from_email='praktikum@mail.ru',
    )
