import sys,os,importlib,time

"""
全局配置设定
1、设置项目根目录
2、设置任务目录
3、设置配置文件目录
4、导入全局模块路径
5、设置任务导入模块路径
6、导入调度器支持模块
7、添加任务列表
8、导入任务模块
9、执行调度器相关任务
"""
#1、设置项目根目录
BD_PROJECT_ROOT_DIR = os.path.abspath(os.path.pardir)
#2、设置任务目录
BD_CTB_TASK_DIR = 'tasks'
#3、设置配置文件目录
BD_CTB_CONF_DIR = os.path.abspath(os.path.pardir) + '/camp'
#4、导入全局模块路径
sys.path.append(BD_PROJECT_ROOT_DIR)
#5、设置任务导入模块路径
BD_CTB_TASK_MODULE_PATH = BD_CTB_TASK_DIR.replace('/','.').replace('\\','.')
#6、导入调度器支持模块
from crontab.crontaber import Crontaber
from camp import run_schedule
#7、添加任务列表
tasks = [
    {
        "cron": '30 17 * * *',#指定执行时间
        "event_key": 'helloworld',#事件名称
        "event": 'helloworld',#事件对象
        "stop":False,#是否停止该事件
        "level":1,#事件等级返回执行列表时将按等级由高到低排序
    }
]

#8、导入任务实例
for i in range(len(tasks)):
    item = tasks[i]['event']
    tasks[i]['event'] = importlib.import_module(BD_CTB_TASK_MODULE_PATH + '.' + item)


#9、执行相关任务
ctb = Crontaber(crons=tasks)
shced = run_schedule.run_schedule(pool_num=10,cron=ctb,conf_dir=BD_CTB_CONF_DIR)
shced.run()
