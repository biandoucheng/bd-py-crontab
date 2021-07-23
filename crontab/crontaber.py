from operator import itemgetter
from datetime import datetime
import math

class Crontaber:
    def __init__(self,crons:list):
        """
        初始化一个定时器

        :param crons: 定时事件列表
        eg: [
                {
                    "cron": '10,50 8,16,17 * * *',#这里指
                    "event_key": 'email_send',#事件名称
                    "event": object,#事件对象
                    "stop":bool,#是否停止该事件
                    "level":int,#事件等级返回执行列表时将按等级由高到低排序
                }
            ]
        """
        self.__crons = crons



    def init_time(self):
        """
        返回当前事件对象

        :return: datetime.now
        """
        return datetime.now()



    def time_chunk(self,tl:int,sp:int,st:int):
        """
        获取时间分片

        :param tl: int 时间长度 分钟:60,周:7 ...
        :param num: int 每两次执行间隔时间
        :param st:int 开始执行的时间
        :return: list 时间点列表
        """
        if tl != 0 and sp == 0:
            return []

        lis = {st}
        ttn = math.ceil(tl/sp)

        for i in range(ttn):
            ct = (i + 1) * sp
            if ct <= tl and ct > st:
                lis.add(ct)

        return lis



    def parse_cron_regx_to_time_set(self,cron_regex:str,start:int,end:int):
        """
        将时间规则转化成时间点集合

        :param cron_regex: str 时间规则字符串  *  |  num  |  */num  |  num,num,num  |   num-num   |   num-num/num
        :param start: int 该时间维度的开始
        :param end: int 该事件维度的结束
        :return: set 时间点集合
        """
        # num 指定一个时间点
        if cron_regex.isdigit():
            return {int(cron_regex)}

        # * 全部时间点执行
        if cron_regex == '*':
            return self.time_chunk(tl=end,sp=1,st=start)

        # */num 预期执行num次
        if cron_regex.startswith('*/'):
            sp = int(cron_regex.lstrip('*/'))
            return self.time_chunk(tl=end,sp=sp,st=start)

        # num-num/num 在指定时间端中预期执行指定次数
        if '-' in cron_regex and '/' in cron_regex:
            ts = cron_regex.split('/')
            bt = ts[0].split('-')
            sp = int(ts[1])
            return self.time_chunk(tl=int(bt[1]), sp=sp, st=int(bt[0]))

        # num,num,num 在指定时间点列表中运行
        if ',' in cron_regex:
            ss = set()
            ts = cron_regex.split(',')
            for t in ts:
                if t.isdigit():
                    ss.add(int(t))
            return ss

        if '-' in cron_regex:
            bt = cron_regex.split('-')
            return self.time_chunk(tl=int(bt[1]),sp=1,st=int(bt[0]))



    def cron_check(self,cron:str):
        """
        检测时间规则并判断是否处于执行时间

        :param cron: str 时间规则字符串
        :return: bool 是否处于执行时间
        """
        t = self.init_time()
        crons = cron.split(' ')

        for i in range(len(crons)):
            # 分钟
            if i == 0:
                allow = self.parse_cron_regx_to_time_set(cron_regex=crons[i],start=0,end=59)
                if t.minute not in allow:
                    return False
            #小时
            if i == 1:
                allow = self.parse_cron_regx_to_time_set(cron_regex=crons[i],start=0,end=23)
                if t.hour not in allow:
                    return False
            #天 这里不用考虑大小月问题
            if i == 2:
                allow = self.parse_cron_regx_to_time_set(cron_regex=crons[i],start=1,end=31)
                if t.day not in allow:
                    return False
            #月
            if i == 3:
                allow = self.parse_cron_regx_to_time_set(cron_regex=crons[i],start=1,end=12)
                if t.month not in allow:
                    return False
            #周 时间里面提取的周会少一天
            if i == 4:
                allow = self.parse_cron_regx_to_time_set(cron_regex=crons[i],start=1,end=7)
                wek = t.weekday() + 1
                if wek not in allow:
                    return False

        return True



    def get_en_tasks(self):
        """
        判断当前需要执行的任务，并按照任务级别排序返回

        :return: list tasks
        """
        tasks = []
        for event in self.__crons:
            if not event['stop'] and self.cron_check(event['cron']):
                tasks.append(event)
        return sorted(tasks,key=itemgetter('level'))

