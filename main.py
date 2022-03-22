"""在app.__init__.py APP初始設定"""
import app
from lib.story import setFirstStroy, start
from lib.story.autoIpSettingStory import AutoIpSettingStory
# from lib.story.mIpSettingStory import ManualIPSettingStory
from lib.story.mainStory import MainStory

if __name__ == '__main__':
   setFirstStroy(MainStory())
   start()