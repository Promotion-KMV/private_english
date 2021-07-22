from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
import datetime
from english_teacher.models import CustomUser


class AppTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (text_type(user.is_active)+text_type(user.pk)+text_type(timestamp))


token_generator = AppTokenGenerator()


def delete_user_is_not_activate():
    user = CustomUser.objects.filter(is_active=False)
    for i in user:
        if (datetime.datetime.now().timestamp() - i.date_joined.timestamp()) > 10800:
            i.delete()

