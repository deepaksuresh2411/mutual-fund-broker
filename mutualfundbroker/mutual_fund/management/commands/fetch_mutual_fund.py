import os
import time

import requests
from dotenv import load_dotenv
from django.core.management.base import BaseCommand

from mutual_fund.models import MutualFund, MutualFundFamily

# Load the .env file
load_dotenv()


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        print("handle")
        fund_families = MutualFundFamily.objects.all()

        for fund_family in fund_families:
            RAPID_API_URL = f"https://{os.getenv('RAPID_API_HOST')}/latest"
            HEADERS = {
                "X-RapidAPI-Key": os.getenv("RAPID_API_KEY"),
                "x-rapidapi-host": os.getenv("RAPID_API_HOST"),
            }
            querystring = {
                "Mutual_Fund_Family": fund_family.name,
                "Scheme_Type": "Open",
            }

            try:
                response = requests.get(
                    RAPID_API_URL, headers=HEADERS, params=querystring
                )
                response.raise_for_status()
                funds_data = response.json()
                mutual_funds = MutualFund.objects.filter(fund_family=fund_family)
                for fund in funds_data:
                    mf = mutual_funds.filter(scheme_code=fund["Scheme_Code"]).last()
                    if mf:
                        mf.net_asset_value = fund["Net_Asset_Value"]
                        mf.save()
                    else:
                        MutualFund.objects.create(
                            scheme_code=fund["Scheme_Code"],
                            scheme_name=fund["Scheme_Name"],
                            net_asset_value=fund["Net_Asset_Value"],
                            scheme_type=fund["Scheme_Type"],
                            scheme_category=fund["Scheme_Category"],
                            fund_family=fund_family,
                        )
                time.sleep(2)
            except requests.exceptions.RequestException as e:
                self.stderr.write(
                    self.style.ERROR(f"Error fetching data from RapidAPI: {e}")
                )
        self.stdout.write(
            self.style.SUCCESS("Successfully updated the mutual funds data.")
        )
