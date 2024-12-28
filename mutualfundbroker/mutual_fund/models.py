from django.db import models


class MutualFundFamily(models.Model):
    # This model is added because we can add/remove a fund family from Admin panel
    # instead of having a choice field for fund family where we need to make code changes
    name = models.CharField(max_length=100, null=True, blank=True)


class MutualFund(models.Model):
    scheme_code = models.CharField(max_length=30, null=True, blank=True, unique=True)
    scheme_name = models.CharField(max_length=100, null=True, blank=True)
    fund_family = models.ForeignKey(
        MutualFundFamily, on_delete=models.CASCADE, null=True
    )
    net_asset_value = models.PositiveIntegerField(verbose_name="NAV", default=0)
    last_updated_datetime = models.DateTimeField(auto_now=True)
    scheme_type = models.CharField(max_length=25, null=True, blank=True)
    scheme_category = models.CharField(max_length=100, null=True, blank=True)
