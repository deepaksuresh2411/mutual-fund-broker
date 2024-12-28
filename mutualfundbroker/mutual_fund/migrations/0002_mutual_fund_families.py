from django.db import migrations


def create_fund_families(apps, schema_editor):
    fund_families = [
        "Aditya Birla Sun Life Mutual Fund",
        "Axis Mutual Fund",
        "Bandhan Mutual Fund",
        "Bank of India Mutual Fund",
        "Baroda BNP Paribas Mutual Fund",
        "Canara Robeco Mutual Fund",
        "DSP Mutual Fund",
        "Edelweiss Mutual Fund",
        "Franklin Templeton Mutual Fund",
        "HDFC Mutual Fund",
        "HSBC Mutual Fund",
        "ICICI Prudential Mutual Fund",
        "Invesco Mutual Fund",
        "JM Financial Mutual Fund",
        "Kotak Mahindra Mutual Fund",
        "LIC Mutual Fund",
        "Mahindra Manulife Mutual Fund",
        "Mirae Asset Mutual Fund",
        "Motilal Oswal Mutual Fund",
        "Navi Mutual Fund",
        "Nippon India Mutual Fund",
        "PGIM India Mutual Fund",
        "PPFAS Mutual Fund",
        "Quant Mutual Fund",
        "Quantum Mutual Fund",
        "SBI Mutual Fund",
        "Sundaram Mutual Fund",
        "TRUST Mutual Fund",
        "Tata Mutual Fund",
        "360 ONE Mutual Fund",
        "UTI Mutual Fund",
        "Union Mutual Fund",
        "WhiteOak Capital Mutual Fund",
        "Zerodha Mutual Fund",
    ]
    mutual_fund_family = apps.get_model("mutual_fund", "MutualFundFamily")
    for fund_family in fund_families:
        mutual_fund_family.objects.create(name=fund_family)


class Migration(migrations.Migration):

    dependencies = [("mutual_fund", "0001_initial")]

    operations = [
        migrations.RunPython(create_fund_families),
    ]
