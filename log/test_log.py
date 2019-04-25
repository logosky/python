#!/usr/bin/python
# -*- coding: UTF-8 -*-


from my_log import MyLog, Logger, Singleton

logger = MyLog().get_logger()
        
lg = Logger()
def main():
    print "test"
    
    logger.debug('debug log')
    logger.info('info log')
    logger.warning('warning log')
    logger.error('error log')
    logger.critical('critical log')
    
    lg.logger.debug('debug log')
    lg.logger.info('info log')
    lg.logger.warning('warning log')
    lg.logger.error('error log')
    lg.logger.critical('critical log')
    
if __name__ == '__main__':
    main()
