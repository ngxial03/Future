# -*- coding: utf-8 -*-

# python排程模組
from apscheduler.schedulers.blocking import BlockingScheduler
from common import output, raw_data_gen, raw_data_download
from policy import happy, pre_enter_point, max_min
scheduler = BlockingScheduler()

# 匯入要排程的指令碼執行主函式
# from test1 import main_job1


#在指定的時間，只執行一次
# scheduler.add_job(run, 'date', run_date='2020-02-08 11:24:00')

# # 採用cron的方式執行
# scheduler.add_job(run, 'cron', day_of_week='4', second='*/4')


# @schedule.scheduled_job('interval', seconds=20)
# def timed_job():
#     output.remove()
#     raw_data_download.download()
#     raw_data_gen.go()
#     max_min.go()
#     happy.go()

def job():
    output.remove()
    raw_data_download.download()
    raw_data_gen.go()
    max_min.go()
    happy.go()


scheduler.add_job(job, 'interval', 'cron', day_of_week='mon-fri', hour=15, minute=10)


print('before the start funciton')


while True:
    scheduler.start()
