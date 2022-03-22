from lib.core.baseObj import BaseObj
from lib.story.base.baseStory import BaseStory
from lib.utils.baseUtils import BaseUtils
import copy


class StroyManger(BaseObj):
    """只要story.getNextStory() is None 就會重新開始"""
    def __init__(self, story: BaseStory = None) -> None:
        super().__init__()
        self.story: BaseStory = story
        self.firstStory: BaseStory = copy.copy(story)
        pass

    def setfirstStroy(self, story: BaseStory):
        self.story = story
        self.firstStory = copy.copy(story)

    # def startStory(self):
    #     iterStory = iter(self._storySet)
    #     iterStory = iter(self._storySet)
    #     for story in iterStory:
    #         self._logger.logger.info(f"{BaseUtils.getObjInfo(story)} start()")
    #         story.start()
    #         self._logger.logger.info(f"{BaseUtils.getObjInfo(story)} Done()")

    #     print("allDone")

    def startStory(self):
        if self.story is None:
            raise Exception("story cant be None")
        self.story.start()
        # if self.story.hasNextStory():
        # while (self.story.hasNextStory()):
        while (True):
            self._logger.logger.info(f"{BaseUtils.getObjInfo( self.story)} end and next()")
            self.story = self.story.getNextStory()
            if self.story is None:
                self.story = copy.copy(self.firstStory)
            self.story.start()
            self._logger.logger.info(f"next story{BaseUtils.getObjInfo( self.story)}")
        else:
            self._logger.logger.info(f"{BaseUtils.getObjInfo(self.story)} the End()")
        print("allDone")
