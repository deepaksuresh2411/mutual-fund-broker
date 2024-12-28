from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

from mutual_fund.models import MutualFund


class AppUserManager(UserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(email, password, **extra_fields)


class Appuser(AbstractUser):
    email = models.EmailField(
        verbose_name="Email ID", null=True, blank=True, unique=True
    )
    account_created_at = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=1, unique=False)  # Not getting used

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    objects = AppUserManager()


class UserInvestDetails(models.Model):
    user = models.ForeignKey(Appuser, on_delete=models.CASCADE, null=True)
    mutual_fund = models.ForeignKey(MutualFund, on_delete=models.CASCADE)
    units_owned = models.PositiveIntegerField(default=0)
    amount_invested = models.PositiveIntegerField(default=0)
    investment_date = models.DateField(null=True, blank=True)

    @property
    def current_value(self):
        return self.mutual_fund.net_asset_value * self.units_owned
