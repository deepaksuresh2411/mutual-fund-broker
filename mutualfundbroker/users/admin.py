from django.contrib import admin

from users.models import Appuser, UserInvestDetails

# Register your models here.

admin.site.register(Appuser)
admin.site.register(UserInvestDetails)
