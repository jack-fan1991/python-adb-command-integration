"""
 在import app 時做 logging 初始化
 import 順序很重要

"""
import logging
from logging import handlers
import os
import json
from lib.core.enum import Mode
from datetime import datetime
from lib.utils import baseUtils
import pprint

from lib.utils.fileUtils import initDir
import sys
print("啟動中,請耐心等候.....", flush=True)
# global參數
APPMODE = Mode.DEBUG
LOGGER_LEVEL = logging.DEBUG
LOGGER_FILE_PATH = './logs/default'
LOGGER_EZPRINT = False
LOGGER_COLOR_PRINT = True
APK_FILE_PATH = './apk'
CMD_TIMEOUT = 9999999

LOG_FORMAT = '%(asctime)s | %(levelname)s | %(name)s | (%(filename)s:%(lineno)d) | %(message)s '
EZ_FORMAT = '%(message)s '
MAIN_FILE = baseUtils.BaseUtils.getMainPyFileName()

class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;20"
    blue = "\x1b[;34;20m"
    yellow = "\x1b[33;20m"
    green = "\x1b[;32;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    # format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: blue + LOG_FORMAT + reset,
        logging.INFO: green + LOG_FORMAT + reset,
        logging.WARNING: yellow + LOG_FORMAT + reset,
        logging.ERROR: bold_red + LOG_FORMAT + reset,
        logging.CRITICAL: bold_red + LOG_FORMAT + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

# 禁用預設
# 初使化logging設定
def update():
    global LOGGER_COLOR_PRINT
    if APPMODE is Mode.DEBUG:
        LOGGER_COLOR_PRINT = True
    else:
        LOGGER_COLOR_PRINT = False


def loadLogSetting(mainFileName: str, lonSettingFilepath='.\\logConfig.json'):
    global LOGGER_LEVEL
    global APPMODE
    global LOGGER_FILE_PATH
    global CMD_TIMEOUT
    # 檢查路徑打包exe會有問題
    print(f"check : {lonSettingFilepath} setting")
    if os.path.exists(lonSettingFilepath) is not True:
        absPath = baseUtils.BaseUtils.getMainPyFilePath().split("\\")[0:-1]
        absPath.append(lonSettingFilepath.split("\\")[-1])
        absPath = "\\".join(absPath)
        if os.path.exists(absPath) is not True:
            print(f"absPath : {absPath} not exist")
        else:
            print(f"absPath : {absPath} load success")
            lonSettingFilepath = absPath
    else:
        print(f"absPath : {lonSettingFilepath} load success")

    def setLogLevel(settingLevel: str):
        if "info" in settingLevel or "i" in settingLevel or "I" in settingLevel:
            return logging.INFO
        elif "warning" in settingLevel or "w" in settingLevel or "W" in settingLevel:
            return logging.WARNING
        elif "error" in settingLevel or "e" in settingLevel or "E" in settingLevel:
            return logging.ERROR
        else:
            return logging.DEBUG
    # encrypt = getEncrypt(encryptName)
    # sender = None
    # mailAccount = None
    # passward = None
    # mailSetting = {}
    try:
        with open(lonSettingFilepath, 'r') as read_file:
            config = json.load(read_file)
            if config.get(mainFileName) is not None:
                exeInfo = config[mainFileName]
                if exeInfo.get('LogLevel') is not None:
                    LOGGER_LEVEL = setLogLevel(exeInfo.get('LogLevel'))
                    logging.getLogger().setLevel(LOGGER_LEVEL)
                if exeInfo.get('Mode') is not None:
                    mode = exeInfo.get('Mode')
                    APPMODE = Mode.isDebug(mode)
                    update()
                if exeInfo.get('FileName') is not None:
                    fileName = exeInfo.get('FileName')
                    LOGGER_FILE_PATH = f'./logs/{fileName}'
                if exeInfo.get('ApkFilePath') is not None:
                    apkFileName = exeInfo.get('ApkFilePath')
                    APK_FILE_PATH = f'{apkFileName}'
                if exeInfo.get('CMDtimeoutSec') is not None and  exeInfo.get('CMDtimeoutSec') is not "":
                    timeOut = exeInfo.get('CMDtimeoutSec')
                    try:
                        timeOut = int(exeInfo.get('CMDtimeoutSec'))
                        CMD_TIMEOUT = timeOut
                    except Exception as e:
                        print(f"CMDtimeoutSec : {timeOut} 不符合格式")  
            else:
                print(f"{lonSettingFilepath}找不到{mainFileName}設定黨")

        #     if config.get('mailer'):
        #         if config['mailer'].get('sender')!=None:
        #             sender =  config['mailer']['sender']
        #             if sender.get('MailAccount')!=None:
        #                 mailSetting['MailAccount'] = sender.get('MailAccount')
        #             if sender.get('cipherPassward')!=None:
        #                 mailSetting.update( encrypt.AES_decrypt(sender.get('cipherPassward')) )
        # if mailSetting['MailAccount']  ==None  or mailSetting['Passward']  ==None:
        #     e=''
        #     if len(mailSetting)>0:
        #         e=mailSetting['Msg']
        #     raise Exception("mailAccount Passward cant be None , %s ,%s"%( mailAccount , passward) , e)
        # return  mailSetting, configLevel
    except Exception as e:
        print(e)


loadLogSetting(MAIN_FILE)

_infoObj = [APPMODE, LOGGER_LEVEL, LOGGER_FILE_PATH, LOGGER_EZPRINT, LOGGER_COLOR_PRINT, APK_FILE_PATH, CMD_TIMEOUT]
_infoObjNeme = ["MODE", "LOGGER_LEVEL", "LOGGER_FILE_PATH", "LOGGER_EZPRINT", "LOGGER_COLOR_PRINT", "APK_FILE_PATH", "CMD_TIMEOUT"]

def getInfo():
    map = {}
    for i in range(len(_infoObj)):
        map[_infoObjNeme[i]] = _infoObj[i]
    return map

print("loadDone")
# 初始化logger
# 設定顯示等級
logging.basicConfig(level=LOGGER_LEVEL)
LOGGER_FILE_PATH += "_{date:%Y%m%d}.log".format(date=datetime.now())
logging.basicConfig(level=LOGGER_LEVEL)
logger = logging.getLogger()
initDir(LOGGER_FILE_PATH)
writer = handlers.TimedRotatingFileHandler(filename=LOGGER_FILE_PATH, when='d', backupCount=3, encoding='utf-8')
# 設定檔案裡寫入的格式
# 螢幕上輸出
colorConsole = logging.StreamHandler()
# colorConsole.setFormatter(logging.Formatter(LOG_FORMAT))
colorConsole.setFormatter(CustomFormatter())
# ezConsole = logging.StreamHandler()
# ezConsole.setFormatter(CustomFormatter(EZ_FORMAT))
writer.setFormatter(logging.Formatter(LOG_FORMAT))

logger.handlers.clear()
logger.addHandler(writer)
if APPMODE is Mode.DEBUG:
    logger.addHandler(colorConsole)
logger.info(pprint.pformat(getInfo()))
pprint.pprint(getInfo())
logger.propagate = False
