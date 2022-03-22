# from lib.story.base.baseIPStory import BaseIPStory
# from lib.story.singleAdbConnectStory import SingleAdbConnectStory


# class ManualIPSettingStory(BaseIPStory):
#     """單一IP手動輸入流程"""

#     def __init__(self, previous=None, deviceIdx=0) -> None:
#         super().__init__(previous=previous, deviceIdx=deviceIdx)

#     def _setCondition(self):
#         self.conditions = {
#             1: "  1 => 查詢當前連線IP",
#             2: "  2 => 設定連接目標IP"
#             }

#     def _setAction(self):
#         self.actions = {
#             1: BaseIPStory.worker.getConnectIp,
#             2: BaseIPStory.worker.setTargetIP
#             }

#     def _onFailed(self, *args, **kargs):
#         """處理失敗"""
#         errorInfo = self._onFailed.__doc__
#         errorInfo = self._onFailedParser(errorInfo, *args, **kargs)
#         failedInfo = self._onFailedinfoParser(*args, **kargs)
#         self._printErr(errorInfo)
#         self._logger.logger.error(failedInfo + " => " + errorInfo)
#         self.start()

#     def _onActionSelect(self, result) -> None:
#         if result == 1:
#             self.nextStory = self
#         else:
#             self.nextStory = SingleAdbConnectStory(previous=self)
#         return super()._onActionSelect(result)

#     # @Override
#     def _startInput(self):
#         """設定連線目標IP"""
#         super()._startInput(onFailed=self._onFailed)

#     def start(self):
#         super().start()
   
#     def getNextStory(self):
#         return self.nextStory
