import traceback
class StackTraceUtil:
    @staticmethod
    def getCallStack(targetDeep: int):
        """@ param :targetDeep 向上追查調用者深度 """
        current = targetDeep + 1
        stack = traceback.extract_stack()
        return stack[-current]
    
    @staticmethod
    def getCallStackForLog(targetDeep: int):
        """@ param :targetDeep 向上追查調用者深度 """
        current = targetDeep + 1
        stack = traceback.extract_stack()[-current]
        fileName = stack.filename.split("\\")[-1]
        return fileName + ":" + stack.line + " " + str(stack.lineno)