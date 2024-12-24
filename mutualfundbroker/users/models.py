from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class AppUserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email id field must be set")
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, email):
        return self.get(email=email)


class Appuser(AbstractBaseUser):

    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(
        verbose_name="Email ID", null=True, blank=True, unique=True
    )
    account_created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    objects = AppUserManager()


class UserInvestDetails(models.Model):
    user = models.ForeignKey(Appuser, on_delete=models.CASCADE, null=True)
    mutual_fund = models.CharField(
        max_length=20, null=True, blank=True
    )  # Foreign key to MF
    units_owned = models.PositiveIntegerField(default=0)
    investment_date = models.DateField(null=True, blank=True)

    @property
    def current_value(self):
        return self.mutual_fund.net_asset_value * self.units_owned
