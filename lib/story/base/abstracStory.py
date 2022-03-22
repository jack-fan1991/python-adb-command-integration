from abc import ABC, abstractmethod


class AbstracStory(ABC):

    @abstractmethod
    def _setCondition(self):
        """設定條件
        sample:
           conditions = {
            1: "1 => 自動搜尋IP",
            2: "2 => 手動設定IP"
        }
        """
        return "AbstracStoryabstractmethod"
        pass

    @abstractmethod
    def _setAction(self):
        """設定動作
        sample:
            acions = {
                1: action1-> function ,
                2: action2-> function
            }
        """
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def getNextStory(self):
        pass
