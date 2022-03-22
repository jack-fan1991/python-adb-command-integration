
import logging
import socket
from lib.core.baseObj import BaseObj
from lib.decorator.exceptionHandler import Exception_handler
from lib.decorator.thread import ThreadDecarator
from lib.utils.logger import MyLogger
from lib.model.device import Device
from lib.utils.adbCmdUtils import AdbCmdUtils
from lib.utils.baseUtils import BaseUtils

_logger = MyLogger(__name__)


class Worker(BaseObj):
    deviceMap = {}
    IPPrefix: str = ""

    def __init__(self) -> None:
        pass

    @classmethod
    def getConnectIpPrefix(cls) -> str:
        """"檢查目前連線"""
        title: str = f"\n\n==========={Worker.inputConnectIp.__doc__}===========\n"
        ip: str = cls.getConnectIp()
        Worker.IPPrefix = ".".join(ip.split(".")[:3])
        info = f'網域IP = {Worker.IPPrefix}.XX'
        print(title)
        _logger.logger.info(title)
        print(info)
        _logger.logger.info(info)
        return Worker.IPPrefix

    @classmethod
    def getConnectIp(cls) -> str:
        """取得連線IP"""
        title: str = f"\n\n==========={cls.getConnectIp.__doc__}===========\n"
        ip: str = socket.gethostbyname(socket.gethostname())
        Worker.IPPrefix = ".".join(ip.split(".")[:3])
        info = f'當前連線IP : {ip}'
        print(title)
        _logger.logger.info(title)
        print(info)
        _logger.logger.info(info)
        return ip

    @classmethod
    def inputConnectIp(cls) -> str:
        """手動設定網域IP,格式 : XX.XX.XX.XX  or  XX.XX.XX"""
        title: str = f"\n\n==========={cls.inputConnectIp.__doc__}===========\n=>"
        # 每一區段不能大於3
        condiction = lambda x: len(str(x)) > 3
        while True:
            _logger.logger.info(title)
            result = input(f"{title}")
            result = result.replace(" ", "")
            result = str(result)
            if len(result.split(".")) < 3 or len(result.split(".")) > 4:
                error = f'IP = {result} , [格式不符,請參照格式=>XX.XX.XX.XX]'
                Worker.printErr(error)
                _logger.logger.error(error)
                continue
            # 每一區段不能大於3
            if any([condiction(result) for result in result.split(".")]) is True:
                error = f'IP = {result} , [格式不符,每一區段不能大於3]'
                Worker.printErr(error)
                _logger.logger.error(error)
                continue
            Worker.IPPrefix = ".".join(result.split(".")[:3])
            break
        info = f'IP = {Worker.IPPrefix}.XX'
        print(info)
        _logger.logger.info(info)
        return Worker.IPPrefix

    @classmethod
    def setTargetIP(cls, clearIPMap: bool = True) -> str:
        """設定連線目標IP,格式 : XX.XX.XX.XX"""
        title: str = f"\n\n==========={cls.setTargetIP.__doc__}===========\n=>"
        # 每一區段不能大於3
        condiction = lambda x: len(str(x)) > 3
        while True:
            _logger.logger.info(title)
            result = input(f"{title}")
            result=result.replace(" ", "")
            result = str(result)
            if len(result.split(".")) != 4:
                error = f'IP = {result} , [格式不符,請參照格式=>XX.XX.XX.XX]'
                Worker.printErr(error)
                _logger.logger.error(error)
                continue
            cls.getConnectIp()
            # if Worker.IPPrefix not in result:
            #     error = f'IP = {result} , [當前網域為 : {Worker.IPPrefix} 連線目標IP : {result} 於不同網域]'
            #     Worker.printErr(error)
            #     _logger.logger.error(error)
            #     continue
            # 每一區段不能大於3
            if any([condiction(result) for result in result.split(".")]) is True:
                error = f'IP = {result} , [格式不符,每一區段不能大於3]'
                Worker.printErr(error)
                _logger.logger.error(error)
                continue
            Worker.IPPrefix = ".".join(result.split(".")[:3])
            break
        info = f'連接裝置 IP = {result} '
        print(info)
        _logger.logger.info(info)
        if clearIPMap:
            cls.clearDeviceMap()
        cls.addDevice(result)
        _logger.logger.info(f"addIP Result {cls.deviceMap}")

    @classmethod
    def addDevice(cls, ip: str):
        idx = len(cls.deviceMap)
        cls.deviceMap[idx] = Device(ip)

    @classmethod
    def clearDeviceMap(cls):
        cls.deviceMap = {}

    @classmethod
    def IPMapVerification(cls) -> bool:
        if BaseUtils.isDictEmpty(cls.deviceMap) or len(cls.deviceMap) > 1:
            return False
        return True

    @classmethod
    def isDeviceMapEmpty(cls) -> bool:
        return BaseUtils.isDictEmpty(cls.deviceMap)


    @Exception_handler()
    def getIP(self, **kwargs):
        try:
            for i in range(0, 255):
                if(i < 10):
                    i = f'0{i}'
                ip = f"{Worker.IPPrefix}.{i}"
                reslt = self.adbConnect(ip)
            # 等待所有人結束
            ThreadDecarator.waitAllResult()
            print(f"=========={len(ThreadDecarator.Success_list)}個連線==========")
            print("\n".join(ThreadDecarator.Success_list))
            print(f"=========={len(ThreadDecarator.Failed_list)}個連線失敗==========")
            # print("\n".join(ThreadDecarator.Failed_list))
            # if "connected" in reslt:
            #         Worker.IPList.append(ip)
        except Exception as e:
            print(e)

    def cmdFailed(self, *args, **kargs):
        print("return")

    @Exception_handler()
    def getIP(self, onAdbConnectSuccessFilter, **kwargs):
        def adbConnect(ip):
            reslt = AdbCmdUtils.do_adb_connect_in_baground(ip=ip, onFailed=self.cmdFailed, conditionFilter=onAdbConnectSuccessFilter)
        try:
            for i in range(0, 255):
                if(i < 10):
                    i = f'0{i}'
                ip = f"{Worker.IPPrefix}.{i}"
                reslt = adbConnect(ip)
            # 等待所有人結束
            ThreadDecarator.waitAllResult()
            print(f"=========={len(ThreadDecarator.Success_list)}個連線==========")
            print("\n".join(ThreadDecarator.Success_list))
            print(f"=========={len(ThreadDecarator.Failed_list)}個連線失敗==========")
            # print("\n".join(ThreadDecarator.Failed_list))
            # if "connected" in reslt:
            #         Worker.IPList.append(ip)
        except Exception as e:
            print(e)

    @Exception_handler(throwException=True)
    def startAdbConnect(self, deviceIdx: int, logger: logging, onFailed=None, **kwargs):
        device: Device = Worker.deviceMap.get(deviceIdx)
        if device is None:
            info = f"{len(Worker.deviceMap)} 數量異常"
            logger.warning(info)
            raise Exception(info)
        result = self.adbConnect(device.ip, onFailed=onFailed)
        if AdbCmdUtils.onAdbConnectSuccessFilter(result=result):
            print("連接成功")
            logger.info("連接成功")
        else:
            print("連接失敗")
            logger.error("連接失敗")
            raise Exception("連接失敗")

    def adbConnect(self, ip: str, onFailed=None, **kwargs):
        return AdbCmdUtils.adbConnect(ip=ip, onFailed=onFailed, **kwargs)

    def adbDisconnect(self, ip: str, onFailed=None, **kwargs):
        return AdbCmdUtils.adbDisConnect(ip=ip, onFailed=onFailed,)

    def getDevices(self, onFailed=None, **kwargs):
        return AdbCmdUtils.getDevices(onFailed=onFailed)

    def showApk(self, ip: str, onFailed=None, **kwargs):
        return AdbCmdUtils.showApk(ip=ip, onFailed=onFailed)

    def installApk(self, ip: str, installApkNamePath: str, isExist: bool = False, onFailed=None, **kwargs):
        return AdbCmdUtils.installApk(ip=ip, installApkNamePath=installApkNamePath, isExist=isExist, onFailed=onFailed)

    def pushApk(self, ip: str, installApkNamePath: str, onFailed=None, **kwargs):
        return AdbCmdUtils.pushApk(ip=ip, installApkNamePath=installApkNamePath, onFailed=onFailed)

    def removeApp(self, ip: str, applicationID: str, onFailed=None, **kwargs):
        return AdbCmdUtils.removeApp(ip=ip, applicationID=applicationID, onFailed=onFailed)

    def removeAllTempApkFile(self, ip: str, onFailed=None, **kwargs):
        return AdbCmdUtils.removeAllTempApkFile(ip=ip, onFailed=onFailed)

    def startApp(self, ip: str, applicationID: str, onFailed=None, **kwargs):
        return AdbCmdUtils.startApp(ip=ip, applicationID=applicationID, onFailed=onFailed)

    def removeFile(self, ip: str, filePath: str, onFailed=None, **kwargs):
        return AdbCmdUtils.removeFile(ip=ip, filePath=filePath, onFailed=onFailed)

    def stopApp(self, ip: str, applicationID: str, onFailed=None, **kwargs):
        return AdbCmdUtils.stopApp(ip=ip, applicationID=applicationID, onFailed=onFailed)

    def screenShot(self, ip: str, onFailed=None, **kwargs):
        return AdbCmdUtils.screenShot(ip=ip, onFailed=onFailed)

    def pullPNG(self, ip: str, onFailed=None, **kwargs):
        return AdbCmdUtils.pullPNG(ip=ip, onFailed=onFailed)
 
    def cleanPNG(self, ip: str, onFailed=None, **kwargs):
        return AdbCmdUtils.cleanPNG(ip=ip, onFailed=onFailed)

    @staticmethod
    def printErr(err):
        print("!!"*5+err+"!!"*5)
