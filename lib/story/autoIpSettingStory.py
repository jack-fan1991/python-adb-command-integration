from lib.story.base.baseIPStory import BaseIPStory
from lib.utils import adbCmdUtils

"""自動掃描(padding)"""


class AutoIpSettingStory(BaseIPStory):

    def __init__(self) -> None:
        super().__init__()

    def _setCondition(self):
        self.conditions = {
            1: "1 => 自動搜尋IP",
            2: "2 => 手動設定IP"
            }

    def _setAction(self):
        self.actions = {
            1: BaseIPStory.worker.getConnectIpPrefix,
            2: BaseIPStory.worker.inputConnectIp
            }
        pass

    def onFailed(self, *args, **kargs):
        """處理失敗"""
        errorInfo = self.onFailed.__doc__
        errorInfo = self._onFailedParser(errorInfo, *args, **kargs)
        failedInfo = self._onFailedinfoParser(*args, **kargs)
        self._printErr(errorInfo)
        self._logger.logger.error(failedInfo + " => " + errorInfo)
        self.start()

    # @Override
    def setp1(self, onFailed=None):
        """設定IP"""
        # super()._startInput(onFailed=self.onFailed)
        BaseIPStory.worker.inputConnectIp()
        AutoIpSettingStory.worker.getIP()

    def start(self):
        BaseIPStory.worker.setTargetIP()
        AutoIpSettingStory.worker.getIP(onAdbConnectSuccessFilter=adbCmdUtils.AdbCmdUtils.onAdbConnectSuccessFilter)

    # @Override
    def setp2(self):
        AutoIpSettingStory.worker.getIP()