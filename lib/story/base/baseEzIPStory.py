from lib.story.base.baseIPStory import BaseIPStory
from lib.utils.baseUtils import BaseUtils


class BaseEzIPStory(BaseIPStory):
    """實作抽象方法的父類"""
    def __init__(self, previous=None, deviceIdx=0) -> None:
        super().__init__(previous=previous, deviceIdx=deviceIdx)
        self._logger.logger.debug(f"{BaseUtils.getObjInfo(self)} is BaseNoInputConditionStory")
    
    def _setCondition(self):
        pass

    def _setAction(self):
        pass

    def _setup(self):
        pass
