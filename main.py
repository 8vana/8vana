#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pyxel
import os
import argparse
import json
from app1vana.modules.actor import Actor
from app1vana.modules.fonts import Fonts

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

# CHAR_WIDTH    = 5 # pyxel.text
# CHAR_HEIGHT   = 7 # pyxel.text

CHAR_WIDTH = 8
CHAR_HEIGHT = 17

parser = argparse.ArgumentParser(description='1vana')
parser.add_argument('-l','--log_time',
    help='このオプションは、ログ再生機能で利用することを想定されており、ログファイル先頭のリソース（最も古いログ）から時刻を取得し、開始時刻の基準値として利用します。このオプションを利用しない場合は、現在時刻が開始時刻として利用されます。',
    action="store_true")
args = parser.parse_args()


class App:
    number_of_mode = 2

    def __init__(self):
        pyxel.init(255, 255, caption="Welcome to 8vana")
        self.dir = os.path.dirname(os.path.abspath("__file__")) + "/"

        self.icon = {}
        self.icon["title"] = Actor(16, 16)
        self.icon["title"].set_size(224, 71)
        self.icon["title"].imageload(self.dir + "common/assets/8vana_logo_224_16_edit.png", DARK_GREEN) # dark_green

        self.count = 0
        self.selected_app = 0

        # draw mouse cursor
        pyxel.mouse(True)

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            self.selected_app = 99
            pyxel.quit()
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            self.selected_app = 99
            pyxel.quit()
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.count += 1
            self.selected_app = self.count % App.number_of_mode
        if pyxel.btnp(pyxel.KEY_ENTER):
            pyxel.quit()

    def draw(self):
        pyxel.cls(0)

        self.icon["title"].put()
        pyxel.text(88, 60, "The visualization tool of", 0)
        pyxel.text(88, 68, "security incidents like retro games.", 0)

        pyxel.text(84, 132, "Push SPACE: Select mode", 7)
        pyxel.text(84, 140, "Push ENTER: Start 8vana", 7)
        if self.selected_app == 0:
            pyxel.text(128, 152, "> 1vana", 7)
            pyxel.text(128, 160, "  2vana", 7)
        elif self.selected_app == 1:
            pyxel.text(128, 152, "  1vana", 7)
            pyxel.text(128, 160, "> 2vana", 7)


class App2:
    contents = '''[
    {
        "titlej" : "title", 
        "title"  : "8vana staff",
        "name"   : ""
    },
    {
        "titlej" : "監督", 
        "title"  : "director",
        "name"   : "@bbr_bbq"
    },
    {
        "titlej" : "プログラマー", 
        "title"  : "programmer",
        "name"   : "@bbr_bbq, @mahoyaya"
    },
    {
        "titlej" : "音楽1", 
        "title"  : "sound design",
        "name"   : "Wanted"
    },
    {
        "titlej" : "キャラクターデザイン", 
        "title"  : "character design",
        "name"   : "@yoneyoneyo"
    },
    {
        "titlej" : "協力", 
        "title"  : "special thanks",
        "name"   : "PixelGaro, PixelMplus"
    },
    {
        "titlej" : "制作", 
        "title"  : "producer",
        "name"   : "@mahoyaya"
    },
    {
        "titlej" : "制作", 
        "title"  : "exective producer",
        "name"   : "Isao Takaesu"
    },
    {
        "titlej" : "提供", 
        "title"  : "presented by...",
        "name"   : "https://github.com/8vana/8vana"
    },
    {
        "titlej" : "", 
        "title"  : "",
        "name"   : ""
    },
    {
        "titlej" : "", 
        "title"  : "",
        "name"   : ""
    },
    {
        "titlej" : "", 
        "title"  : "",
        "name"   : ""
    }
]'''

    def __init__(self):
        pyxel.init(255, 255, caption="Ending")
        self.dir = os.path.dirname(os.path.abspath("__file__")) + "/"

        self.icon = {}
        self.icon["title"] = Actor(16, 16)
        self.icon["title"].set_size(224, 71)
        self.icon["title"].imageload(self.dir + "common/assets/8vana_logo_224_16_edit.png", DARK_GREEN)

        self.icon["bt2019"] = Actor(0, 0)
        self.icon["bt2019"].set_size(255, 252)
        self.icon["bt2019"].imageload(self.dir + "common/assets/bsidestokyo2019/bt.png", GREEN)

        self.chars = [
            "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
            "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
            "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
            "u", "v", "w", "x", "y", "z", "@", '"', "'", "/",
            "_", "<", ">", "(", ")", "!", "?", "#", ",", ".",
            ":", ";"
            ]
        
        self.chars2 = [
            "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
            "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
            "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
            "u", "v", "w", "x", "y", "z", 
            "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
            "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
            "U", "V", "W", "X", "Y", "Z", "@", '"', "'", "/",
            "_", "<", ">", "(", ")", "!", "?", "#", ",", ".",
            ":", ";", "$", "%", "*", "=", "\\", "`", "{", "}"
            ]

        self.font = {}
        self.font["white8"] = Fonts()
        self.font["white8"].imageload(self.dir + "app1vana/images/alpha/num_alpha2_white_pink_150r1.png", PINK)
        self.font["white8"].imagesplit(0, 8, 17, 10, 6, 1, self.chars)

        self.font["white5"] = Fonts()
        self.font["white5"].imageload(self.dir + "app1vana/images/alpha/num_alpha2_white_pink_r1.png", PINK)
        self.font["white5"].imagesplit(0, 5, 11, 10, 6, 1, self.chars)

        self.font["pixelmplus10white"] = Fonts()
        self.font["pixelmplus10white"].imageload(self.dir + "app1vana/images/alpha/PixelMplus10_white_pink_r3.png", PINK)
        self.font["pixelmplus10white"].imagesplit(0, 5, 12, 10, 9, 1, self.chars2)

        self.speed        = 1
        self.distance     = 0
        self.update_frame = 1 # 3くらい？

        self.roles = json.loads(App2.contents)

        # draw mouse cursor
        pyxel.mouse(True)

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.frame_count % self.update_frame == 0:
            self.distance += 1
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()
        if pyxel.btnp(pyxel.KEY_ENTER):
            self.speed += 1

    def draw(self):
        pyxel.cls(0)

        self.icon["title"].put()
        pyxel.text(88, 60, "The visualization tool of", 0)
        pyxel.text(88, 68, "security incidents like retro games.", 0)

        i = 0
        for row in self.roles:
            width = 255
            start_y = 255
            stop_x = 88
            if len(row["title"]) > 0:
                title = "## " + row["title"] + " ##"
            else:
                title = row["title"]
            name = row["name"]
            tlen = len(title)
            nlen = len(name)

            if tlen > width:
                continue
            if nlen > width:
                continue

            distance = self.distance * 1
            mtop = 2

            delta = start_y + i - distance
            mleft = int((width - (tlen * (CHAR_WIDTH - -1))) / 2)
            if delta > stop_x:
                # pyxel.text(mleft, delta, title, WHITE)
                self.font["white8"].pmove_abs(title, mleft, delta)
            i += CHAR_HEIGHT + mtop
            # print(title, ":", mleft, ":",  tlen, ":",  mleft + mleft + (tlen * (CHAR_WIDTH - 1)))

            delta = start_y + i - distance
            # mleft = int((width - (nlen * (CHAR_WIDTH - -1))) / 2)
            mleft = int((width - (nlen * (self.font["pixelmplus10white"].get_width() - 0))) / 2)
            if(delta > stop_x):
                # pyxel.text(mleft, delta, name, WHITE)
                self.font["pixelmplus10white"].pmove_abs(name, mleft, delta)
            # i += CHAR_HEIGHT + CHAR_HEIGHT + mtop
            i += self.font["pixelmplus10white"].get_height() + self.font["pixelmplus10white"].get_height() + mtop
            # print(name, ":", mleft, ":",  nlen, ":",  mleft + mleft + (nlen * (CHAR_WIDTH - 1)))

            delta = start_y + i - distance
            if delta < 1:
                delta = 0
        
        self.icon["bt2019"].pmove_abs(0, delta)
        # Thank you for giving us a precious opportunity.
        if delta < 1:
            pyxel.text(32, 136, "Thank you for giving us a precious opportunity.", PINK)


app = App()

if app.selected_app == 0:
    print("1vana")
    from app1vana.app import App1vana
    App1vana(args.log_time)
elif app.selected_app == 1:
    print("2vana")
    from app2vana.app import App2vana
    from app2vana.util import Utility
    utility = Utility()
    App2vana(utility)

foo = App2()
