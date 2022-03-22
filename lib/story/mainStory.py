
from lib.story.apkInstallStory import ApkInstallStory
from lib.story.base.baseIPStory import BaseIPStory
from lib.story.onlyCMDStory import OnlyCMDStory
from lib.story.removeAppStory import RemoveAppStory
from lib.story.removeSdCardFileStory import RemoveSdCardFileStory
from lib.story.screenShotStory import ScreenShot
from lib.story.startAppStory import StartAppStory
import os

"""主要選擇行為的頁面"""


class MainStory(BaseIPStory):

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

    def _setCondition(self):
        self.conditions = {
            0: "  0 => 返回",
            1: "  1 => 安裝apk",
            2: "  2 => APP啟動",
            3: "  3 => APP移除",
            4: "  4 => APP初始化",
            5: "  5 => 命令模式",
            6: "  6 => 螢幕截圖"
        }

    def _setAction(self):
        self.actions = {
            0: self.start,
            1: self._setNextToApkInstallStory,
            2: self._setNextToStartAPPStory,
            3: self._setNextToRemoveAPPStory,
            4: self._setNextToRemoveSdCardFileStory,
            5: self._setNextToOnlyCMDStory,
            6: self._setNextToScreenShotStory,
        }

    def _setNextToApkInstallStory(self):
        self.nextStory = ApkInstallStory(previous=self, deviceIdx=self.deviceIdx)

    def _setNextToStartAPPStory(self):
        self.nextStory = StartAppStory(previous=self, deviceIdx=self.deviceIdx)

    def _setNextToRemoveAPPStory(self):
        self.nextStory = RemoveAppStory(previous=self, deviceIdx=self.deviceIdx)

    def _setNextToRemoveSdCardFileStory(self):
        self.nextStory = RemoveSdCardFileStory(previous=self, deviceIdx=self.deviceIdx)

    def _setNextToOnlyCMDStory(self):
        self.nextStory = OnlyCMDStory(previous=self, deviceIdx=self.deviceIdx)

    def _setNextToScreenShotStory(self):
        self.nextStory = ScreenShot(previous=self, deviceIdx=self.deviceIdx)

    def _startInput(self):
        """主選單 Exit => 離開"""
        super()._startInput(onFailed=self._onFailed)

    def _resultFormatter(self, result: str):
        """攔截輸入"""
        if "e" in result or "E" in result:
            print("Say Good Bye")
            os._exit(0)
        return super()._resultFormatter(result)

    def start(self):
        self.worker.setTargetIP()
        self.worker.startAdbConnect(deviceIdx=0, logger=self._logger.logger, onFailed=self._onFailed)
        super()._listPackage()
        self._setCondition()
        self._setAction()
        self._startInput()

    def _setGoBack(self):
       """self.nextStory = None 將重新開始流程"""
       self.nextStory = None

    def getNextStory(self):
        return self.nextStory
