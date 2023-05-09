import schedule
import time
import os
def job():
    os.system("venv/bin/python3 cli.py source apple -d download_configs/download_news.ini ")
    print("I'm working...")

schedule.every().day.at("10:30").do(job)
while True:
    schedule.run_pending()
    time.sleep(1)
