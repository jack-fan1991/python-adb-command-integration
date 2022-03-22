"""紀錄基礎用法
   1. __name__ 属性
    >>> 模塊是被引用時,值是模塊名, python文件被直接運行, 值是'__main__'

   2.__file__ 属性
    模塊絕對路徑
    >>> os.__file__
    >>> '/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/os.pyc'

    3.__doc__ 属性
    模塊的註釋文檔可對類或方法使用
    >>> myClass.__doc__
    >>> myClass.funcA.__doc__

    4.__package__ 属性
    package name

    5.sys.modules -> dict
    取得所有引入的module
    !!!print自動排版
    import pprint
    pprint.pprint(sys.modules)

"""

from lib.utils.baseUtils import BaseUtils
from lib.utils.logger import MyLogger

class BaseObj:
    def __init__(self) -> None:
        self._logger = MyLogger(BaseUtils.getClassName(self))

    def getClassName(self):
        """取得類名稱"""
        return str(self.__class__)

    def getField(self):
        """
        查詢物件的全部屬性
        dir() 函數不帶參數時，當前範圍內的可用變數
        dir([object])
        """
        return dir(self)
