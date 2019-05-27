from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from .managers import UserManager

# 正则匹配
USERNAME_REGEX = '^[a-z0-9._-]*$'


class User(AbstractUser):
    first_name = None
    last_name = None

    username = models.CharField(
        max_length=256,
        unique=True,
        blank=False,
        validators=[
            RegexValidator(
                regex=USERNAME_REGEX,
                message='Username must contain: a-z, 0-9 or ".-_" ',
                code='invalid_username'
                )
            ]
        )

    email = models.EmailField(unique=True, blank=False)

    USERNAME_FIELD = 'email'  # 使用邮箱进行登陆
    REQUIRED_FIELDS = ['username']  # 当 user 创建时必填项

    objects = UserManager()

    def __str__(self):
        return self.username

    class Meta:
        verbose_name='用户信息'
        verbose_name_plural = verbose_name
