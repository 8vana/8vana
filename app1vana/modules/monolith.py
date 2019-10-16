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


# モノリス向けセッティング（各種表示位置を設定）
MONOLITH_X1               = 48
MONOLITH_Y1               = 92
MONOLITH_X2               = 204
MONOLITH_Y2               = 224
MONOLITH_MARGIN_LEFT      = 4
MONOLITH_MARGIN_TOP       = 4
MONOLITH_TITLE_LENGTH     = 6

# モノリスのサイズを画面サイズの割合で指定します
MONOLITH_WIDTH  = 0.6
MONOLITH_HEIGHT = 0.8

# モノリス向けセッティング（ログのページ移動量を設定）
## <- をクリックしたときの移動量
MONOLITH_PREVIOUS_AMOUNT1 = 10
## << をクリックしたときの移動量
MONOLITH_PREVIOUS_AMOUNT2 = 100
## -> をクリックしたときの移動量
MONOLITH_NEXT_AMOUNT1     = 10
## >> をクリックしたときの移動量
MONOLITH_NEXT_AMOUNT2     = 100

# 時刻表示セッティング（表示位置を設定）
TIME_AREA_X          = 120
TIME_AREA_Y          = 245

CHAR_WIDTH    = 5
CHAR_HEIGHT   = 7

class Monolith:
    def __init__(
            self,
            mono_x1 = MONOLITH_X1, mono_y1 = MONOLITH_Y1,
            mono_x2 = MONOLITH_X2, mono_y2 = MONOLITH_Y2,
            margin_left = MONOLITH_MARGIN_LEFT, margin_top = MONOLITH_MARGIN_TOP,
            title_len = MONOLITH_TITLE_LENGTH,
            previous_amount1 = MONOLITH_PREVIOUS_AMOUNT1, previous_amount2 = MONOLITH_PREVIOUS_AMOUNT2,
            next_amount1 = MONOLITH_NEXT_AMOUNT1, next_amount2 = MONOLITH_NEXT_AMOUNT2,
            time_x = TIME_AREA_X, time_y = TIME_AREA_Y,
            char_width = CHAR_WIDTH, char_height = CHAR_HEIGHT
        ):
        self.x1 = mono_x1
        self.y1 = mono_y1
        self.x2 = mono_x2
        self.y2 = mono_y2
        self.mleft = margin_left
        self.mtop  = margin_top
        self.tlen  = title_len
        self.p1    = previous_amount1
        self.p2    = previous_amount2
        self.n1    = next_amount1
        self.n2    = next_amount2
        self.time_x = time_x
        self.time_y = time_y
        self.char_w = char_width
        self.char_h = char_height


    def draw_time(self, time, color=WHITE):
        # draw time
        epoch = "{:.1f}".format(time)
        dt    = datetime.fromtimestamp(int(time))
        date  = "{0:%Y-%m-%d %H:%M:%S}".format(dt)
        time  = "{} {}".format(date, epoch)
        pyxel.text(
            self.time_x,
            self.time_y,
            time,
            color)  # x, y, string, color
        return True


    def area(self, color=LIGHT_GRAY):
        pyxel.rect(self.x1, self.y1, self.x2, self.y2, color)
        return True


    def time(self, target1, target2, color=WHITE, count=0):
        # draw strings on log area
        offset = self.char_h
        dt1   = datetime.fromtimestamp(target1["time"])
        time1 = "{0:%Y-%m-%d %H:%M:%S}".format(dt1)
        time2 = ""

        if(type(target2) is dict and target1 != target2):
            #print(target2)
            dt2   = datetime.fromtimestamp(target2["time"])
            time2 = " -> {0:%Y-%m-%d %H:%M:%S}".format(dt2)

        time = time1 + time2
        pyxel.text(
            self.x1 + self.mleft,
            self.y1 + self.mtop + (offset * count),
            time,
            color)  # x, y, string, color
        return (count + 1)


    def next(self, page, page_max, color=BROWN, count=0):
        # draw click to next sign on log area
        offset_h = self.char_h
        offset_w = self.char_w
        line       = "<<    <- {0:>4}/{1:<4} ->    >>".format(page+1, page_max)
        line_width = len(line) * offset_w
        margin     = (self.x2 - self.x1 - line_width)
        pyxel.text(
            self.x1 + self.mleft + margin,
            self.y2 - self.mtop - offset_h,
            line,
            color)  # x, y, string, color
        #print("draw_monolith_log_next:margin:%d:line_width:%d" % (margin, line_width))
        return (margin, line_width)


    def log(self, log, color=DARK_GRAY, count=0, margin_left=0):
        # draw strings on monolith area
        offset = self.char_h
        pyxel.text(
            self.x1 + self.mleft + margin_left,
            self.y1 + self.mtop  + (offset * count),
            log,
            color)  # x, y, string, color
        return (count + 1)

