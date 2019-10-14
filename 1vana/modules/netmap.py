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

LEVEL_1 = RED
LEVEL_2 = PINK
LEVEL_3 = ORANGE
LEVEL_4 = BLUE
LEVEL_5 = LIGHT_GRAY

WORLDMAP = 0
CLASS_A  = 1
CLASS_B  = 2
CLASS_C  = 3
HOST     = 4


# 描画するログの範囲を指定
VISUALIZE_TIME_RANGE = 30

WINDOW_WIDTH  = 255
WINDOW_HEIGHT = 255
NETMAP_OBJ_WIDTH = 15  # 1 charactor 5pix
NETMAP_OBJ_HEIGHT = 8
NETMAP_OBJ_MARGIN_TOP = 8
NETMAP_OBJ_MARGIN_DOWN = 10
NETMAP_OBJ_MARGIN_RIGHT = 2
NETMAP_BASE_X = 8
NETMAP_BASE_Y = 4

CHAR_WIDTH    = 5
CHAR_HEIGHT   = 7

class Netmap:
    def __init__(
            self,
            vtrange = VISUALIZE_TIME_RANGE,
            char_width = CHAR_WIDTH, char_height = CHAR_HEIGHT,
            l1 = LEVEL_1, l2 = LEVEL_2, l3 = LEVEL_3, l4 = LEVEL_4, l5 = LEVEL_5,
            worldmap = WORLDMAP, class_a = CLASS_A, class_b = CLASS_B, class_c = CLASS_C, host = HOST,
            width = NETMAP_OBJ_WIDTH, height = NETMAP_OBJ_HEIGHT,
            margin_top = NETMAP_OBJ_MARGIN_TOP, margin_down = NETMAP_OBJ_MARGIN_DOWN, margin_right = NETMAP_OBJ_MARGIN_RIGHT,
            base_x = NETMAP_BASE_X, base_y = NETMAP_BASE_Y,
            ww = WINDOW_WIDTH, wh = WINDOW_HEIGHT
        ):
        self.timerange    = vtrange
        self.l1       = l1
        self.l2       = l2
        self.l3       = l3
        self.l4       = l4
        self.l5       = l5
        self.worldmap = worldmap
        self.a        = class_a
        self.b        = class_b
        self.c        = class_c
        self.host     = host
        self.width    = width
        self.height   = height
        self.mtop     = margin_top
        self.mdown    = margin_down
        self.mright   = margin_right
        self.x        = base_x
        self.y        = base_y
        self.ww       = ww
        self.wh       = wh
        self.char_w   = char_width
        self.char_h   = char_height

    def obj(
        self, idx, x, y,  reset=False, cls_color=BLACK, line_color=BLACK, bg_color=DARK_GRAY, font_color=WHITE
        ):

        if(reset):
            pyxel.cls(cls_color)  # reset display color

        s = '%03d' % (idx)
        obj_map = {
            "line_x1" : x - 1,
            "line_y1" : y - 1,
            "line_x2" : x + self.width  + 0,
            "line_y2" : y + self.height + 1,
            "fill_x1" : x - 0,
            "fill_y1" : y - 0,
            "fill_x2" : x + self.width  - 1,
            "fill_y2" : y + self.height + 0,
            "str_x"   : x + self.mright,
            "str_y"   : y + self.mright
        }
        pyxel.rect(obj_map["line_x1"], obj_map["line_y1"], obj_map["line_x2"], obj_map["line_y2"], line_color)
        pyxel.rect(obj_map["fill_x1"], obj_map["fill_y1"], obj_map["fill_x2"], obj_map["fill_y2"], bg_color)
        pyxel.text(obj_map["str_x"],   obj_map["str_y"], s, font_color)  # x, y, string, color
        return True


    def wide_obj(
        self, idx, x, y, xx=0, yy=0, reset=False, cls_color=BLACK, line_color=BLACK, bg_color=DARK_GRAY, font_color=WHITE
        ):

        if(reset):
            pyxel.cls(cls_color)  # reset display color

        s = '%03d' % (idx)
        obj_map = {
            "line_x1" : x - 1 - (xx),
            "line_y1" : y - 1 - (yy),
            "line_x2" : x + self.width  + 0 + (xx),
            "line_y2" : y + self.height + 1 + (yy),
            "fill_x1" : x - 0 - (xx),
            "fill_y1" : y - 0 - (yy),
            "fill_x2" : x + self.width  - 1 + (xx),
            "fill_y2" : y + self.height + 0 + (yy),
            "str_x"   : x + self.mright,
            "str_y"   : y + self.mright
        }
        pyxel.rect(obj_map["line_x1"], obj_map["line_y1"], obj_map["line_x2"], obj_map["line_y2"], line_color)
        pyxel.rect(obj_map["fill_x1"], obj_map["fill_y1"], obj_map["fill_x2"], obj_map["fill_y2"], bg_color)
        pyxel.text(obj_map["str_x"],   obj_map["str_y"], s, font_color)  # x, y, string, color
        return True


    def fill_obj(self, str, x, y, xx=0, yy=0, reset=False, cls_color=BLACK, line_color=BLACK, bg_color=DARK_GRAY, font_color=WHITE):

        if(reset):
            pyxel.cls(0)  # reset display color

        obj_map = {
            "line_x1" : x - 1 - (xx),
            "line_y1" : y - 1 - (yy),
            "line_x2" : x + self.width  + 0 + (xx),
            "line_y2" : y + self.height + 1 + (yy),
            "fill_x1" : x - 0 - (xx),
            "fill_y1" : y - 0 - (yy),
            "fill_x2" : x + self.width  - 1 + (xx),
            "fill_y2" : y + self.height + 0 + (yy),
            "str_x"   : x + self.mright,
            "str_y"   : y + self.mright
        }
        pyxel.rect(obj_map["line_x1"], obj_map["line_y1"], obj_map["line_x2"], obj_map["line_y2"], line_color)
        pyxel.rect(obj_map["fill_x1"], obj_map["fill_y1"], obj_map["fill_x2"], obj_map["fill_y2"], bg_color)
        pyxel.text(obj_map["str_x"],   obj_map["str_y"], str, font_color)  # x, y, string, color
        return True


    #self.netmap_att["offset_x"], self.netmap_att["offset_y"], [ self.netmap_att["list_obj_maps"], [self.netmap_att["selected_obj"]] ]
    def net_obj(self, att, l, node_status={}):
        offset_x      = att["offset_x"]
        offset_y      = att["offset_y"]
        list_obj_maps = att["list_obj_maps"]
        obj_list      = l
        x = self.x + offset_x
        y = self.y + self.mtop + offset_y
        
        #print("x: " + str(offset_x) + ", y:" + str(offset_y))

        for obj_map in list_obj_maps:
            event_time = 0
            addr = list(map(str, att["addr_obj"]))
            addr.append(str(obj_map[0]))
            
            if(
                att["netmap"] == self.worldmap and
                node_status.get(addr[0]) != None
                ):
                status = node_status[addr[0]]["status"]
                if(status["update"] > event_time):
                    event_time = status["update"]
            elif(
                att["netmap"] == self.a and
                node_status.get(addr[0]) != None and
                node_status.get(addr[0]).get(addr[1]) != None
                ):
                status = node_status[addr[0]][addr[1]]["status"]
                if(status["update"] > event_time):
                    event_time = status["update"]
            elif(
                att["netmap"] == self.b and
                node_status.get(addr[0]) != None and
                node_status.get(addr[0]).get(addr[1]) != None and
                node_status.get(addr[0]).get(addr[1]).get(addr[2]) != None
                ):
                status = node_status[addr[0]][addr[1]][addr[2]]["status"]
                if(status["update"] > event_time):
                    event_time = status["update"]
            elif(
                att["netmap"] == self.c and
                node_status.get(addr[0]) != None and
                node_status.get(addr[0]).get(addr[1]) != None and
                node_status.get(addr[0]).get(addr[1]).get(addr[2]) != None and
                node_status.get(addr[0]).get(addr[1]).get(addr[2]).get(addr[3]) != None
                ):
                status = node_status[addr[0]][addr[1]][addr[2]][addr[3]]["status"]
                if(status["update"] > event_time):
                    event_time = status["update"]


            if(obj_map[0] != 0 and obj_map[0] % 16 == 0):
                y += self.mdown
                x = self.x + offset_x
            
            x = (self.x + (obj_map[0] % 16) * self.width) + \
                self.mright + offset_x
            
            (line_color, bg_color, font_color) = (obj_map[5], obj_map[6], obj_map[7])

            # ノードのイベント発生状態からバックグラウンドカラーを選択する
            delta = att["now"] - event_time
            if(   delta >= (0 - self.timerange) and delta <= 60 * 1):
                bg_color = self.l1
            elif( delta >  60 * 1  and delta <= 60 * 5):
                bg_color = self.l2
            elif( delta >  60 * 5  and delta <= 60 * 10):
                bg_color = self.l3
            elif( delta >  60 * 10 and delta <= 60 * 30):
                bg_color = self.l4
            elif( delta >  60 * 30 and delta <= 60 * 60):
                bg_color = self.l5
            

            if(len(obj_list) > 0):
                if(obj_map[0] in obj_list):
                    print("selected_obj: " + str(obj_map[0]))
                    self.obj(obj_map[0], x, y, False, line_color, line_color, bg_color, font_color)
            else:
                self.obj(obj_map[0], obj_map[1], obj_map[2], False, line_color, line_color, bg_color, font_color)

            # time.sleep(5) # dame zettai!
        return True



    def address(self, status):
        # draw network address
        stratum      = status["netmap"]
        selected_obj = status["selected_obj"]
        addr_obj     = status["addr_obj"]
        
        reset = '[push R key to Reset]'
        network = ''
        netmask    = '/'
        if stratum == 0:
            network = '0.0.0.0'
            netmask += str(0)
        elif stratum == 1:
            network = '.'.join(map(str,addr_obj)) + '.0.0.0'
            netmask += str(8)
        elif stratum == 2:
            network = '.'.join(map(str,addr_obj)) + '.0.0'
            netmask += str(16)
        elif stratum == 3:
            network = '.'.join(map(str,addr_obj)) + '.0'
            netmask += str(24)
        elif stratum == 4:
            network = '.'.join(map(str,addr_obj))
            netmask += str(32)
        
        #print("[*] Stratum: " + str(stratum))
        
        address = network + netmask

        pyxel.text(
            self.x,
            self.y,
            address,
            7)  # x, y, string, color

        if(selected_obj > -1):
            pyxel.text(
                self.x + self.mright +
                (len(address) * 5),
                self.y,
                str(selected_obj),
                14)  # x, y, string, color

        pyxel.text(
            (pyxel.width - (len(reset) * self.char_w) -
            self.mright),
            self.y,
            reset,
            9)  # x, y, string, color
        return True
