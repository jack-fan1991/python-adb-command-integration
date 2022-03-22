import os
from lib.decorator.exceptionHandler import Exception_handler
from lib.story.base.baseEzIPStory import BaseEzIPStory
from lib.utils.fileUtils import walkFile
from app import APK_FILE_PATH


class ApkInstallStory(BaseEzIPStory):

    def __init__(self, previous=None, deviceIdx=0) -> None:
        super().__init__(previous=previous, deviceIdx=deviceIdx)

    def _onFailed(self, *args, **kargs):
        """處理失敗"""
        errorInfo = self._onFailed.__doc__
        errorInfo = self._onFailedParser(errorInfo, *args, **kargs)
        failedInfo = self._onFailedinfoParser(*args, **kargs)
        self._printErr(errorInfo)
        self._logger.logger.error(failedInfo + " => " + errorInfo)
        self.start()

    @Exception_handler(onFailed=_onFailed)
    def _findInstallApk(self):
        """可安裝apk"""
        def conditionsFormatter(apkDict: dict):
            conditions = {}
            for k, v in apkDict.items():
                conditions[k] = f" {k} => " + v.split("\\")[1]
            self._resetToOnlyBackCondition(conditions=conditions)

        def actionsFormatter(apkDict: dict):
            """action 皆為 self._apkInstallFlow"""
            actions = {}
            for k, v in apkDict.items():
                actions[k] = self._apkInstallFlow
            self._resetToOnlyBackAction(actions=actions)

        self.apkPathDict = walkFile(APK_FILE_PATH, logger=self._logger.logger.debug)
        conditionsFormatter(self.apkPathDict)
        actionsFormatter(self.apkPathDict)
        return

    def _setCondition(self):
        pass

    def _setAction(self):
        pass

    def _onActionSelect(self, result) -> None:
        """配置installApk 參數"""
        super()._onActionSelect(result)

    @Exception_handler(onFailed=_onFailed)
    def _installApk(self):
        """執行參數由 doBeforeRunAction回調進行配置"""
        # 檢查路徑是否有問題
        if len(self.targetPath) == 0:
            error = f"targetPath is {self.targetPath}"
            self._logger.logger.error(error)
            raise Exception(error)
        if os.path.isfile(self.targetPath) is not True:
            error = f"targetPath is {self.targetPath}"
            self._logger.logger.error(error)
            raise Exception(f"{self.targetPath}=>檔案異常")
        # 檢查是否安裝過
        # info = f"現有apk{self.targetDevice.apkList}"
        # print(info)
        # self._logger.logger.info(info)
        # isExist = self.targetDevice.isApkExist( self.targetApkPath.split("\\")[1])
        # if isExist:
        #     existInfo = f"{self.targetPath}已存在"
        #     print(existInfo)
        #     self._logger.logger.info(existInfo)

        installInfo = "\n\n===========安裝中...===========\n"
        installInfo += ">>>>>" + self.targetPath.split("\\")[1]
        print(installInfo)
        self._logger.logger.info(installInfo)
        # 都走強制安裝
        self.worker.installApk(
            ip=self.targetDevice.ip,
            installApkNamePath=self.targetPath.split("\\")[1],
            isExist=True,
            onFailed=self._onFailed)
        installInfo = "\n\n==========安裝完成===========\n"
        print(installInfo)
        self._logger.logger.info(installInfo)

    def _apkInstallFlow(self):
        self._pushApk()
        self._installApk()
        self._removeAllTempApkFile()
        self._adbDisconnect()
        self._getDevices()

    @Exception_handler(onFailed=_onFailed)
    def _pushApk(self):
        """執行參數由 doBeforeRunAction回調進行配置"""
        uploadInfo = "\n\n===========上傳中...==========="
        print(uploadInfo)
        self._logger.logger.info(uploadInfo)
        self.worker.pushApk(ip=self.targetDevice.ip, installApkNamePath=self.targetPath, onFailed=self._onFailed)
        uploadInfo = "\n\n===========上傳成功==========="
        print(uploadInfo)
        self._logger.logger.info(uploadInfo)

    @Exception_handler(onFailed=_onFailed)
    def _removeAllTempApkFile(self):
        """移暫存檔"""
        self._logger.logger.info(f"{self._adbDisconnect.__doc__}")
        self.worker.removeAllTempApkFile(ip=self.targetDevice.ip, installApkName=self.targetPath, onFailed=self._onFailed)

    @Exception_handler()
    def _adbDisconnect(self):
        """斷開連接"""
        self._logger.logger.info(f"{self._adbDisconnect.__doc__}")
        self.worker.adbDisconnect(ip=self.targetDevice.ip, onFailed=self._onFailed)

    @Exception_handler()
    def _getDevices(self):
        """查看連接devices"""
        self._logger.logger.info(f"{self._adbDisconnect.__doc__}")
        self.worker.getDevices(onFailed=self._onFailed)

    def _startInput(self):
        """"選擇apk"""
        super()._startInput(onFailed=self._onFailed)

    def start(self):
        self._findInstallApk()
        self._startInput()
        # go back
        super()._setGoBack()

    def getNextStory(self):
        return self.nextStory
