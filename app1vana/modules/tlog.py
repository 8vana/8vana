import re
import pyxel
from datetime import datetime

# color http://tkitao.hatenablog.com/entry/2017/01/26/193908
BLACK = 0
DARK_BLUE = 1
DARK_PURPLE = 2
DARK_GREEN = 3
BROWN = 4
DARK_GRAY = 5
LIGHT_GRAY = 6
WHITE = 7
RED = 8
ORANGE = 9
YELLOW = 10
GREEN = 11
BLUE = 12
INDIGO = 13
PINK = 14
PEACH = 15

# ログウィンドウ向けセッティング（各種表示位置を設定）
LOG_AREA_X       = 52
LOG_AREA_Y       = 184

CHAR_WIDTH    = 5
CHAR_HEIGHT   = 7

class Targetlog:
    def __init__(
            self,
            log_area_x = LOG_AREA_X, log_area_y = LOG_AREA_Y,
            char_width = CHAR_WIDTH, char_height = CHAR_HEIGHT
        ):
        self.x = log_area_x
        self.y = log_area_y
        self.char_w = char_width
        self.char_h = char_height


    def time(self, target1, target2, color=WHITE, count=0):
        # draw strings on log area
        dt1    = datetime.fromtimestamp(target1["time"])
        time1  = "{0:%Y-%m-%d %H:%M:%S}".format(dt1)
        time2  = ""
        offset = self.char_h

        if(type(target2) is dict and target1 != target2):
            #print(target2)
            dt2   = datetime.fromtimestamp(target2["time"])
            time2 = " -> {0:%Y-%m-%d %H:%M:%S}".format(dt2)

        time = time1 + time2
        pyxel.text(
            self.x,
            self.y + (offset * count),
            time,
            color)  # x, y, string, color
        return (count + 1)


    def next(self, color=WHITE, count=0):
        # draw click to next sign on log area
        offset = self.char_h
        pyxel.text(
            self.x,
            self.y + (offset * count),
            "**** click to next page ****",
            color)  # x, y, string, color
        return (count + 1)


    def log(self, target, note="", color=GREEN, count=0):
        # draw strings on log area
        offset = self.char_h
        log = ""
        if(type(target) is dict):
            #dt   = datetime.fromtimestamp(target["time"])
            #time = "{0:%Y-%m-%d %H:%M:%S}".format(dt)
            #time = "{0:%H:%M:%S}".format(dt)
            #log  = "{}:{}:{}: {} > {} {}".format(time, target["phase"], target["attack"], target["from"], target["to"], note)
            log  = "{}: {} > {} {}".format(target["attack"], target["from"], target["to"], note)
        elif(type(target) is str):
            log = target

        pyxel.text(
            self.x,
            self.y + (offset * count),
            log,
            color)  # x, y, string, color
        return (count + 1)

