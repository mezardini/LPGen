from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email,  password, **extra_fields):

        values = [email, ]
        field_value_map = dict(zip(self.model.REQUIRED_FIELDS, values))

        for field_name, value in field_value_map.items():
            if not value:
                raise ValueError('The {} value must be set'.format(field_name))

        email = self.normalize_email(email)

        user = self.model(
            email=email,

            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email,  password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email,  password, **extra_fields)

    def create_superuser(self, email,  password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email,  password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    slug = models.CharField(max_length=305, null=True, blank=True)
    username = models.CharField(max_length=305, null=True, blank=True)
    credit = models.IntegerField(default=10, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return f'{self.email}'


class Idea(models.Model):
    details = models.TextField()
    # creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    target_audience = models.TextField()
    time_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.biz_name


class Creators(models.Model):
    email = models.EmailField()
    time_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.email


# class PaymentLogs(models.Model):
#     SUCCESS = 'Success'
#     FAILED = 'Failed'
#     Transaction_status = [
#         (SUCCESS, ('Success')),
#         (FAILED, ('Failed')),
#     ]

#     payer = models.ForeignKey(
#         CustomUser, on_delete=models.CASCADE, related_name='payment_user')
#     time = models.DateTimeField(auto_now_add=True)
#     amount = models.FloatField()
#     transaction_id = models.CharField(max_length=200)
#     status = models.CharField(max_length=200)
#     pay_date = models.DateTimeField(auto_now_add=True, null=True)

#     def __str__(self):
#         return f"{self.payer.email} - {self.amount}"
