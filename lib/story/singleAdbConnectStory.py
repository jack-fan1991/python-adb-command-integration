# from lib.model.device import Device
# from lib.story.mainStory import MainStory
# from lib.story.base.baseEzIPStory import BaseEzIPStory
# from lib.utils.adbCmdUtils import AdbCmdUtils

# """adb connect"""


# class SingleAdbConnectStory(BaseEzIPStory):
#     def __init__(self, previous=None) -> None:
#         super().__init__(previous=previous)

#     # def _onFailed(self, *args, **kargs):
#     #     """處理失敗"""
#     #     errorInfo = self._onFailed.__doc__
#     #     errorInfo = self._onFailedParser(errorInfo, *args, **kargs)
#     #     failedInfo = self._onFailedinfoParser(*args, **kargs)
#     #     self._printErr(errorInfo)
#     #     self._logger.logger.error(failedInfo + " => " + errorInfo)
#     #     self.start()

#     # @Override
#     def _startInput(self, onFailed=None):
#         """開始連線"""
#         device: Device = self.worker.deviceMap.get(0)
#         if device is None:
#             info = f"{len(self.worker.deviceMap)} 數量異常"
#             self._logger.logger.warning(info)
#             raise Exception(info)
#         result = self.worker.adbConnect(device.ip, onFailed=self._onFailed)
#         if AdbCmdUtils.onAdbConnectSuccessFilter(result=result):
#             print("連接成功")
#             self._logger.logger.info("連接成功")
#             self.nextStory = MainStory(previous=self)
#         else:
#             print("連接失敗")
#             self._logger.logger.error("連接失敗")
#             self.nextStory = self.previousStory
#         return

#     def getNextStory(self):
#         return self.nextStory
