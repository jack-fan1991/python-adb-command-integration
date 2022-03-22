from lib.decorator.exceptionHandler import Exception_handler
from lib.story.removeAppStory import RemoveAppStory

"""APP初始化移除 App中的shpreferences.xml"""

class RemoveSdCardFileStory(RemoveAppStory):

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
    def _removeFile(self):
        """初始化..."""
        self._logger.logger.info(f"{self.targetPath }{self._removeFile.__doc__}")
        filePath = f"data/data/{self.targetPath}/shared_prefs/{self.targetPath}_preferences.xml"
        # self.worker.stopApp(ip=self.targetDevice.ip, applicationID=self.targetPath, onFailed=self._onFailed)
        self.worker.removeFile(ip=self.targetDevice.ip, filePath=filePath, onFailed=self._onFailed)
        info = f"==========={self.targetPath}初始化完成==========="
        print(info)
        self._logger.logger.info(info)
    
    def _doAction(self):
        self._removeFile()

    # def setNextToApkInstallStory(self):
    #     self.nextStory = ApkInstallStory(previous=self, deviceIdx=self.deviceIdx)

    def _startInput(self):
        """選擇要初始化的APP"""
        super()._startInput()
