import os
import time
import schedule


def fetch_mutual_fund_data():
    os.system("python manage.py fetch_mutual_fund")


schedule.every(1).hour.do(fetch_mutual_fund_data)

print("Hourly task started running...")
while True:
    schedule.run_pending()
    time.sleep(30)
