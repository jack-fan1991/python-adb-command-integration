import sys, os


def initDir(filename: str):
    if '/' in filename:
        filename = filename.replace('/', '\\')
    dir = filename.split('\\')[:-1]
    path = ''.join([str(fold) + '\\' for fold in dir])
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print(exc_type, exc_value, exc_traceback)


def walkFile(dirPath: str, logger=None) -> dict:
    def log(info):
        print(info)
        if logger is not None:
            logger(info)
    apksDict = {}
    idx: int = 0
    if os.path.isdir(dirPath) is not True:
        return apksDict
    log(f"apk資料夾{dirPath}")
    for dirPath, dirNames, fileNames in os.walk(dirPath):
        for f in fileNames:
            idx += 1
            if ".apk" in f:
                log(f"可安裝apk : {f}")
                apksDict[idx] = os.path.join(dirPath, f)
            # print(os.path.join(dirPath, f))
    return apksDict