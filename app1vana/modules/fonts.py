import pyxel
import math
import numpy as np

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

import util
from actor import Actor


DEFAULT_WIN_WIDTH  = 255
DEFAULT_WIN_HTIGHT = 255

util = util.Util()

class Fonts(Actor):
    def __init__(self, x=0, y=0, ibi=0, ibp = [0,0], w=32, h=32, ww=DEFAULT_WIN_WIDTH, wh=DEFAULT_WIN_HTIGHT, ib=""):

        super().__init__(x, y, ibi, ibp, w, h, ib)
        self.char                 = {}
        self.char_width           = 0
        self.char_height          = 0
        self.window_width         = ww
        self.window_height        = wh


    def imagesplit(self, pixmap_index=0, width=8, height=8, count_x=1, count_y=1, margin=0, chars=[], ignore_empty=True):
        """
        インデックスカラー形式のpngファイル（8bit）から等幅な文字列の画像を切り出す。
        pixmap_indexにはactorクラスのimageloadを実行した順番を指定（imageloadで格納された結果はリストで格納されるので、1回目なら0を指定）。
        width,heightは文字のサイズをピクセル単位で指定する。
        count_x,count_yは横と縦に存在する文字数をピクセル単位で指定する。
        marginには文字と文字の間に存在する空白の幅をピクセル単位で指定する。
        charsにはリストで登録する文字の順番を指定する。ここで指定した文字がputs関数で利用できる。
        ignore_emptyがFalseの場合、背景色だけの場所は無視される
        """
        if(len(self.pixmap) == 0):
            return False
        if(len(chars) == 0):
            chars = [
                "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
                "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
                "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
                "u", "v", "w", "x", "y", "z", "_", "<", ">", "(", ")", "!", "?"
            ]

        pixmap      = self.pixmap[pixmap_index]
        max_width   = (width  + 1) * count_x
        #max_height  = (height + 1) * count_y
        #max_chars   = count_x * count_y
        char_width  = width  + margin
        #char_height = height + margin

        charmap = {}
        i = 0
        v = 0
        block = max_width * (height + 1)
        for p in pixmap:
            if(i != 0 and i % max_width == 0):
                v += 1
                #print(v)
            c = int(int(i / char_width) - (v * max_width / char_width) + (int(i / block) * count_x))
            #print(c)
            if(charmap.get(c) == None):
                charmap[c] = [p]
            else:
                charmap[c].append(p)
            i += 1
        
        #print(charmap)
        charmaps = []
        for k in charmap.keys():
            #self.chardump(charmap[k], char_width)
            if(ignore_empty == True):
                total = 0
                length = len(charmap[k])
                for c in charmap[k]:
                    total += c
                if(total / length != self.bg_color):
                    # 空文字排除
                    charmaps.append(charmap[k])
            else:
                charmaps.append(charmap[k])

        self.char = {}
        for i in range(len(charmaps)):
            self.char[chars[i]] = charmaps[i]

        self.char_width  = width  + margin
        self.char_height = height + margin

        #util.chardump(self.char["0"], self.char_width)
        return len(self.char)


    def puts(self, string="", ratio=1):
        """
        文字列を指定済みの座標に表示する
        """
        chars = list(string)
        i = 0
        for c in chars:
            if(c != " "):
                if(self.char.get(c) == None):
                    util.logger("fonts:puts:invalid charactor:" + c, "!")
                else:   
                    if(self.putchar(c, i, ratio) == False):
                        util.logger("Fonts:puts:failed:" + c, "!")
            i += 1

        return i


    def putchar(self, c="", offset=0, ratio=1):
        """
        文字を指定済みの座標に表示する
        """
        pixmap    = self.char.get(c)
        x         = self.position_x
        y         = self.position_y
        start_x   = self.position_x
        start_y   = self.position_y
        color_old = 255 # 存在しない色
        pix_count = 0   # 処理したpixel数
        char_width  = self.char_width
        char_height = self.char_height
        #region_end = 255
        #print("################################# x: %s, y: %s" % (self.position_x, self.position_y))

        if(pixmap == None):
            return False

        # ratioに従ってサイズを変更する
        if(ratio != 1):
            char_width  = self.char_width  * ratio
            char_height = self.char_height * ratio
            pixmap = self.update_scale(pixmap, ratio)
            #pixmap = self.update_scale2(pixmap, ratio)

        for color in pixmap:
            p = pix_count % (char_width) # pix_map上のx座標
            x = self.position_x + p + (offset * char_width)
            #print("p: %s, x: %s, px: %s" % (p, x, self.position_x + p))
            if( pix_count != 0 and (x == 0 or p == 0) ):
                y += 1
                #print("pix_count %s, p: %03s, x: %s, y: %s, x2: %s, y2: %s Y+1" % (int(pix_count / char_width), p, start_x, start_y, x, y))
                if( (y - self.position_y) > char_height or y > self.window_height):
                    break

            # 代替案１： 同じ色が続くことが多いと想定されるため、line関数を利用して描画する回数を減らしている
            if(color != color_old):
                # 色に変化があった
                if(pix_count != 0 and p != 0 and color_old != self.bg_color):
                    # 描画開始地点が初期地点でなく、変化前の色がバックグラウンドカラーでもない
                    if(self.wraparound == True or x >= self.position_x and x < self.window_width):
                        # 画面端より内側
                        pyxel.line(start_x, start_y, (x-1), y, color_old)
                        #print("pix_count %03s, p: %03s, startx: %03s, starty: %03s, x2: %03s, y2: %03s draw" % ( int(pix_count / self.width), p, start_x, start_y, x, y))
                
                
                (start_x, start_y) = (x, y)

            if(x == self.window_width - 1):
                # 画面の最大幅に到達した
                #region_end = p
                if(color != self.bg_color):
                    # 現在選択されている色がバックグラウンドカラーでなければ、現在の色で描画する
                    pyxel.line(start_x, start_y, x, y, color)
                    
                #print("pix_count %03s, p: %03s, x: %s, y: %s, x2: %s, y2: %s window_width" % ( int(pix_count / self.width), p, start_x, start_y, x, y))
                (start_x, start_y) = (0, y + 1)
            
            elif(p == char_width - 1):
                # 画像の最大幅に到達した
                if(color != self.bg_color):
                    # 現在選択されている色がバックグラウンドカラーでなければ、現在の色で描画する
                    pyxel.line(start_x, start_y, x, y, color)
                #print("pix_count %s, p: %03s, x: %s, y: %s, x2: %s, y2: %s img_width" % ( int(pix_count / self.width), p, start_x, start_y, x, y))

                    

                (start_x, start_y) = (self.position_x, (y+1))

            color_old  = color
            pix_count += 1
        
        return True



    def update_scale(self, pixmap, ratio=1):
        """
        画像の表示倍率を変更する
        ratioは整数であり、ratioに指定された倍率で表示する
        """
        print("update_scale:in")
        new_pixmap = pixmap
        list_maps  = []

        # pixmapを行毎のリストに変換する
        i = 0
        for pmap in pixmap:
            idx = int(i / self.char_width)
            if(len(list_maps)-1 != idx):
                list_maps.append([])
            list_maps[idx].append(pmap)
            i += 1
        
        list_maps = np.array(list_maps).repeat(ratio, axis=0).repeat(ratio, axis=1).flatten().tolist()

        new_pixmap = list_maps
        print("update_scale:out")
        return new_pixmap


    def pmove(self, string="", x=0, y=0, ratio=1):
        """
        アクターの座標を相対値でx,yの変更をして表示する
        """
        self.move(self.position_x + x, self.position_y + y)
        self.puts(string, ratio)

    def pmove_x(self, string="", x=0, ratio=1):
        """
        アクターの座標を相対値でxのみ変更して表示する
        """
        self.move_x(self.position_x + x)
        self.puts(string, ratio)

    def pmove_y(self, string="", y=0, ratio=1):
        """
        アクターの座標を相対値でyのみ変更して表示する
        """
        self.move_y(self.position_y + y)
        self.puts(string, ratio)

    def pmove_abs(self, string="", x=0, y=0, ratio=1):
        """
        アクターの座標をx,yで変更して表示する
        """
        self.move(x, y)
        self.puts(string, ratio)

    def pmove_x_abs(self, string="", x=0, ratio=1):
        """
        アクターの座標をxのみ変更して表示する
        """
        self.move_x(x)
        self.puts(string, ratio)

    def pmove_y_abs(self, string="", y=0, ratio=1):
        """
        アクターの座標をyのみ変更して表示する
        """
        self.move_y(y)
        self.puts(string, ratio)






    # ボツ案
    def update_scale2(self, pixmap, ratio):
        print("update_scale:in")
        #new_width  = math.ceil(self.char_width  * ratio)
        #new_height = math.ceil(self.char_height * ratio)
        new_width  = round(self.char_width  * ratio)
        new_height = round(self.char_height * ratio)
        new_pixmap = pixmap
        list_maps  = []

        # pixmapを行毎のリストに変換する
        i = 0
        for pmap in pixmap:
            idx = int(i / self.char_width)
            if(len(list_maps)-1 != idx):
                list_maps.append([])
            list_maps[idx].append(pmap)
            i += 1
        

        # 横のスケールを変更する
        h_list_maps = []
        for pmap in list_maps:
            #print(m)
            count = 0
            old   = 255 # 存在しない値
            pmap_new   = []
            for i in range(len(pmap)):
                if(i == 0 or pmap[i] == old):
                    count += 1
                else:
                    scale = math.floor(count * ratio)
                    if(scale > new_width / 2):
                        scale -= 1
                    elif(scale < new_width / 6):
                        scale += 1
                    new_count = scale
                    #new_count = math.ceil(count * ratio)
                    #new_count = math.floor(count * ratio)
                    if(new_count >= new_width):
                        new_count -= 1
                    #new_count = math.floor(count * ratio)
                    #print("count: %d, ratio: %d" %(count, ratio))
                    count     = 0
                    list(map(lambda x: pmap_new.append(old), range(new_count)))
                
                if(i >= len(pmap) - 1):
                    new_count = new_width - len(pmap_new)
                    count     = 0
                    list(map(lambda x: pmap_new.append(pmap[i]), range(new_count)))
                
                old = pmap[i]
            h_list_maps.append(pmap_new)


        util.chardump(pixmap, self.char_width)

        # pixmapを列毎のリストに変換する
        list_maps = []
        for idx in range(new_width):
            list_maps.append([])

        i = 0
        for pmap in h_list_maps:
            for idx in range(len(pmap)):
                list_maps[idx].append(pmap[idx])
            i += 1
        


        for pmap in h_list_maps:
            print(pmap)


        # 縦のスケールを変更する
        v_list_maps = []
        for pmap in list_maps:
            #print(m)
            count = 0
            old   = 255 # 存在しない値
            pmap_new   = []
            for i in range(len(pmap)):
                if(i == 0 or pmap[i] == old):
                    count += 1
                else:
                    scale = math.floor(count * ratio)
                    if(scale > new_height / 2):
                        scale -= 1
                    elif(scale < new_height / 6):
                        scale += 1
                    new_count = scale
                    #new_count = math.ceil(count * ratio)
                    #new_count = math.floor(count * ratio)
                    #if(new_count == new_height):
                    #    new_count -= 1
                    #new_count = math.floor(count * ratio)
                    #print("count: %d, ratio: %d" %(count, ratio))
                    count     = 0
                    list(map(lambda x: pmap_new.append(old), range(new_count)))
                
                if(i >= len(pmap) - 1):
                    new_count = new_height - len(pmap_new)
                    count     = 0
                    list(map(lambda x: pmap_new.append(pmap[i]), range(new_count)))
                
                old = pmap[i]
            v_list_maps.append(pmap_new)



        # 1次元のリストに変換する
        list_maps = []
        i = 0
        for i in range(new_height):
            for pmap in v_list_maps:
                list_maps.append(pmap[i])
            i += 1

        # for debug
        #for pmap in list_maps:
        #    print(pmap)
        #for pmap in h_list_maps:
        #    print(pmap)
        #for pmap in v_list_maps:
        #    print(pmap)
        #self.chardump(list_maps, new_width)

        new_pixmap = list_maps
        print("update_scale:out")
        return new_pixmap
