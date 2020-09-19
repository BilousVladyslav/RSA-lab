from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CryptUserManager(BaseUserManager):
    def create_user(self, username, s_key_module, s_key_exp, s_key_d, u_key_module, u_key_exp):

        if not username:
            msg = 'This username is not valid'
            raise ValueError(msg)

        if not s_key_module:
            msg = 'Please Verify Your server key module'
            raise ValueError(msg)

        if not s_key_exp:
            msg = 'Please Verify Your server key exponent'
            raise ValueError(msg)

        if not s_key_d:
            msg = 'Please Verify Your server key D'
            raise ValueError(msg)

        if not u_key_module:
            msg = 'Please Verify Your user key module'
            raise ValueError(msg)

        if not u_key_exp:
            msg = 'Please Verify Your user key exponent'
            raise ValueError(msg)

        user = self.model(username=username, server_key_module=s_key_module, server_key_exponent=s_key_exp,
                          server_key_D=s_key_d, user_key_module=u_key_module, user_key_exponent=u_key_exp)

        user.set_password(None)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, email, s_key_module=1,
                         s_key_exp=1, s_key_d=1, u_key_module=1, u_key_exp=1):
        user = self.create_user(username, s_key_module, s_key_exp, s_key_d, u_key_module, u_key_exp)
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CryptUser(AbstractUser):
    server_key_module = models.IntegerField(blank=False)
    server_key_exponent = models.IntegerField(blank=False)
    server_key_D = models.IntegerField(blank=False)
    user_key_module = models.IntegerField(blank=False)
    user_key_exponent = models.IntegerField(blank=False)

    objects = CryptUserManager()
