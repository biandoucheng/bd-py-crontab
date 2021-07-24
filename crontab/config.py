import configparser,os,traceback

class ConfigError(Exception):
    """
    定义配置类异常
    """
    def __init__(self, errorinfor):
        self.error = errorinfor

    def __str__(self):
        return self.error


class Configer:
    """
    1、配置文件加载类
    2、.py配置文件的优先级高于.ini配置文件的优先级
    """
    def __init__(self,conf_catalog:str,encode_str:str='utf-8'):
        #配置文件目录
        self.__root = conf_catalog.rstrip('/')
        #编码格式
        self.__encode_str = encode_str
        #配置文件模块字典
        self.__conf_dict = dict()
        #已经加载的配置文件集合
        self.loaded_conf_sets = set()



    def __load_ini_cfparse(self):
        """
        初始化ini配置文件解析实例
        :return:
        """
        if not hasattr(self,'__cf_parse') or not self.__cf_parse:
            self.__cf_parse = configparser.ConfigParser()


    def is_config_file_exists(self,name:str):
        """
        判断配置文件是否存在

        :param name: str 配置为文件名称
        :return: bool
        """
        return os.path.exists(self.__root + '/' + name)



    def __load_conf_module(self,name=''):
        """
        配置模块导入 .py
        :param name: string 配置文件名
        :return:
        """
        if not self.is_config_file_exists(name=name+'.py'):
            return

        if name not in self.__conf_dict:
            self.__conf_dict[name] = {}
        cf = __import__(name='config.'+name,fromlist=['None'])
        self.__conf_dict[name].update(cf.configs)
        self.loaded_conf_sets.add(name+'.py')



    def __load_conf_ini(self,name='',section='DEFAULT'):
        """
        配置文件导入 .ini
        :param name: string 配置文件名称
        :param section: string 指定配置文件分区 DEFAULT
        :return:
        """
        if not self.is_config_file_exists(name=name+'.ini'):
            return

        self.__load_ini_cfparse()

        if name not in self.__conf_dict:
            self.__conf_dict[name] = {}
        self.__cf_parse.read(filenames=self.__root+'/'+name+'.ini',encoding=self.__encode_str)

        if not section or section.lower() == 'default':
           section = 'DEFAULT'

        if section != 'DEFAULT' and section not in self.__cf_parse.sections():
            return

        itms = self.__cf_parse.items(section=section)

        for it in itms:
            k,v = it
            if k not in self.__conf_dict[name]:
                self.__conf_dict[name][k] = v

        self.loaded_conf_sets.add(name+'.ini-'+section.lower())



    def __load_configs(self,name='',section='DEFAULT',flu=False):
        """
        加载配置文件
        :param name: string 文件名
        :param section: string .ini配置的分区 默认 DEFAULT
        :param flu: bool 是否强制刷新 False
        :return:
        """
        try:
            if not name or not isinstance(name, str):
                return

            if flu or name + '.py' not in self.loaded_conf_sets:
                self.__load_conf_module(name=name)

            if flu or name + '.ini-' + section.lower() not in self.loaded_conf_sets:
                self.__load_conf_ini(name=name, section=section)
        except Exception as e:
            raise ConfigError("配置文件初始化失败")



    def get_val(self,name='',key='',section='DEFAULT',flu=False):
        """
        加载配置项
        :param name: string 文件名
        :param key: string 键名 支持 . 连接的
        :param section: string .ini配置的分区 默认 DEFAULT
        :param flu: bool 刷新后获取 False
        :return: fixed 配置项的值
        """
        self.__load_configs(name=name,section=section,flu=flu)

        if name not in self.__conf_dict:
            return None
        res = self.__conf_dict[name]

        if key:
            ks = key.split('.')
            for k in ks:
                if not isinstance(res,dict) or k not in res:
                    return None
                res = res[k]

        return res



    def set_val(self,name='',key='',val=None,section='DEFAULT',fix=False):
        """
        更改配置文件  该更改只会对当前配置实例有效不会去更改源文件
        :param name: string 文件名
        :param key: string 键名 支持 . 连接的
        :param val: 值 列表，字典，元组，集合 等不支持写入.ini文件
        :param section: string .ini配置的分区 默认 DEFAULT
        :param fix: bool 是否修改.ini配置 False
        :return: bool 是否设置成功 该状态不包含是否写入.ini配置文件成功
        """
        if fix:
            self.set_val_to_ini(name=name,key=key,val=val,section=section)

        if name not in self.__conf_dict:
            return False

        res = self.__conf_dict[name]
        ks = key.split('.')
        num = len(ks)

        for i in range(num):
            k = ks[i]
            if not isinstance(res,dict):
                return False
            if i == num - 1:
                res[k] = val
                return True

        return False



    def del_key(self,name='',key='',section='DEFAULT',fix=False):
        """
        删除一个配置
        :param name: string 文件名  test
        :param key: string 键名  支持.连接
        :param section: string .ini配置的分区  DEFAULT
        :param fix: 是否修改.ini配置  bool False
        :return: bool 是否修改成功 该状态不包含是否写入.ini配置文件成功
        """
        if fix:
            self.del_key_form_ini(name=name,key=key,section=section)

        if name not in self.__conf_dict:
            return True

        res = self.__conf_dict[name]
        ks = key.split('.')
        num = len(ks)

        for i in range(num):
            k = ks[i]
            if not isinstance(res, dict):
                return False
            if i == num - 1:
                del res[k]
                return True

        return False




    def set_val_to_ini(self,name='',section='DEFAULT',key='',val=''):
        """
        修改源.ini配置文件
        :param name: string 文件名  test
        :param section: string 分区  DEFAULT
        :param key: string 键名 不支持.连接，如果使用.连接将按照一个字段来存储
        :param val: 值 不支持 列表，集合，字段，元组 等的写入，写入的值必须是能转化从str的
        :return: bool 是否写入成功
        """
        if section == '' or section.lower() == 'default':
            section = 'DEFAULT'

        try:
            real_path = self.__root + '/'+name+'.ini'
            self.__cf_parse.read(real_path,encoding=self.__encode_str)
            if section != 'DEFAULT' and section not in self.__cf_parse.sections():
                self.__cf_parse.add_section(section=section)

            self.__cf_parse.set(section=section,option=key,value=str(val))
            res = self.__cf_parse.write(open(file=real_path,mode='w',encoding=self.__encode_str))
            return True
        except:
            raise ConfigError("配置写入失败")



    def del_key_form_ini(self,name='',key='',section='DEFAULT'):
        """
        删除.ini配置里的一个值
        :param name: string 文件名
        :param key: string 键名 不支持.连接写法
        :param section: string 分区  DEFAULT
        :return: bool 是否删除成功
        """
        if section == '' or section.lower() == 'default':
            section = 'DEFAULT'
        try:
            self.__cf_parse.read(self.__root + '/' + name + '.ini')
            if section in self.__cf_parse.sections():
                self.__cf_parse.remove_option(section=section,option=key)
                self.__cf_parse.write(open(self.__root+'/'+name+'.ini','w'))
            return True
        except:
            return False
