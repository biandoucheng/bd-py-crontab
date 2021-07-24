import threading,time,traceback
from concurrent.futures import ThreadPoolExecutor,wait
from crontab.crontaber import Crontaber
from crontab.config import Configer

class Schedule:
    def __init__(self,pool_num:int,cron:Crontaber,conf_dir:str=''):
        #初始化线程池
        self.thread_lock  = threading.Lock()
        self.thread_pool  = ThreadPoolExecutor(pool_num)
        self.handle_pools = []
        #初始化定时器
        self.cron         = cron
        #重置信号记录文件地址
        if conf_dir:
            self.cong_dir = conf_dir
        else:
            self.cong_dir = './'
        #配置类
        self.configer = Configer(conf_catalog=self.cong_dir,encode_str="utf-8")



    def call_task(self,task:dict):
        """
        调用任务执行方法

        :param obj: object 任务对象
        :return:
        """
        print("执行任务 >",task)
        self.before_run_task(**task)
        res = task['event']().run()
        self.after_run_task(res,**task)



    def before_run_task(self,**kwargs):
        """
        在执行一个任务之前需要执行的代码

        :param kwargs: dict 任务信息，有定时器提供的字典
        :return:
        """



    def after_run_task(self,*args,**kwargs):
        """
        执行完一个任务需要执行的代码

        :param args: *args 任务执行返回信息，这里要任务代码里做好返回值约束
        :param kwargs: dict 任务信息，有定时器提供的字典
        :return:
        """




    def before_start(self):
        """
        开始定时运行之前执行的内容

        :return:
        """



    def after_run_over(self):
        """
        一轮执行完成需要执行的内容

        :return:
        """


    def sign_check(self):
        """
        检测信号

        :return:
        """
        busy = int(self.configer.get_val(name='signal',key='busy'))
        without_overlapping = int(self.configer.get_val(name='signal',key='without_overlapping'))
        last_end_at = int(self.configer.get_val(name='signal',key='last_end_at'))
        shutdown = int(self.configer.get_val(name='signal',key='shutdown'))
        now_timestamp = int(time.time())

        #关机不执行
        if shutdown:
            exit()

        #上次任务没有执行完
        if busy:
            #没有设置超时时间则停止执行本轮任务
            if without_overlapping:
                return False
            else:
                #没有超过超时时间则停止执行本轮循环
                if now_timestamp < (last_end_at + without_overlapping):
                    return False

        return True



    def signaled(self,start:bool):
        """
        标记开始与借宿

        :param start: bool 开始|结束
        :return:
        """
        if start:
            self.configer.set_val_to_ini(name='signal',key='busy',val=1)
            self.configer.set_val_to_ini(name='signal',key='last_start_at',val=int(time.time()))
        else:
            self.configer.set_val_to_ini(name='signal', key='busy', val=0)
            self.configer.set_val_to_ini(name='signal', key='last_end_at', val=int(time.time()))



    def run(self,just_once=False):
        run = True
        while run:
            if just_once:
                run = False

            #检测信号
            if not self.sign_check():
                continue
            else:
                #标记开始
                self.signaled(start=True)

            #获取任务列表
            tasks = self.cron.get_en_tasks()

            #任务循环前执行代码
            self.before_start()

            #循环执行任务
            for i in range(len(tasks)):
                try:
                    task = tasks[i]
                    handel = self.thread_pool.submit(self.call_task,event=task)
                    self.handle_pools.append(handel)
                except Exception as e:
                    print(traceback.format_exc())
            else:
                print("等待执行。。。")
                try:
                    wait(self.handle_pools)
                except Exception as e:
                    print("任务执行失败:\n"+traceback.format_exc())

            #任务执行后代码
            self.after_run_over()

            #标记结束
            self.signaled(start=False)

            #睡眠一秒
            time.sleep(1)

