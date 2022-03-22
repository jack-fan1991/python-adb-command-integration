
import math as math
import os
from lib.decorator import Exception_handler
from lib.utils.logger import MyLogger
from lib.utils.cmdUtils import Cmd

_logger = MyLogger(__name__)
PORT = 5555

class AdbCmdUtils(Cmd):
    @staticmethod
    @Exception_handler()
    def do_adb_connect_in_baground(ip: str, **kwargs) -> str:
        """"多執行續在結果回傳前先回傳當前thread可調用waitResult()執行等待
            細節請參照ThreadDecarator
        """
        commend: str = f"adb connect {ip}:{PORT}"
        cmdResult = Cmd.do_call_in_baground(commend, **kwargs)
        info = f'adb connect response : {cmdResult}'
        print(info)
        _logger.logger.info(info)
        return cmdResult

    @staticmethod
    @Exception_handler()
    def adbConnect(ip: str, **kwargs) -> str:
        commend: str = f"adb connect {ip}:{PORT}"
        print("連接中...")
        cmdResult = Cmd.call(commend, **kwargs)
        info = f'adb connect response : {cmdResult}'
        print(info)
        _logger.logger.info(info)
        if AdbCmdUtils.onAdbConnectSuccessFilter(result=cmdResult):
            return cmdResult
        else:
            print("ip 連接失敗")
            raise Exception(f"adbConnect failed {cmdResult}")

    @staticmethod
    @Exception_handler()
    def adbDisConnect(ip: str, **kwargs) -> str:
        commend: str = f"adb disconnect {ip}:{PORT}"
        cmdResult = Cmd.call(commend, printResp=False, **kwargs)
        info = f'adb disconnect response : {cmdResult}'
        print(info)
        _logger.logger.info(info)
        return cmdResult

    @staticmethod
    @Exception_handler()
    def getDevices(**kwargs) -> str:
        commend: str = "adb devices"
        cmdResult = Cmd.call(commend, printResp=False, **kwargs)
        info = f'adb devices response : {cmdResult}'
        print(info)
        _logger.logger.info(info)
        return cmdResult

    @staticmethod
    def onAdbConnectSuccessFilter(**kargs) -> bool:
        """
        解析參數名稱
        @Param : result
        """
        result = kargs.get('result', None)
        if result is not None and "connected" in result:
            return True
        else:
            return False

    @staticmethod
    @Exception_handler()
    def showApk(ip: str, **kwargs) -> str:
        commend: str = f"adb -s  {ip}:{PORT}  shell pm list packages"
        cmdResult = Cmd.call(commend, printResp=False, **kwargs)
        info = f'adb list packages response : {cmdResult}'
        _logger.logger.debug(info)
        return cmdResult

    @staticmethod
    @Exception_handler()
    def installApk(ip: str, installApkNamePath: str, isExist: bool = False, **kwargs) -> str:
        commend: str = f"adb -s  {ip}:{PORT}  shell pm install -g /data/local/tmp/{installApkNamePath}"
        if isExist:
            commend: str = f"adb -s  {ip}:{PORT}  shell pm install -g -r /data/local/tmp/{installApkNamePath}"
        cmdResult = Cmd.call(commend, timeoutSeconds=120, **kwargs)
        info = f'adb pm install response : {cmdResult}'
        print(info)
        _logger.logger.info(info)
        if "Success" not in cmdResult:
            print("installApk failed")
            raise Exception(f"installApk failed {cmdResult}")
        return cmdResult

    @Exception_handler()
    def pushApk(ip: str, installApkNamePath: str, onFailed=None, **kwargs) -> str:
        cmdResult = Cmd.call(f"adb -s {ip}:{PORT} root", **kwargs)
        cmdResult = Cmd.call(f"adb -s {ip}:{PORT} remount", **kwargs)
        commend: str = f"adb -s {ip}:{PORT} push {installApkNamePath} /data/local/tmp"
        cmdResult = Cmd.call(commend, **kwargs)
        info = f'pushApk response : {cmdResult}'
        print(info)
        _logger.logger.info(info)
        if "pushed" not in cmdResult or 'failed' in cmdResult:
            raise Exception(f"push上傳失敗 {cmdResult}")
        return cmdResult

    @Exception_handler()
    def removeApp(ip: str, applicationID: str, onFailed=None, **kwargs) -> str:
        commend: str = f"adb -s {ip}:{PORT} shell pm uninstall {applicationID}"
        cmdResult = Cmd.call(commend, **kwargs)
        info = f'startApp response : {cmdResult}'
        print(info)
        _logger.logger.info(info)
        return cmdResult

    @Exception_handler()
    def startApp(ip: str, applicationID: str, onFailed=None, **kwargs) -> str:
        commend: str = f"adb -s {ip}:{PORT} shell am start -n  \"{applicationID}/com.gsh.biofit2.online.samples.NewMainActivity\" -a android.intent.action.MAIN -c android.intent.category.LAUNCHER"
        cmdResult = Cmd.call(commend, **kwargs)
        info = f'startApp response : {cmdResult}'
        print(info)
        _logger.logger.info(info)
        return cmdResult


    @Exception_handler()
    def removeTempApkFile(ip: str, installApkNamePath: str, onFailed=None, **kwargs) -> str:
        commend: str = f"adb -s {ip}:{PORT} shell rm -f /data/local/tmp/{installApkNamePath}"
        cmdResult = Cmd.call(commend, **kwargs)
        info = f'已刪除存檔: {installApkNamePath}'
        print(info)
        _logger.logger.info(info)

        return cmdResult

    @Exception_handler()
    def removeAllTempApkFile(ip: str, onFailed=None, **kwargs) -> None:
        commend: str = f"adb -s {ip}:{PORT} ls /data/local/tmp"
        cmdResult = Cmd.call(commend, **kwargs)
        info = f'pushApk response : {cmdResult}'
        print(info)
        _logger.logger.info(info)
        result = AdbCmdUtils.listPackagefilter(
            ['.apk'],
            cmdResult,
            filter=AdbCmdUtils.keepPackageFilter,
            logger=_logger.logger.debug)
        for namePath in result:
            namePath = namePath.split(" ")[-1]
            _logger.logger.info(f"準備移除{namePath}")
            AdbCmdUtils.removeTempApkFile(ip=ip, installApkNamePath=namePath)

    @Exception_handler()
    def removeFile(ip: str, filePath: str, onFailed=None, **kwargs) -> None:
        cmdResult = Cmd.call(f"adb -s {ip}:{PORT} root", **kwargs)
        cmdResult = Cmd.call(f"adb -s {ip}:{PORT} remount", **kwargs)
        commend: str = f"adb -s {ip}:{PORT} shell rm -f {filePath}"
        cmdResult = Cmd.call(commend, **kwargs)
        info = f'開始除 : {filePath}'
        # print(info)
        _logger.logger.info(info)
        info = f'pushApk removeFile path : {filePath}'
        # print(info)
        _logger.logger.info(info)


    @Exception_handler()
    def stopApp(ip: str, applicationID: str, onFailed=None, **kwargs) -> None:
        commend: str = f"adb -s {ip}:{PORT} shell am force-stop {applicationID}"
        cmdResult = Cmd.call(commend, **kwargs)
        info = f'停止 : {applicationID}'
        # print(info)
        _logger.logger.info(info)
        info = f'pushApk stopApp path : {applicationID}'
        # print(info)
        _logger.logger.info(info)

    @Exception_handler()
    def screenShot(ip: str, onFailed=None, **kwargs) -> None:
        cmdResult = Cmd.call(f"adb -s {ip}:{PORT} shell mkdir /sdcard/tempPng")
        lsCommend = Cmd.call(f"adb -s {ip}:{PORT} shell ls /sdcard/tempPng")
        cmdResult = Cmd.call(f"adb -s {ip}:{PORT} shell screencap -p /sdcard/tempPng/{AdbCmdUtils.getPngName(lsCommend)}")

        # print(info)
    @staticmethod
    def getPngName(lsCommend: str):
        lsResp = lsCommend.replace("\n", "").split('\r')
        maxVal: int = 0
        for name in lsResp:
            if "png" in name:
                maxVal = max(maxVal, int(name.split(".")[0]))
        return f"{maxVal+1}.png"

    @Exception_handler()
    def pullPNG(ip: str, onFailed=None, **kwargs) -> None:
        commend: str = f"adb -s {ip}:{PORT} pull /sdcard/tempPng"
        cmdResult = Cmd.call(commend, **kwargs)
        info = f'拉取圖片至 /tempPng'
        print(info)
        _logger.logger.info(info)

    @Exception_handler()
    def cleanPNG(ip: str, onFailed=None, **kwargs) -> None:
        commend: str = f"adb -s {ip}:{PORT} shell rm -r /sdcard/tempPng"
        cmdResult = Cmd.call(commend, **kwargs)
        info = f'清除裝置內暫存照片'
        print(info)
        _logger.logger.info(info)




    @staticmethod
    def skipPackageFilter(prefixs: list, packageName: str, logger=None):
        """filter 結果為True的將被保留"""
        for prefix in prefixs:
            if prefix in packageName:
                if logger is not None:
                    logger(f"skip packageName : {packageName}")
                return True
        if logger is not None:
            logger(f"keep packageName : {packageName}")
        return False

    @staticmethod
    def keepPackageFilter(prefixs: list, packageName: str, logger=None):
        """filter 結果為True的將被保留"""
        for prefix in prefixs:
            if prefix in packageName:
                if logger is not None:
                    logger(f"keep packageName : {packageName}")
                return False
        if logger is not None:
            logger(f"skip packageName : {packageName}")
        return True

    @staticmethod
    def listPackagefilter(dropPackagePrefix, listPackageResp, filter, logger=None):
        """filter 結果為True的將被保留"""
        listPackageResp = listPackageResp.replace("\n", "").split('\r')
        if logger is not None:
            logger(f"skip packageName  if contain {dropPackagePrefix}")
        condiction = lambda x : filter(dropPackagePrefix, x, logger=logger)
        dropResult = [condiction(packageName) for packageName in listPackageResp]
        outList = []
        for i, v in enumerate(dropResult):
            if v:
                continue
            packageName = listPackageResp[i].replace("\n", "")
            if packageName == "":
                continue
            outList.append(packageName)
        return outList