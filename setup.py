from crontab import CronTab
import os

cmd = os.popen("which python3").read().strip("\n")
pwd = os.popen("pwd").read().strip("\n")
cron = CronTab(user = True)
job = cron.new(command = cmd + " " + pwd + "/tb2k.py")
job.day.on(6)
job.enable()
cron.write()
