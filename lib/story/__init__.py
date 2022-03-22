from .stroyManger import StroyManger
from lib.story.base import BaseStory
from lib.utils.logger import MyLogger
_logger = MyLogger(__name__)
_logger.logger.debug("storyInit")
myStory = StroyManger()


def setFirstStroy(story: BaseStory):
    myStory.setfirstStroy(story)

def start():
    myStory.startStory()