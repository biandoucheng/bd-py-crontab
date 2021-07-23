from crontab import schedule
from crontab import crontaber

class run_schedule(schedule.Schedule):
    def __init__(self,pool_num:int,cron:crontaber.Crontaber,conf_dir:str=''):
        super().__init__(pool_num,cron,conf_dir)


    def before_run_task(self,**kwargs):
        print("任务执行之前执行的内容")


    def after_run_task(self,*args,**kwargs):
        print("一个任务执行完成之后要执行的内容")


    def before_start(self):
        print("开始任务执行之前的执行内容")


    def after_run_over(self):
        print("完成一轮任务执行之后执行的内容")
