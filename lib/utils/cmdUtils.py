from lib.decorator.exceptionHandler import Exception_handler
import os
from lib.decorator.thread import ThreadDecarator
from lib.utils.logger import MyLogger
import subprocess, datetime, time, signal
from app import CMD_TIMEOUT
_logger = MyLogger(__name__)

CMD_WATCH_DOG = 0.2
class Cmd:
    class CmdTimeOutError(Exception):
        pass
    # @staticmethod
    # @Exception_handler()
    # def call(commend: str, printResp=True, onFailed=None) -> str:
    #     print(f'{commend}')
    #     _logger.logger.info(commend)
    #     pip = os.popen(commend)
    #     cmdResult = pip.buffer.read().decode(encoding='utf8')
    #     info = f'response : {cmdResult}'
    #     if printResp:
    #         print(info)
    #     _logger.logger.info(info)
    #     return cmdResult
    @staticmethod
    @Exception_handler(throwException=True)
    def call(commend: str, timeoutSeconds=CMD_TIMEOUT, printResp=True, onFailed=None, **kargs) -> str:
        start = datetime.datetime.now()
        print(f'{commend}')
        _logger.logger.info(commend)
        process = subprocess.Popen(commend, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        desplayTime: int = 0
        while process.poll() is None:
            time.sleep(CMD_WATCH_DOG)
            desplayTime += CMD_WATCH_DOG
            now = datetime.datetime.now()
            totalTime = (now - start).seconds
            # _logger.logger.debug(f"{commend} : run Time : {round(desplayTime, 2)}")
            if round(desplayTime, 2) % 1 == 0:
                if round(desplayTime, 1) % 30 == 0:
                    print("#", end="", flush=True)
                    print(f"\n{round(desplayTime, 1)} Sec", flush=True)
                else:
                    print("#", end="", flush=True)

            if totalTime > timeoutSeconds:
                os.kill(process.pid, signal.SIGINT)
                _logger.logger.info(f"{commend} : time out at : {totalTime}")
                print(f"time out at : {totalTime}")
                print("", flush=True)
                raise Cmd.CmdTimeOutError("沒有回應")
        print("", flush=True)
        _logger.logger.info(f"{commend} : Done at : {totalTime}")
        return "".join(result.decode(encoding='utf8', errors='ignore') for result in process.stdout.readlines() )

    @staticmethod
    @ThreadDecarator
    @Exception_handler()
    def do_call_in_baground(commend: str, **kwargs) -> str:
        """"多執行續在結果回傳前先回傳當前thread可調用waitResult()執行等待
            細節請參照ThreadDecarator
            @ param : onFailed 可於exception時進行回調
            @ param : conditionFilter 定義ThreadDecarator 對執行續結果成功與失敗進行分類於
            class ThreadDecarator:
                # 管理執行續成功結果
                Success_list = []
                # 管理執行續失敗結果
                Failed_list = []      
        """
        print(f'{commend}')
        _logger.logger.info(commend)
        pip = os.popen(commend)
        cmdResult = pip.buffer.read().decode(encoding='utf8')
        info = f'response : {cmdResult}'
        print(info)
        _logger.logger.info(info)
        return cmdResult

    @Exception_handler()
    def do_adb_connect_in_baground(ip: str, **kwargs) -> str:
        """"多執行續在結果回傳前先回傳當前thread可調用waitResult()執行等待
            細節請參照ThreadDecarator
        """
        commend: str = f"adb connect {ip}"
        cmdResult = Cmd.do_call_in_baground(commend, **kwargs)
        info = f'adb connect response : {cmdResult}'
        print(info)
        _logger.logger.info(info)
        return cmdResult

    @Exception_handler()
    def do_adb_connect(ip: str, **kwargs) -> str:
        commend: str = f"adb connect {ip}"
        cmdResult = Cmd.call(commend, **kwargs)
        info = f'adb connect response : {cmdResult}'
        print(info)
        _logger.logger.info(info)
        return cmdResult


    
    # @staticmethod
    # def some_adb_cmd():
    #     p = subprocess.Popen('adb shell cd sdcard&&ls&&cd ../sys&&ls',
    #     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #     return_code = p.poll()
    #     while return_code is None:
    #     line = p.stdout.readline()
    #     return_code = p.poll()
    #     line = line.strip()
    #     if line:
    #     print line
    #     print "Done"