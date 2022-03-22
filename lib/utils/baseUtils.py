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

import __main__


class BaseUtils:

    @staticmethod
    def getClassName(cls):
        """取得類名稱"""
        return str(cls.__class__)

    @staticmethod
    def getField(ant):
        """
        查詢物件的全部屬性
        dir() 函數不帶參數時，當前範圍內的可用變數
        dir([object])
        """
        return dir(any)

    @staticmethod
    def isDictEmpty(dict: dict) -> bool:
        return bool(dict) is False

    @staticmethod
    def getObjInfo(any: any, dtl=False) -> str:
        """"""
        info = ""
        if any is None:
            return "object is None"
        if BaseUtils.isFunction(any):
            info += f"| {any.__module__}"
            if "__name__" in (dir(any)) or "__qualname__" in (dir(any)):
                if "__name__" in (dir(any)):
                    info += f".{any.__name__}() |"
                else:
                    info = f". {any.__qualname__}() |"
            else:
                if "__func__" in (dir(any)):
                    info += f".{any.__func__.__name__}() |"
            # elif "__qualname__" in (dir(any)):
            #     info = f"| {any.__qualname__}() |"
        else:
            if "__class__" in (dir(any)):
                info = f"| {any.__class__} |"
            if "__qualname__" in (dir(any)):
                info += f"{any.__qualname__} | "
        if dtl is True:
            return info + f"| >>>> [ DTL ] SIZE {any.__sizeof__()} bytes - ID : {id(any)} - module: {any.__module__} |"
        else:
            return info

    @staticmethod
    def isFunction(any) -> bool:
        return callable(any)

    @staticmethod
    def getMainPyFileName():
        return __main__.__file__.split('\\')[-1].split('.')[0]

    @staticmethod
    def getMainPyFilePath():
        return __main__.__file__
    # @classmethod
    # def isEmpty(any: any) -> bool:
    #     if any is dict
    #         return bool(dict)
