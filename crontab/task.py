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
]

#8、执行相关任务
task_list = Crontaber(crons=tasks).get_en_tasks()
for task in task_list:
    print(task)
