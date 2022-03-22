from lib.story.base.baseIPStory import BaseIPStory


class StartAppStory(BaseIPStory):

    def __init__(self, previous=None, deviceIdx=0) -> None:
        super().__init__(previous=previous, deviceIdx=deviceIdx)

    def onFailed(self, *args, **kargs):
        """處理失敗"""
        errorInfo = self.onFailed.__doc__
        errorInfo = self._onFailedParser(errorInfo, *args, **kargs)
        failedInfo = self._onFailedinfoParser(*args, **kargs)
        self._printErr(errorInfo)
        self._logger.logger.error(failedInfo + " => " + errorInfo)
        self.start()

    def _setCondition(self):
        super()._resetToOnlyBackCondition()
        for k, v in enumerate(self.targetDevice.apkList):
            self.conditions[k+1] = f" {k+1} => " + v.split(":")[1]
            self.apkPathDict[k+1] = v.split(":")[1]

    def _setAction(self):
        """執行參數由 doBeforeRunAction回調進行配置"""
        super()._resetToOnlyBackAction()
        for k, v in enumerate(self.targetDevice.apkList):
            self.actions[k+1] = self.startApk
        pass

    def doActionSelect(self, result) -> None:
        return super()._doActionSelect(result)

    def startApk(self):
        self.worker.startApp(ip=self.targetDevice.ip, applicationID=self.targetPath, onFailed=self.onFailed)
        info = f"==========={self.targetPath}已啟動==========="
        print(info)
        self._logger.logger.info(info)

    # def setNextToApkInstallStory(self):
    #     self.nextStory = ApkInstallStory(previous=self, deviceIdx=self.deviceIdx)

    def _startInput(self):
        """選擇啟動的APP"""
        super()._startInput(onFailed=self.onFailed)

    def start(self):
        self._setCondition()
        self._setAction()
        self._startInput()
        super()._setGoBack()

    def getNextStory(self):
        return self.nextStory
