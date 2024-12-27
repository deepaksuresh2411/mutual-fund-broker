from rest_framework.serializers import ModelSerializer, SerializerMethodField

from users.models import UserInvestDetails


class UserInvestmentsModelSerializer(ModelSerializer):
    scheme_name = SerializerMethodField()
    nav = SerializerMethodField()

    class Meta:
        model = UserInvestDetails
        fields = [
            "id",
            "scheme_name",
            "units_owned",
            "amount_invested",
            "investment_date",
            "current_value",
            "nav",
        ]

    def get_scheme_name(self, obj):
        return obj.mutual_fund.scheme_name

    def get_nav(self, obj):
        return obj.mutual_fund.net_asset_value
