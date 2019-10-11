import os
import pyxel

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))
import imageloader

DEFAULT_BG_COLOR   = 7   # env.WHITE
DEFAULT_WIN_WIDTH  = 255
DEFAULT_WIN_HTIGHT = 255
DEFAULT_ICON_ACTION_WAIT = 8

class Actor:
    def __init__(self, x=0, y=0, ibi=0, ibp = [0,0], w=32, h=32, iaw=DEFAULT_ICON_ACTION_WAIT, ww=DEFAULT_WIN_WIDTH, wh=DEFAULT_WIN_HTIGHT, ib=""):
        if(type(ibi) != "int" or ibi > 2):
            ibi = 0
        
        if(type(ibp) != "list" or type(ibp[0]) != "int" or type(ibp[1]) != "int" or ibp[0] < 0 or ibp[0] > 255 or ibp[1] < 0 or ibp[1] > 255):
            ibp = [0,0]
        
        self.position_x        = x
        self.position_y        = y
        self.img_bank          = ib
        self.img_bank_index    = ibi
        self.width             = w
        self.height            = h
        self.actions           = [ibp] # position of image bank
        self.frame             = 0
        self.action_wait       = 4
        self.pixmap            = []    # pixel map for ImageLoader
        self.wraparound        = False
        self.window_width      = ww
        self.window_height     = wh
        self.bg_color          = DEFAULT_BG_COLOR # env.WHITE
        self.icon_action_wait  = iaw
        self.draw = 0


    def imageload(self, source_file="", bg_color=DEFAULT_BG_COLOR):
        if(source_file != "" and os.path.exists(source_file)):
            self.img_bank     = source_file
            self.set_bg_color(bg_color)
        
        if(os.path.exists(self.img_bank)): 
            im = imageloader.ImageLoader(self.img_bank)
            self.pixmap.append(im.get_pixelmap())
            wh = im.get_size()
            self.width  = wh[0]
            self.height = wh[1]
            #print(im.show(im.get_pixelmap(), wh[0]))
        else:
            print("[!] Imageload: file not found: " + self.img_bank)


    def load(self, source_file):
        pyxel.image(self.img_bank_index).load(0, 0, source_file)


    def put(self):
        """
        アクターを指定済みの座標に表示する
        """
        # 登録されている画像やイメージバンクの範囲の数をカウントする
        # この処理はImageLoaderで読み込まれたデータが優先される
        actions_count = len(self.pixmap) if len(self.pixmap) > 0 else len(self.actions)
        if(pyxel.frame_count % self.icon_action_wait == 0):
            if self.frame >= actions_count - 1:
                self.frame = 0
            else:
                self.frame += 1
        
        if(len(self.pixmap) > 0):
            # pixmapが空でなければImageLoaderが利用されているので優先する
            pixmap    = self.pixmap[self.frame]
            x         = self.position_x
            y         = self.position_y
            start_x   = self.position_x
            start_y   = self.position_y
            color_old = 255 # 存在しない色
            pix_count = 0   # 処理したpixel数
            #region_end = 255
            #print("################################# x: %s, y: %s" % (self.position_x, self.position_y))
            for color in pixmap:
                p = pix_count % (self.width) # pix_map上のx座標
                x = self.position_x + p
                #print("p: %s, x: %s, px: %s" % (p, x, self.position_x + p))
                if( pix_count != 0 and (x == 0 or p == 0) ):
                    y += 1
                    #print("pix_count %s, p: %03s, x: %s, y: %s, x2: %s, y2: %s Y+1" % (int(pix_count / self.width), p, start_x, start_y, x, y))
                    if( (y - self.position_y) > self.height or y > self.window_height):
                        break

                # 代替案１： 同じ色が続くことが多いと想定されるため、line関数を利用して描画する回数を減らしている
                if(color != color_old):
                    # 色に変化があった
                    if(pix_count != 0 and p != 0 and color_old != self.bg_color):
                        # 描画開始地点が初期地点でなく、変化前の色がバックグラウンドカラーでもない
                        if(self.wraparound == True or x >= self.position_x):
                            # 回り込み描画が有効またはx座標が初期位置よりも大きい場合、変化前の色で1pixel手前まで描画する
                            # ようにしようと思ったが、バグってるし使わないのでとりあえず放置
                            #if(start_x >= self.position_x):
                            #    pyxel.line(start_x, start_y, (x-1)-self.position_x - region_end, y, color_old)
                            #    print("pix_count %s, p: %03s, x: %s, y: %s, x2: %s, y2: %s change_color left"  % (int(pix_count / self.width), p, start_x, start_y, (x-1)-self.position_x - region_end, y))
                            #else:
                            #    pyxel.line(start_x, start_y, (x-1), y, color_old)
                            #    print("pix_count %s, p: %03s, x: %s, y: %s, x2: %s, y2: %s change_color right" % (int(pix_count / self.width), p, start_x, start_y, (x-1), y))
                            pyxel.line(start_x, start_y, (x-1), y, color_old)
                            self.draw = 1
                    #if pix_count != 0 and self.width == 8:
                    #    for i in range(int(start_x), int(x)):
                    #        print("%2d" % (color_old), end="")
                    #    print()
                    #    print("pix_count %s, p: %03s, x: %s, y: %s, x2: %s, y2: %s change_color %s" % (int(pix_count / self.width), p, start_x, start_y, x, y, self.draw))
                    self.draw = 0
                    
                    
                    (start_x, start_y) = (x, y)

                if(x == self.window_width - 1):
                    # 画面の最大幅に到達した
                    #region_end = p
                    if(color != self.bg_color):
                        # 現在選択されている色がバックグラウンドカラーでなければ、現在の色で描画する
                        pyxel.line(start_x, start_y, x, y, color)
                    #print("pix_count %s, p: %03s, x: %s, y: %s, x2: %s, y2: %s window_width" % ( int(pix_count / self.width), p, start_x, start_y, x, y))
                    (start_x, start_y) = (0, y + 1)
                
                elif(p == self.width - 1):
                    # 画像の最大幅に到達した
                    if(color != self.bg_color):
                        # 現在選択されている色がバックグラウンドカラーでなければ、現在の色で描画する
                        pyxel.line(start_x, start_y, x, y, color)
                        

                    #if self.width == 8:
                    #    for i in range(int(start_x), int(x+1)):
                    #        print("%2d" % (color), end="")
                    #    print()
                    #print("pix_count %s, p: %03s, x: %s, y: %s, x2: %s, y2: %s image_width" % (int(pix_count / self.width), p, start_x, start_y, x, y))
                    #print()
                    (start_x, start_y) = (self.position_x, (y+1))
                    

                color_old  = color
                pix_count += 1
            
            # 代替案１： 最後の1ラインを描画する
            #if(color_old != self.bg_color):
            #    pyxel.line(start_x, start_y, x, y, color_old)
            #print()
            #print("[+] ImageLoader: x: %s(%s), y: %s" % (x, idx / width,y))

            #if self.width == 8:
            #    i = 0
            #    for p in (pixmap):
            #        if i % 8 == 0:
            #            print()
            #        print("%2d" % (p), end="")
            #        i += 1
            #print()
        else:
            #print(str(len(self.actions)) + "," + str(self.frame) + ", [" + str(self.actions[self.frame][0]) + "," + str(self.actions[self.frame][1]) + "]")
            pyxel.blt(self.position_x, self.position_y, self.img_bank_index, self.actions[self.frame][0], self.actions[self.frame][1], self.width, self.height, DEFAULT_BG_COLOR)


    def pmove(self, x=0, y=0):
        """
        アクターの座標を相対値でx,yの変更をして表示する
        """
        self.move(self.position_x + x, self.position_y + y)
        self.put()

    def pmove_x(self, x=0):
        """
        アクターの座標を相対値でxのみ変更して表示する
        """
        self.move_x(self.position_x + x)
        self.put()

    def pmove_y(self, y=0):
        """
        アクターの座標を相対値でyのみ変更して表示する
        """
        self.move_y(self.position_y + y)
        self.put()

    def pmove_abs(self, x=0, y=0):
        """
        アクターの座標をx,yで変更して表示する
        """
        self.position_x = x
        self.position_y = y
        self.put()

    def pmove_x_abs(self, x=0):
        """
        アクターの座標をxのみ変更して表示する
        """
        self.move_x(x)
        self.put()

    def pmove_y_abs(self, y=0):
        """
        アクターの座標をyのみ変更して表示する
        """
        self.move_y(y)
        self.put()



    def set_frame(self, index):
        """
        アクターのフレームを設定する
        """
        self.frame = index
        return self.frame

    def set_size(self, w=32, h=32):
        """
        アクターサイズを設定する
        """
        self.width = w
        self.height = h
        return [self.width, self.height]

    def set_img_bank_index(self, ibi=0):
        """
        イメージバンクのインデックスを設定する
        """
        if type(ibi) != "int" or ibi > 2:
            ibi=0
        self.img_bank_index = ibi
        return self.img_bank_index


    def set_img_bank(self, ib):
        """
        イメージバンクとして利用するファイル指定する
        """
        if os.path.exists(ib) == False:
            ib = ""
        self.img_bank = ib
        return self.img_bank


    def set_wraparound(self, boolean=True):
        """
        画像の回り込みを表示するか決めるフラグを切り替える
        """
        if boolean == True:
            self.wraparound = True
        else:
            self.wraparound = False
        return self.wraparound


    def set_bg_color(self, bg_color=DEFAULT_BG_COLOR):
        if(bg_color >= 0 and bg_color <= 16):
            self.bg_color = bg_color
        return True


    def move(self, x, y):
        """
        アクターの座標をx,yを指定して変更する
        """
        self.position_x = x
        self.position_y = y
    
    def move_x(self, x):
        """
        アクターの座標をxのみ指定して変更する
        """
        self.position_x = x
    
    def move_y(self, y):
        """
        アクターの座標をyのみ指定して変更する
        """
        self.position_y = y



    def set_frame_wait(self, wait):
        """
        アニメーションを行うフレームの間隔を指定する
        """
        self.frame_wait = wait

    def add_frame(self, ibp):
        """
        イメージバンクを利用したアニメーションのために別のイメージの範囲を追加する
        """
        if(
            type(ibp)    is not list or
            type(ibp[0]) is not int  or
            type(ibp[1]) is not int  or
            ibp[0] < 0   or
            ibp[0] > 255 or
            ibp[1] < 0   or
            ibp[1] > 255
            ):
            self.logger("add_frame: invalid argument" + str(ibp), "!")
            ibp = [0,0]
        self.actions.append(ibp)

    def reset_frame(self):
        """
        追加したアニメーションを削除する
        """
        self.actions = [self.actions[0]]

    def fullreset_frame(self):
        """
        アニメーションをすべて削除する
        """
        self.actions = []
        self.pixmap  = []

    def list_actions(self):
        """
        アニメーションの一覧を表示する
        """
        print(self.actions)

    def get_position(self):
        """
        アイコンのx,yを返す
        """
        x = self.position_x
        y = self.position_y
        return [x, y]

    def get_center_position(self):
        """
        アイコンの中心のx,yを返す
        """
        x = self.position_x + (self.width /2)
        y = self.position_y + (self.height/2)
        return [x, y]

    def logger(self, m, o="+"):
        print("[" + o + "] " + str(m))




    def put2(self, bgcolor=DEFAULT_BG_COLOR):
        """
        アクターを指定済みの座標に表示する
        """
        # 登録されている画像やイメージバンクの範囲の数をカウントする
        # この処理はImageLoaderで読み込まれたデータが優先される
        actions_count = len(self.pixmap) if len(self.pixmap) > 0 else len(self.actions)
        if(pyxel.frame_count % self.icon_action_wait == 0):
            if self.frame >= actions_count - 1:
                self.frame = 0
            else:
                self.frame += 1
        
        if(len(self.pixmap) > 0):
            # pixmapが空でなければImageLoaderが利用されているので優先する
            pixmap    = self.pixmap[self.frame]
            x         = self.position_x
            y         = self.position_y
            start_x   = self.position_x
            start_y   = self.position_y
            color_old = 255 # 存在しない色
            pix_count = 0   # 処理したpixel数
            #print("################################# x: %s, y: %s" % (self.position_x, self.position_y))
            for color in pixmap:
                p = pix_count % (self.width) # pix_map上のx座標
                x = self.position_x + p
                #print("p: %s, x: %s, px: %s" % (p, x, self.position_x + p))
                if( pix_count != 0 and (x == 0 or p == 0) ):
                    y += 1
                    #print("pix_count %s, p: %03s, x: %s, y: %s, x2: %s, y2: %s Y+1" % (int(pix_count / self.width), p, start_x, start_y, x, y))
                    if( (y - self.position_y) > self.height or y > self.window_height):
                        break

                # ボツ案： 単純にpixel単位で描画する方式だと描画回数が限界を超えて(?)表示できなくなってしまう
                if(color != bgcolor):
                    if self.wraparound == True or self.wraparound == False and x >= self.position_x:
                        pyxel.pix(x, y, color)

                color_old  = color
                pix_count += 1
            
            # 代替案１： 最後の1ラインを描画する
            if(color_old != bgcolor):
                pyxel.line(start_x, start_y, x, y, color_old)
            #print("[+] ImageLoader: x: %s(%s), y: %s" % (x, idx / width,y))

        else:
            #print(str(len(self.actions)) + "," + str(self.frame) + ", [" + str(self.actions[self.frame][0]) + "," + str(self.actions[self.frame][1]) + "]")
            pyxel.blt(self.position_x, self.position_y, self.img_bank_index, self.actions[self.frame][0], self.actions[self.frame][1], self.width, self.height, DEFAULT_BG_COLOR)
