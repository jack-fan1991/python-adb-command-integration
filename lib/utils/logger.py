if __name__ == '__main__':
    import sys, os
    sys.path.append(os.getcwd())
import logging
import app as App
import traceback

class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;20"
    blue = "\x1b[;34;20m"
    yellow = "\x1b[33;20m"
    green = "\x1b[;32;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    # format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: blue + App.LOG_FORMAT + reset,
        logging.INFO: green + App.LOG_FORMAT + reset,
        logging.WARNING: yellow + App.LOG_FORMAT + reset,
        logging.ERROR: bold_red + App.LOG_FORMAT + reset,
        logging.CRITICAL: bold_red + App.LOG_FORMAT + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class MyLogger(object):
    def __init__(self, name: str = None):
        self.logger = logging.getLogger(name)    
        self.logger.handlers =logging.getLogger().handlers  
        # self.logger.addHandler(App.writer)
        # if App.APPMODE is App.Mode.DEBUG:
        #     if App.LOGGER_COLOR_PRINT:
        #         App.colorConsole.setFormatter(CustomFormatter())
        #         self.logger.addHandler(App.colorConsole)
        #     if App.LOGGER_EZPRINT:
        #         self.logger.addHandler(App.ezConsole)
        # 禁用預設
        self.logger.propagate = False

    def _getMethodName(self, method: str):
        if method is not None:
            return method+"() | "
        stack = traceback.extract_stack()
        return stack[-3].name+"() | "

    # 裝飾器使用的log方法若要調用要手動查找方法 lineno
    def _debug(self, msg, method: str = None, *args, **kwargs):
        self.logger.debug(self._getMethodName(method) + msg, *args, **kwargs)

    def _info(self, msg, method: str = None, *args, **kwargs):
        self.logger.info(self._getMethodName(method) + msg, *args, **kwargs)

    def _warning(self, msg, method: str = None, *args, **kwargs):
        self.logger.warning(self._getMethodName(method) + msg, *args, **kwargs)

    def _error(self, msg, method: str = None, *args, **kwargs):
        self.logger.error(self._getMethodName(method) + msg, *args, **kwargs)

    def _critical(self, msg, method: str = None, *args, **kwargs):
        self.logger.critical(self._getMethodName(method) + msg, *args, **kwargs)
# def log_error():
#     """
#     We create a parent function to take arguments
#     :param path:
#     :return:
#     """

#     def error_log(func):

#         @functools.wraps(func)
#         def wrapper(*args, **kwargs):

#             try:
#                 # Execute the called function, in this case `divide()`.
#                 # If it throws an error `Exception` will be called.
#                 # Otherwise it will be execute successfully.
#                 return func(*args, **kwargs)
#             except Exception as e:
#                 error_msg = 'And error has occurred at /' + func.__name__ + '\n'
#                 logger.exception(error_msg)

#                 return e  # Or whatever message you want.

#         return wrapper

#     return error_log


def testMethodCall():
    log = MyLogger("test")
    log._debug('debug')


if __name__ == '__main__':
    log = MyLogger()
    log._debug('debug')
    log.logger.debug('debug')
    log._info('info')
    log._warning('警告')
    log._error('報錯')
    log._critical('嚴重')
    testMethodCall()
    # logger.critical('嚴重sss')
    # Logger('logs\\error', level='error').logger.error('error')