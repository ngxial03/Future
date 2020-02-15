from apscheduler.schedulers.blocking import BlockingScheduler
from common import output, raw_data_gen, raw_data_download
from policy import happy, pre_enter_point, max_min
from pytz import utc
from tzlocal import get_localzone
import os
import datetime

scheduler = BlockingScheduler(timezone="Asia/Taipei")

print (datetime.datetime.now())


tz = get_localzone()
print(tz)


def job():
    print(datetime.datetime.now())
    output.remove()
    raw_data_download.download()
    raw_data_gen.go()
    max_min.go()
    happy.go()
    # update to git
    log = "update " + datetime.datetime.now().strftime("%Y%m%d")
    os.system('git pull')
    os.system('git status')
    os.system('git add .')
    os.system('git commit -m "' + log + '"')
    os.system('git push')


# scheduler.add_job(job, 'interval', seconds=10)

scheduler.add_job(job, 'cron', day_of_week='mon-fri', hour=17, minute=30)
# scheduler.add_job(job, 'cron', hour=11, minute=02)

print('****** start scheduler ******')


while True:
    scheduler.start()
