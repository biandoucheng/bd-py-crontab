import sys,os

"""
全局配置设定
1、设置项目根目录
2、设置任务目录
3、设置配置文件目录
4、导入全局模块路径
5、设置任务导入模块路径
6、导入调度器支持模块
7、添加任务列表
8、执行相关任务
"""
#1、设置项目根目录
BD_PROJECT_ROOT_DIR = os.path.abspath(os.path.pardir)
#2、设置任务目录
BD_CTB_TASK_DIR = 'camp'
#3、设置配置文件目录
BD_CTB_CONF_DIR = 'camp'
#4、导入全局模块路径
sys.path.append(BD_PROJECT_ROOT_DIR)
#5、设置任务导入模块路径
BD_CTB_TASK_MODULE_PATH = BD_CTB_TASK_DIR.replace('/','.').replace('\\','.')
#6、导入调度器支持模块
from crontab.crontaber import Crontaber
#7、添加任务列表
tasks = [
    {
        "cron": '* * * * *',#这里指
        "event_key": 'email_send',#事件名称
        "event": 'dsadsfds',#事件对象
        "stop":False,#是否停止该事件
        "level":1,#事件等级返回执行列表时将按等级由高到低排序
    },
    {
        "cron": '* * * * *',#这里指
        "event_key": 'email_send',#事件名称
        "event": 'dsadsfds',#事件对象
        "stop":False,#是否停止该事件
        "level":2,#事件等级返回执行列表时将按等级由高到低排序
    },
    {
        "cron": '40-50 * * * *',#这里指
        "event_key": 'email_send',#事件名称
        "event": 'dsadsfds',#事件对象
        "stop":False,#是否停止该事件
        "level":3,#事件等级返回执行列表时将按等级由高到低排序
    },
    {
        "cron": '40-50 * * * *',#这里指
        "event_key": 'email_send',#事件名称
        "event": 'dsadsfds',#事件对象
        "stop":False,#是否停止该事件
        "level":4,#事件等级返回执行列表时将按等级由高到低排序
    }
]

#8、执行相关任务
task_list = Crontaber(crons=tasks).get_en_tasks()
for task in task_list:
    print(task)
