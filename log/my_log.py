import logging
from logging.handlers import TimedRotatingFileHandler
import logging, os, sys, time

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class MyLog(object):
    __metaclass__ = Singleton

    logger = logging.getLogger(__name__)
    log_file = 'my.log'

    def __init__(self):
        self.logger.setLevel(logging.ERROR)
        self.init_logger()

    @classmethod
    def get_logger(cls):
        return cls.logger

    def init_logger(self):
        log_path = os.path.dirname(os.path.realpath(__file__)) + '/logs'
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        log_file_tmp = os.path.join(log_path, self.log_file)

        logging_msg_format = '[%(asctime)s] [%(levelname)s] [%(filename)s] [%(funcName)s] [%(lineno)d] %(message)s'

        fh = logging.handlers.RotatingFileHandler(
            log_file_tmp, maxBytes=100*1024*1024, backupCount=10000)
        fh.setFormatter(logging.Formatter(logging_msg_format))
        self.logger.addHandler(fh)
        

def singleton(cls):
  instances = {}
  def _singleton(*args,**kwargs):
    if cls not in instances:
      instances[cls] = cls(*args,**kwargs)
    return instances[cls]
  return _singleton
 
@singleton
class Logger():
    def __init__(self,logfile=None):
        self.logger = logging.getLogger()
        formater = logging.Formatter('%(asctime)s %(name)s  %(levelname)s %(filename)s  %(lineno)d '
                        '%(thread)d %(threadName)s %(process)d %(message)s')
        if logfile == None:
            cur_path = os.path.split(os.path.realpath(__file__))[0]
            stime = time.strftime("%Y-%m-%d",time.localtime())
            logfile = cur_path + os.sep + "log_" + stime + ".log"
        else:
            logfile = logfile
        self.sh = logging.StreamHandler(sys.stdout)
        self.sh.setFormatter(formater)
        self.fh = logging.FileHandler(logfile)
        self.fh.setFormatter(formater)
        self.logger.addHandler(self.sh)
        self.logger.addHandler(self.fh)
        self.logger.setLevel(logging.WARNING)