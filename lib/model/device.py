
class Device:
    def __init__(self, ip) -> None:
        self.ip: str = ip
        self.apkList = []

    def isApkListEmpty(self):
        return len(self.apkList) == 0

    def isApkExist(self, installApkName: str):
        if self.isApkListEmpty() or installApkName not in self.apkList:
            return False
        return True


if __name__ == '__main__':
    d1 = Device("123")
    # d1.isConnected = True
    m = {"123": d1}
    print(m.get(1))
