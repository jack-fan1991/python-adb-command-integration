from lib.decorator.exceptionHandler import Exception_handler
from lib.core.baseObj import BaseObj
from lib.story.base.abstracStory import AbstracStory
from lib.utils.baseUtils import BaseUtils
from lib.utils.cmdUtils import Cmd


class BaseStory(AbstracStory, BaseObj):
    """只要story.getNextStory() is None 就會重新開始"""
    def __init__(self, previous=None) -> None:
        super().__init__()
        self.conditions: dict[any] = {}
        self.actions: dict[any] = {}
        self.previousStory: BaseStory = previous
        self.nextStory: BaseStory = None
        self.targetPath = ""

    def _onFailed(self, *args, **kargs):
        """處理失敗"""
        errorInfo = self._onFailed.__doc__
        errorInfo = self._onFailedParser(errorInfo, *args, **kargs)
        failedInfo = self._onFailedinfoParser(*args, **kargs)
        self._printErr(errorInfo)
        self._logger.logger.error(failedInfo + " => " + errorInfo)
        if type(kargs.get('error')) is Cmd.CmdTimeOutError:
            self._setGoBack()
        else:
            self.start()

    def _onFailedParser(self, errorInfo, *args, **kargs) -> str:
        """onFailed回調訊息處理"""
        if kargs.get('error', None) is not None:
            error = kargs.get('error')
            if type(error) is ValueError:
                errorInfo += ",格式不符"
            if type(error) is Cmd.CmdTimeOutError:
                errorInfo += f",{str(error)}"
        return errorInfo

    def _onFailedinfoParser(self, *args, **kargs) -> str:
        """onFailed回調訊息處理"""
        info: str = ""
        if kargs.get('failedInfo', None) is not None:
            info = f"{kargs.get('failedInfo')}"
        return info

    def getNextStory(self):
        return self.nextStory

    def hasNextStory(self):
        return self.getNextStory() is not None

    def _onSuperFailedCall(self, *args, **kargs):
        "子類未提供錯誤處理 onFailed方法"
        info = f'{self._onSuperFailedCall.__doc__}'
        self._logger.logger.warning(info)
        if kargs.get('error', None) is not None:
            self._logger.logger.error(BaseUtils.getObjInfo(self)+f"Base setp1 Exception => {kargs.get('error', None)}")
            raise kargs.get('error', None)
        pass

    def _isResultInConditions(self, result) -> bool:
        self._conditionsVerification()
        return result in self.conditions

    def _isResultInAcions(self, result) -> bool:
        self._actionVerification()
        return result in self.actions

    def _conditionsVerification(self):
        """self.conditions 條件不能為空"""
        if BaseUtils.isDictEmpty(self.conditions):
            error = f"{self._conditionsVerification.__doc__}"
            self._logger.logger.error(error)
            raise Exception(f"{self._conditionsVerification.__doc__}")

    def _actionVerification(self):
        """self.actions 動作不能為空"""
        if BaseUtils.isDictEmpty(self.actions):
            error = f"{self._actionVerification.__doc__}"
            self._logger.logger.error(error)
            raise Exception(f"{self._actionVerification.__doc__}")

    def _getTitle(self) -> str:
        condition: str = ""
        for value in self.conditions.values():
            condition = condition + value+"\n"
        condition += ">>>>"
        return condition

    def _getConditon(self, key: any):
        return self.conditions.get(key, None)

    def _getAction(self, key: any):
        return self.actions.get(key, None)

    def _resultFormatter(self, result: str):
        """定義轉換類型"""
        return int(result)

    @Exception_handler(onFailed=_onSuperFailedCall)
    # 若調用super().setp1() onFailed 以參數傳入否則將回調onSuperFailedCall
    def _startInput(self, onFailed=None) -> None:
        # 回傳選擇結果
        """執行第一步"""
        title: str = f"\n\n==========={self._startInput.__doc__}===========\n{self._getTitle()}"
        self._logger.logger.info(title)
        result = input(f"{title}")
        result = self._resultFormatter(result)
        if self._isResultInConditions(result) is not True:
            error = f"輸入結果: {result} , 輸入錯誤"
            self._printErr(error)
            self._logger.logger.error(error)
            self.start()
            return

        fun = self._getAction(result)

        if(fun is None):
            error = f"查無action key : {result} 行為請通知開發者"
            self._printErr(error)
            self._logger.logger.error(error)
            self.start()
            return
        print(f"輸入結果: {self._getConditon(result)}")
        self._logger.logger.info(f"輸入結果: {result} ,condition=>{self._getConditon(result)} action=> {fun.__name__}")
        self._onActionSelect(result)
        if BaseUtils.isFunction(fun) is not True:
            raise Exception(f"[Exception] {BaseUtils.getObjInfo(self)}  self.action value 只能放 function")
        self._logger.logger.debug(f"run action func =>{BaseUtils.getObjInfo(fun)}")
        fun()
        return None
        # except Exception as e:
        #     self._logger.logger.error(BaseUtils.getObjInfo(self)+"Base setp1 Exception => " + e)

    def _onActionSelect(self, result) -> None:
        """action 選擇的設定"""
        pass

    def start(self):
        self._setup()
        self._startInput()

    def _setup(self):
        self._setCondition()
        self._setAction()
        self._conditionsVerification()
        self._actionVerification()

    def _printErr(self, err):
        print("!!"*5+err+"!!"*5)

    def _resetToOnlyBackCondition(self, conditions=None):
        """重置回帶有返回事件的設定"""
        self.conditions = {0: " 0 => 返回"}
        if(BaseUtils.isDictEmpty(conditions)):
            return
        self.conditions.update(conditions)

    def _resetToOnlyBackAction(self, actions=None):
        """重置回帶有返回事件的設定"""
        self.actions = {0: self._setGoBack}
        if(BaseUtils.isDictEmpty(actions)):
            return
        self.actions.update(actions)

    def _setGoBack(self):
        self.nextStory = self.previousStory