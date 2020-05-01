from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,PermissionsMixin
)


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have an Email')

        user = self.model(
            email=email,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(
        max_length=255,
        unique=True,
    )
    first_name = models.CharField('Фамилия', max_length=255, blank=True, null=True)
    last_name = models.CharField('Имя', max_length=255, blank=True, null=True)
    patronymic = models.CharField('Отчество', max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=30,verbose_name="Телефон", null=True, blank=True)
    date_of_birth = models.DateField(verbose_name="Дата рождения",null=True,blank=True)
    last_time_visit = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def full_name(self):
        if self.first_name and self.last_name and self.patronymic:
            return '{} {} {}'.format(self.first_name, self.last_name, self.patronymic)
        elif self.first_name and self.last_name:
            return '{} {}'.format(self.first_name, self.last_name)
        elif self.first_name:
            return '{}'.format(self.first_name)
        else:
            return self.email

    @property
    def fio(self):
        return '{} {}'.format(self.first_name, self.last_name)
