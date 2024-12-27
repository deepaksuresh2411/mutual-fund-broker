from django.contrib import admin

from mutual_fund.models import MutualFund, MutualFundFamily

admin.site.register(MutualFund)
admin.site.register(MutualFundFamily)
