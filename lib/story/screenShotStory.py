from lib.story.base.baseIPStory import BaseIPStory


class ScreenShot(BaseIPStory):

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
        conditions = {
            1: " 1 => 截圖",
            2: " 2 => 拉取檔案",
            3: " 3 => 清除裝置內暫存照片",
        }
        self.conditions.update(conditions)

    def _setAction(self):
        super()._resetToOnlyBackAction()
        actions = {
            1: self.screenShot,
            2: self.pullPNG,
            3: self.cleanPNG,
        }
        self.actions.update(actions)

    def screenShot(self):
        self.worker.screenShot(ip=self.targetDevice.ip, onFailed=self.onFailed)
        # info = f"==========={self.targetPath}已啟動==========="
        # print(info)
        # self._logger.logger.info(info)

    def pullPNG(self):
        self.worker.pullPNG(ip=self.targetDevice.ip, onFailed=self.onFailed)
        # info = f"==========={self.targetPath}已啟動==========="
        # print(info)
        # self._logger.logger.info(info)
    
    def cleanPNG(self):
        self.worker.cleanPNG(ip=self.targetDevice.ip, onFailed=self.onFailed)

    def doActionSelect(self, result) -> None:
        return super()._doActionSelect(result)

    def _startInput(self):
        """螢幕截圖"""
        super()._startInput(onFailed=self.onFailed)

    def start(self):
        self._setCondition()
        self._setAction()
        self._startInput()
        self.nextStory = self

    def getNextStory(self):
        return self.nextStory
