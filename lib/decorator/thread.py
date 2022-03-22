import sys, os
if __name__ == '__main__':
    sys.path.insert(0, './')
from threading import currentThread
import time
from lib.decorator.exceptionHandler import Exception_handler
from lib.utils.logger import MyLogger
from threading import Thread
_logger = MyLogger(__name__)


class ThreadDecarator:
    '''
    函數的線程裝飾器，返回thread線程實例，waitResult獲取結果,
    MyThread.waitResult 獲取結果集合
    @ param : conditionFilter 
    '''
    # 管理執行續實體
    Thread_dict = {}
    # 管理執行續任務結果
    Result_dict = {}
    # 管理執行續成功結果
    Success_list = []
    # 管理執行續失敗結果
    Failed_list = []

    class InnerThread(Thread):
        def __init__(self, func, name='', *args, **kwargs):
            Thread.__init__(self)
            self.func = func
            self.name = name
            self.args = args
            self.kwargs = kwargs
            self.conditionFilter = kwargs.get("conditionFilter", None)
            _logger.logger.debug(self.info())

        def run(self):
            print(f"{self} start with thread_wrap_class...")
            self.taskResult = self.func(*self.args, **self.kwargs)
            if self.conditionFilter is not None:
                if self.conditionFilter(result=self.taskResult):
                    ThreadDecarator.Success_list.append(self.taskResult)
                else:
                    ThreadDecarator.Failed_list.append(self.taskResult)
            ThreadDecarator.updateThreadResult(thread=self, result=self.taskResult)

        def waitResult(self):
            """返回task"""
            self.join()
            return self.taskResult

        def info(self):
            ident = self.ident if self.ident is not None else " "*5
            result = f"[{ident}] Task : {self.func.__name__}() , Thread Name : {self.name} , args : {self.args} , kwargs : {self.kwargs} , "
            return result

    def __init__(self, func):
        self.func = func

    @Exception_handler()
    def __call__(self, *args, **kwargs) -> InnerThread:
        # 產生Thread
        _mythread = self.InnerThread(self.func, self.func.__name__, *args, **kwargs)
        _mythread.start()
        ThreadDecarator.addThread(_mythread)
        return _mythread

    @classmethod
    def waitAllResult(cls):
        for k, thr in cls.Thread_dict.items():
            thr.join()
        return cls.Result_dict

    @classmethod
    def addThread(cls, thread: InnerThread) -> None:
        cls.Thread_dict[thread.ident] = thread

    @classmethod
    def updateThreadResult(cls, thread: InnerThread, result) -> None:
        cls.Result_dict[thread.ident] = result

    @classmethod
    def successList(cls) -> list:
        return cls.Success_list

    @classmethod
    def failedList(cls) -> list:
        return cls.Success_list


def click(callback, *args, **kwargs):
    # print('in main func with <', callback.__name__, '>', *args, **kwargs)
    return callback(*args, **kwargs)


@ThreadDecarator
def event(s):
    time.sleep(s)
    global g_a
    g_a += s
    _logger.logger.debug(f'{currentThread()} < event > finished! {s} {g_a}')
    return 'event Result ：' + str(s) + '|' + str(g_a)


if __name__ == '__main__':
    g_a = 100
    event(4)
    a = event(5)
    _logger.logger.debug('a:', a.waitResult())
    click(event, 3)
    click(event, 6)
    # 等待所有人結束
    _logger.logger.debug(f'event all:{ ThreadDecarator.waitAllResult()}')
