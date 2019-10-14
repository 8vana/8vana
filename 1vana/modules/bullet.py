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

# 時刻表示セッティング（表示位置を設定）
TIME_AREA_X          = 120
TIME_AREA_Y          = 245

class Bullet:
    def __init__(
            self, time_area_x = TIME_AREA_X, time_area_y = TIME_AREA_Y
        ):
        self.x = time_area_x
        self.y = time_area_y



    def time(self, time, color=WHITE):
        # draw time
        epoch = "{:.1f}".format(time)
        dt    = datetime.fromtimestamp(int(time))
        date  = "{0:%Y-%m-%d %H:%M:%S}".format(dt)
        time  = "{} {}".format(date, epoch)
        pyxel.text(
            self.x,
            self.y,
            time,
            color)  # x, y, string, color
        return True



    def draw(self, bullets, icon):
        xy = icon["world"].get_center_position()
        x  = xy[0]
        y  = xy[1]
        for bullet in bullets:
            pyxel.line(x, y, bullet["state"].x2, bullet["state"].y2, bullet["line_color"])
            bullet["icon"].pmove_abs(bullet["state"].x - (bullet["icon"].width / 2), bullet["state"].y - (bullet["icon"].height / 2))
            if(bullet["line_color"] == RED):
                icon["mono"].pmove_abs(bullet["state"].x2, (bullet["state"].y2 - 6))
                icon["fire"].pmove_abs(bullet["state"].x2, bullet["state"].y2)
        return True

