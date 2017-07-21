import logging
 
# 使用logging模块：
class Log:
    # ----------------------------------------------------------------------------
    def __init__(self):
        #日志文件的存放路径，根据自己的需要去修改
        logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                filename='log.log',
                filemode='w')

#################################################################################################
#定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
 
    def DebugMessage(self, msg):
        self.logger.debug(msg)
        pass
