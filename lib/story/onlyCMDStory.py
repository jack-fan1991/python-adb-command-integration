from lib.decorator.exceptionHandler import Exception_handler
from lib.story.base.baseEzIPStory import BaseEzIPStory
from lib.utils.cmdUtils import Cmd

"""只有cmd指令"""

class OnlyCMDStory(BaseEzIPStory):

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

    def _resultFormatter(self, result: str):
        return str(result)

    @Exception_handler(onFailed=_onFailed)
    def _startInput(self, onFailed=None) -> None:
        # 回傳選擇結果
        """輸入命令(不支援進入樹梅派操作): 0 =>返回"""
        title: str = f"\n\n==========={self._startInput.__doc__}===========\n{self._getTitle()}"
        self._logger.logger.info(title)
        result = input(f"{title}")
        result = self._resultFormatter(result)
        if result == "0":
            super()._setGoBack()
            return
        resp = Cmd.call(result)
        print(resp)
        self._logger.logger.info(title)
        self.start()

    def start(self):
        self._startInput()
