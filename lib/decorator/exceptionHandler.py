from functools import wraps
from lib.core.baseObj import BaseObj
from lib.utils.baseUtils import BaseUtils
# def exception_handler(function):
#     def wrapper(*args, **kwargs):
#         try:
#             function(*args, **kwargs)
#         except Exception as e:
#             print(f"{function.__name__} =>{e}")
#         return function(*args, **kwargs)
#     return wrapper


class Exception_handler(BaseObj):
    """
    如果沒有設定回調則繼續向外拋出錯誤
    使用此裝飾器裝飾的方法可於方法中傳入onFailed方法
    於方法參數傳入的callback 優先權為最高
    @ param onFailed :失敗回調,請參照下列格式否則報錯
     => def onFailed(*args, **kargs):
            print(11111111111111)
    """
    def __init__(self, throwException: bool = False, onFailed=None):
        # _logger.debug('[__init__]')
        super().__init__()
        self.throwException = throwException
        self.onFailed = onFailed

    def _checkCallBack(self, func, stackInfo: str):
        try:
            if(self.onFailed is not None):
                self._logger._debug(f' {stackInfo} has callback => {BaseUtils.getObjInfo(self.onFailed)}')
        except Exception as e:
            self._logger.logger.error(e)

    def getCallBackInKargs(self, func, stackInfo: str, **kargs):
        try:
            """以方法參數代的callback為優先,若沒有則調用裝飾器的callback"""
            self.onFailed = kargs.get("onFailed", self.onFailed)
            if kargs.get("onFailed") is not None:
                self._logger._debug(f' {stackInfo} set onFailed callback as => {BaseUtils.getObjInfo(self.onFailed)}')
        except Exception as e:
            self._logger.logger.error(e)

    def __call__(self, func):
        # stackInfo = StackTraceUtil.getCallStackForLog(targetDeep=2)
        stackInfo = BaseUtils.getObjInfo(func)
        # 確認當前方法是否有回調
        self._checkCallBack(func, stackInfo)

        # 確保 exception_handlerWrap.__name__為傳入的func.__name__
        @wraps(func)
        def exception_handlerWrap(*args, **kargs):
            try:
                # 攔截當前方法是否帶有回調
                self.getCallBackInKargs(func, stackInfo, **kargs)
                return func(*args, **kargs)
            except Exception as e:
                if self.onFailed is not None:
                    self._logger._warning(f' {stackInfo} Exception {e}')
                    self._logger._warning(f' {stackInfo}  onFailed call {BaseUtils.getObjInfo(self.onFailed)} with func Param args :{args} , kargs : {kargs}')
                    if self.throwException is True:
                        raise e
                    self.onFailed(*args, **kargs, failedInfo=stackInfo, error=e)

                else:
                    self._logger._error(f' {stackInfo}  {e}')
                    if self.throwException is True:
                        raise e 
        return exception_handlerWrap
