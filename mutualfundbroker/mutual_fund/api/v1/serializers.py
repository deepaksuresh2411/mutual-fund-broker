from rest_framework.serializers import ModelSerializer, SerializerMethodField

from mutual_fund.models import MutualFund


class MutualFundModelSerializer(ModelSerializer):

    fund_family = SerializerMethodField()

    class Meta:
        model = MutualFund
        fields = [
            "scheme_name",
            "scheme_code",
            "scheme_type",
            "net_asset_value",
            "last_updated_datetime",
            "fund_family_name",
        ]

    def get_fund_family_name(self, obj):
        return obj.fund_family.name
