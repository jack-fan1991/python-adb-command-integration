
from lib.model.device import Device
from lib.story.base.baseStory import BaseStory
from lib.core.worker import Worker
from lib.utils.adbCmdUtils import AdbCmdUtils


class BaseIPStory(BaseStory):
    dropPackagePrefix = ["com.google.android", "com.google", "com.android", "package:android"]
    worker = Worker()

    def __init__(self, previous=None, deviceIdx=0) -> None:
        super().__init__(previous=previous)
        self.deviceIdx: int = deviceIdx
        self.targetDevice: Device = self.worker.deviceMap.get(deviceIdx)
        self.apkPathDict: dict = {}
        self.nextStory = None
        # self._logger.logger.debug(f">>>>> {self.getClassName()} , Worker ID =>{id(Worker)} ")
        # self._logger.logger.debug(">>>>")

    def _listPackage(self):
        """檢查當前apk"""
        if not self.worker.IPMapVerification():
            info = f"{len(self.worker.deviceMap)} 數量異常"
            self._logger.logger.warning(info)
            raise Exception(info)
        device: Device = self.worker.deviceMap.get(self.deviceIdx)
        result = self.worker.showApk(device.ip)
        result = AdbCmdUtils.listPackagefilter(
            BaseIPStory.dropPackagePrefix,
            result,
            filter=AdbCmdUtils.skipPackageFilter)
        info = "當前無APK"
        if len(result) > 0:
            info = f"當前APK => {result}"
        print(info)
        self._logger.logger.info(info)
        device.apkList = result
        return

    def _onActionSelect(self, result) -> None:
        """action 選擇的設定"""
        self.targetPath = self.apkPathDict.get(result)
        self._logger.logger.info(f"doBeforeRunAction select {self.targetPath}")
