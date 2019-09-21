#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import argparse
import pyxel
import time
import datetime
import json
import math
import re

import env
import util
import actor
import actor_state
import digest
import draw
import fonts


WINDOW_WIDTH  = 255
WINDOW_HEIGHT = 255

d      = draw.Draw()
util   = util.Util()
digest = digest.Digest()

# 引数の処理
parser = argparse.ArgumentParser(description='1vana')
parser.add_argument('-l','--log_time',
    help='このオプションは、ログ再生機能で利用することを想定されており、ログファイル先頭のリソース（最も古いログ）から時刻を取得し、開始時刻の基準値として利用します。このオプションを利用しない場合は、現在時刻が開始時刻として利用されます。',
    action="store_true")
args = parser.parse_args()

class App:
    def __init__(self):
        pyxel.init(WINDOW_WIDTH, WINDOW_HEIGHT, caption="8vana: Network Map")
        self.dir = os.path.dirname(os.path.abspath("__file__")) + "/"
        self.x = 0

        discover = r"^discovery?$"
        attack   = r"^attack$"
        self.re_discover = re.compile(discover, re.IGNORECASE)
        self.re_attack   = re.compile(attack,   re.IGNORECASE)

        self.font_scale      = 1
        self.font_position_x = 0
        self.font_position_y = 0

        print('width: ' + str(pyxel.width))
        print('height: ' + str(pyxel.height))

        self.log            = []
        self.log_path       = self.dir + env.INPUT_LOG
        self.log_hash       = ""
        self.log_lastupdate = 0
        self.time_begin     = 0
        if(os.path.exists(self.log_path)):
            self.log_hash = digest.file_hash(self.log_path)
            with open(self.dir + env.INPUT_LOG, 'r') as json_file :
                self.log = json.load(json_file)
                print("[option]log_time: " + str(args.log_time))
                if(args.log_time != False):
                    self.time_begin = self.log[0]["time"] - env.VISUALIZE_TIME_RANGE - env.VISUALIZE_TIME_WAIT
                else:
                    now = datetime.datetime.now()
                    epoch = int(now.timestamp())
                    self.time_begin = epoch

                print("[%s] %s, hash: %s\n" % (str(self.time_begin), "log update", self.log_hash))
        
        print(self.dir)
        pyxel.image(0).load(0, 0, self.dir + "images/zei255-red.png")
        pyxel.image(1).load(0, 0, self.dir + "images/debian64.png")
        pyxel.image(2).load(0, 0, self.dir + "images/icons255.png")

        self.icon = {}
        self.actor = {}
        self.bg = {}
        self.title = {}
        self.title["ma"] = {
            "base_y": 177,
            "x": 177,
            "y": 177
        }
        self.title["block"] = {
            "base_y": 127,
            "x": 107,
            "y": 127
        }

        # ImageLoaderを利用したアイコンの登録
        self.icon["world"] = actor.Actor(env.NETMAP_BASE_X, 175)
        self.icon["world"].set_size(32, 32)
        self.icon["world"].imageload(self.dir + "images/internet1_32.png")
        self.icon["world"].imageload(self.dir + "images/internet2_32.png")

        self.icon["arrow"] = actor.Actor()
        self.icon["arrow"].imageload(self.dir + "images/arrow1_up_8.png")

        self.icon["search"] = actor.Actor()
        self.icon["search"].set_size(8,8)
        self.icon["search"].imageload(self.dir + "images/search3_8.png")
        self.icon["search"].imageload(self.dir + "images/search2_8.png")


        self.icon["log1"] = actor.Actor()
        self.icon["log1"].set_size(8,8)
        self.icon["log1"].imageload(self.dir + "images/logarea1_8_16.png")
        self.icon["log2"] = actor.Actor()
        self.icon["log2"].set_size(8,8)
        self.icon["log2"].imageload(self.dir + "images/logarea2_8_16.png")
        self.icon["log3"] = actor.Actor()
        self.icon["log3"].set_size(8,8)
        self.icon["log3"].imageload(self.dir + "images/logarea3_8_16.png")
        self.icon["log4"] = actor.Actor()
        self.icon["log4"].set_size(8,8)
        self.icon["log4"].imageload(self.dir + "images/logarea4_8_16.png")

        self.icon["logvl"] = actor.Actor()
        self.icon["logvl"].set_size(8,8)
        self.icon["logvl"].imageload(self.dir + "images/logarea_vl_8_16.png")
        self.icon["logvr"] = actor.Actor()
        self.icon["logvr"].set_size(8,8)
        self.icon["logvr"].imageload(self.dir + "images/logarea_vr_8_16.png")

        self.icon["loght"] = actor.Actor()
        self.icon["loght"].set_size(8,8)
        self.icon["loght"].imageload(self.dir + "images/logarea_ht_8_16.png")
        self.icon["loghb"] = actor.Actor()
        self.icon["loghb"].set_size(8,8)
        self.icon["loghb"].imageload(self.dir + "images/logarea_hb_8_16.png")


        self.icon["fire"] = actor.Actor()
        self.icon["fire"].imageload(self.dir + "images/fire1_8_16.png")
        self.icon["fire"].imageload(self.dir + "images/fire2_8_16.png")

        self.icon["mono"] = actor.Actor()
        self.icon["mono"].imageload(self.dir + "images/mono/01.png")
        self.icon["mono"].imageload(self.dir + "images/mono/02.png")
        self.icon["mono"].imageload(self.dir + "images/mono/03.png")
        self.icon["mono"].imageload(self.dir + "images/mono/04.png")
        self.icon["mono"].imageload(self.dir + "images/mono/05.png")
        self.icon["mono"].imageload(self.dir + "images/mono/06.png")
        self.icon["mono"].imageload(self.dir + "images/mono/07.png")
        self.icon["mono"].imageload(self.dir + "images/mono/08.png")
        self.icon["mono"].imageload(self.dir + "images/mono/09.png")
        self.icon["mono"].imageload(self.dir + "images/mono/10.png")
        self.icon["mono"].imageload(self.dir + "images/mono/11.png")

        self.icon["unknown"] = actor.Actor(96, 24)
        self.icon["unknown"].imageload(self.dir + "images/unknown64.png")

        self.icon["debian"] = actor.Actor(96, 24)
        self.icon["debian"].imageload(self.dir + "images/debian64.png")

        self.icon["zeijyaku255"] = actor.Actor()
        self.icon["zeijyaku255"].imageload(self.dir + "images/zei255-red.png")



        #self.fonts = fonts.Fonts()
        #self.fonts.imageload(self.dir + "images/alpha/num_alpha.png")
        #pixmap_index=0, width=8, height=8, count_x=1, count_y=1, margin=0, bg_color=env.WHITE, ignore_empty=True
        #self.fonts.imagesplit(0, 24, 44, 10, 5, 1)
        #pixmap_index=0, width=8, height=8, count_x=1, count_y=1, margin=0, bg_color=env.WHITE, ignore_empty=True
        #self.fonts.imageload(self.dir + "images/alpha/num_alpha2.png")
        #self.fonts.imagesplit(0, 5, 11, 10, 5, 1)

        #self.fonts_white = fonts.Fonts()
        #self.fonts_white.imageload(self.dir + "images/alpha/num_alpha2_white_pink.png", env.PINK)
        #self.fonts_white.imagesplit(0, 5, 11, 10, 5, 1)

        #self.fonts_white150 = fonts.Fonts()
        #self.fonts_white150.imageload(self.dir + "images/alpha/num_alpha2_white_pink_150.png", env.PINK)
        #self.fonts_white150.imagesplit(0, 8, 17, 10, 5, 1)

        self.view_object  = 0
        self.mouse_x      = 0
        self.mouse_y      = 0

        self.page = {
            "log"     : 0,
            "monolith": 0
        }

        self.monolith_nextline_x1 = 0
        self.monolith_nextline_y1 = 0
        self.monolith_nextline_x2 = 0
        self.monolith_nextline_y2 = 0

        self.view_object_scale    = 0
        self.view_object_scale_x  = 0
        self.view_object_scale_y  = 0
        self.view_object_scale_x2 = 0
        self.view_object_scale_y2 = 0
        self.frame_counter        = 0
        self.frame_appstart       = 1
        self.passed_seconds       = 0
        self.passed_seconds_real  = 0
        self.bgcolor              = env.DARK_BLUE

        self.netmap_att = {
            "netmap"       : 0,
            "selected_obj" : -1,
            "addr_obj"     : [],
            "list_obj_maps": [],
            "move_right"   : 0,
            "move_left"    : 0,
            "move_up"      : 0,
            "move_down"    : 0,
            "offset_x"     : 0,
            "offset_y"     : 0,
        }

        self.node_status = {}

        self.targets     = []
        self.targets_len = 0
        self.bullets     = []
        self.bullet_init = 1



        # there is include map address of display objects.
        x = env.NETMAP_BASE_X
        y = env.NETMAP_BASE_Y + env.NETMAP_OBJ_MARGIN_TOP
        for num in range(0, 256, 1):
            if(num != 0 and num % 16 == 0):
                y += env.NETMAP_OBJ_MARGIN_DOWN
                x = env.NETMAP_BASE_X

            x = (env.NETMAP_BASE_X + (num % 16) * env.NETMAP_OBJ_WIDTH) + \
                env.NETMAP_OBJ_MARGIN_RIGHT
            line_color = env.BLACK
            bg_color   = env.DARK_GRAY
            font_color = env.WHITE
            self.netmap_att["list_obj_maps"].append(
                [num, x, y, x + env.NETMAP_OBJ_WIDTH, y + env.NETMAP_OBJ_HEIGHT, line_color, bg_color, font_color])

        # draw mouse cursor
        pyxel.mouse(True)

        pyxel.run(self.update, self.draw)



    def update(self):
        self.netmap_att["now"] = self.get_now()

        if(self.netmap_att["netmap"]   == env.WORLDMAP):
            self.bgcolor = env.DARK_BLUE
        elif(self.netmap_att["netmap"] == env.CLASS_A):
            self.bgcolor = env.BROWN
        elif(self.netmap_att["netmap"] == env.CLASS_B):
            self.bgcolor = env.DARK_GREEN
        elif(self.netmap_att["netmap"] == env.CLASS_C):
            self.bgcolor = env.BLACK
        
        # 経過時間（秒）を取得
        if(self.frame_appstart > 0):
            self.passed_seconds      = (pyxel.frame_count - self.frame_appstart) / env.FRAME_SECOND
            self.passed_seconds_real = (pyxel.frame_count - self.frame_appstart) / env.FRAME_SECOND_REAL

        # 最新ログの読み込み処理
        if(self.passed_seconds_real % env.LOG_POLLING_TIME == 0):
            if(os.path.exists(self.log_path)):
                current_log_hash = self.log_hash
                self.log_hash    = digest.file_hash(self.log_path)
                print("[%s] %s, hash: %s, %s" % (str(self.get_now()), "begin log update process", current_log_hash, self.log_hash))
                if(current_log_hash == self.log_hash):
                    with open(self.dir + env.INPUT_LOG, 'r') as json_file :
                        self.log = json.load(json_file)
                print("[%s] %s, hash: %s, %s" % (str(self.get_now()), "end log update process", current_log_hash, self.log_hash))

        # ログの情報を格納する
        self.targets = []
        for row in self.log:
            now = self.get_now()
            #print("[%s]:%s:%s" % (str("{:.1f}".format(now)), row["time"], float(row["time"]) - now))
            if(
                row["time"] >= now and row["time"] > now - env.VISUALIZE_TIME_RANGE and
                row["time"] >= now and row["time"] < now + env.VISUALIZE_TIME_RANGE
            ):

                # 現在時間+描画範囲の秒数以内
                self.targets.append(row)

                # 宛先がIPv4のIPアドレスであることを確認する
                ip = row["to"].split(".")

                # IPv4のIPアドレスであればリストな長さは4になる
                if len(ip) == 4:
                    row["draw"] = True
                else:
                    row["draw"] = False
                    break

                # ノードの状態を更新する
                if(ip[0] not in self.node_status):
                    self.node_status[ip[0]] = {}
                if(ip[1] not in self.node_status[ip[0]]):
                    self.node_status[ip[0]][ip[1]] = {}
                if(ip[2] not in self.node_status[ip[0]][ip[1]]):
                    self.node_status[ip[0]][ip[1]][ip[2]] = {}
                if(ip[3] not in self.node_status[ip[0]][ip[1]][ip[2]]):
                    self.node_status[ip[0]][ip[1]][ip[2]][ip[3]] = {}
                self.node_status[ip[0]]["status"]                      = { "update": row["time"], "phase": row["phase"] }
                self.node_status[ip[0]][ip[1]]["status"]               = { "update": row["time"], "phase": row["phase"] }
                self.node_status[ip[0]][ip[1]][ip[2]]["status"]        = { "update": row["time"], "phase": row["phase"] }
                self.node_status[ip[0]][ip[1]][ip[2]][ip[3]]["status"] = { "update": row["time"], "phase": row["phase"] }
            elif(row["time"] > now + env.VISUALIZE_TIME_RANGE):
                break
            #print(self.node_status)
        if(len(self.targets) != self.targets_len):
            self.bullet_init = 1
        self.targets_len = len(self.targets)


        # if press key `ENTER` then start the app
        #if pyxel.btnp(pyxel.KEY_ENTER):
        #    self.netmap_att["netmap"] = 0
        #    self.frame_appstart       = pyxel.frame_count



        # if press key `Q` then quit the app
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()



        # if press key `R` then reset the app
        if pyxel.btnp(pyxel.KEY_R):
            self.reset_params()
        
        # (test) move square object to left to right and loop
        self.x = (self.x + 1) % pyxel.width

        # set the selected network map object
        if(pyxel.btnr(pyxel.MOUSE_LEFT_BUTTON) and self.netmap_att["netmap"] < 255):
            self.mouse_x = pyxel.mouse_x
            self.mouse_y = pyxel.mouse_y
            
            for obj_map in self.netmap_att["list_obj_maps"]:
                # check the location of object
                if(
                    self.view_object != env.VIEW_MONOLITH and
                    self.mouse_x >= obj_map[1] and
                    self.mouse_x <= obj_map[3] and
                    self.mouse_y >= obj_map[2] and
                    self.mouse_y <= obj_map[4]
                ):
                    print("object_id: " + str(obj_map[0]))
                    self.netmap_att["selected_obj"] = obj_map[0]

                    print("#### position x: "+ str(obj_map[1]) +" y: "+ str(obj_map[2]) +" width: " + str(pyxel.width/2) + " height: " + str(pyxel.height/2))
                    if(obj_map[1] < pyxel.width / 2):
                        self.netmap_att["move_right"] = 1
                    if(obj_map[1] > pyxel.width / 2):
                        self.netmap_att["move_left"]  = 1
                    if(obj_map[2] < pyxel.height / 2):
                        self.netmap_att["move_down"]  = 1
                    if(obj_map[2] > pyxel.height / 2):
                        self.netmap_att["move_up"]    = 1

                    self.print_move_flags()
                    break

            if(
                self.view_object != env.VIEW_MONOLITH and
                self.mouse_x > env.LOG_FRAME_X1 and
                self.mouse_x < env.LOG_FRAME_X2 and
                self.mouse_y > env.LOG_FRAME_Y1 and
                self.mouse_y < env.LOG_FRAME_Y2
            ):
                self.page["log"] += 1
                util.logger("page[\"log\"]" + str(self.page["log"]))


            if(
                self.view_object == env.VIEW_MONOLITH and
                self.mouse_x > self.monolith_nextline_x1 and
                self.mouse_x < self.monolith_nextline_x1 + (env.CHAR_WIDTH * 2) and
                self.mouse_y > self.monolith_nextline_y1 and
                self.mouse_y < self.monolith_nextline_y2
            ):
                self.page["monolith"] -= env.MONOLITH_PREVIOUS_AMOUNT2
                util.logger("page[\"monolith\"]:<<:" + str(self.page["monolith"]))

            elif(
                self.view_object == env.VIEW_MONOLITH and
                self.mouse_x > self.monolith_nextline_x2 - (env.CHAR_WIDTH * 2) and
                self.mouse_x < self.monolith_nextline_x2 and
                self.mouse_y > self.monolith_nextline_y1 and
                self.mouse_y < self.monolith_nextline_y2
            ):
                self.page["monolith"] += env.MONOLITH_NEXT_AMOUNT2
                util.logger("page[\"monolith\"]:>>:" + str(self.page["monolith"]))

            elif(
                self.view_object == env.VIEW_MONOLITH and
                self.mouse_x > self.monolith_nextline_x1 + (env.CHAR_WIDTH * 5) and
                self.mouse_x < self.monolith_nextline_x1 + (env.CHAR_WIDTH * 7) and
                self.mouse_y > self.monolith_nextline_y1 and
                self.mouse_y < self.monolith_nextline_y2
            ):
                self.page["monolith"] -= env.MONOLITH_NEXT_AMOUNT1
                util.logger("page[\"monolith\"]:<-:" + str(self.page["monolith"]))


            elif(
                self.view_object == env.VIEW_MONOLITH and
                self.mouse_x > self.monolith_nextline_x2 - (env.CHAR_WIDTH * 7) and
                self.mouse_x < self.monolith_nextline_x2 - (env.CHAR_WIDTH * 5) and
                self.mouse_y > self.monolith_nextline_y1 and
                self.mouse_y < self.monolith_nextline_y2
            ):
                self.page["monolith"] += env.MONOLITH_NEXT_AMOUNT1
                util.logger("page[\"monolith\"]:->:" + str(self.page["monolith"]))

            elif(
                self.view_object == env.VIEW_MONOLITH and
                self.mouse_x > env.MONOLITH_X1 and
                self.mouse_x < env.MONOLITH_X2 and
                self.mouse_y > env.MONOLITH_Y1 and
                self.mouse_y < env.MONOLITH_Y2
            ):
                self.page["monolith"] += 1
                util.logger("page[\"monolith\"]:>:" + str(self.page["monolith"]))

        # set offset x,y when click the network map object
        obj_map = ''
        if(self.is_netmap_move() > 0):
            selected_obj = self.netmap_att["selected_obj"]
            obj_map      = self.netmap_att["list_obj_maps"][selected_obj]

            # move left
            if(self.netmap_att["move_left"] > 0 ):
                if(self.netmap_att["offset_x"] > self.get_new_place_x1(obj_map) + env.MOVE_X):
                    self.netmap_att["offset_x"] -= env.MOVE_X
                    self.print_position(obj_map, 'netmap_offset_x')
                else:
                    self.netmap_att["offset_x"] = self.get_new_place_x1(obj_map)
                    self.print_position(obj_map, 'finish x')
                    self.netmap_att["move_left"] = 0


            # move up
            if(self.netmap_att["move_up"] > 0 ):
                if(self.netmap_att["offset_y"] > self.get_new_place_y1(obj_map) + env.MOVE_Y):
                    self.netmap_att["offset_y"] -= env.MOVE_Y
                    self.print_position(obj_map, 'netmap_offset_y')
                else:
                    self.netmap_att["offset_y"] = self.get_new_place_y1(obj_map)
                    self.print_position(obj_map, 'finish y')
                    self.netmap_att["move_up"] = 0


            # move right
            if(self.netmap_att["move_right"] > 0 ):
                if(self.netmap_att["offset_x"] < self.get_new_place_x1(obj_map) - env.MOVE_X):
                    self.netmap_att["offset_x"] += env.MOVE_X
                    self.print_position(obj_map, 'netmap_offset_x')
                else:
                    self.netmap_att["offset_x"] = self.get_new_place_x1(obj_map)
                    self.print_position(obj_map, 'finish x')
                    self.netmap_att["move_right"] = 0


            # move down
            if(self.netmap_att["move_down"] > 0 ):
                if(self.netmap_att["offset_y"] < self.get_new_place_y1(obj_map) - env.MOVE_Y):
                    self.netmap_att["offset_y"] += env.MOVE_Y
                    self.print_position(obj_map, 'netmap_offset_y')
                else:
                    self.netmap_att["offset_y"] = self.get_new_place_y1(obj_map)
                    self.print_position(obj_map, 'finish y')
                    self.netmap_att["move_down"] = 0


            self.print_move_flags()

            if(self.is_netmap_move() == 0):
                self.view_object = 1
                print("view_object:" + str(self.view_object))


        # 弾のリストを作る
        if(
            self.netmap_att["netmap"] < env.HOST and
            self.bullet_init == 1
        ):
            self.bullets = self.generate_bullets()
            self.bullet_init = 0
            #print(len(self.bullets))
            
        # update bullet positions
        for bullet in self.bullets:
            # 進む量
            distance = bullet["state"].distance / 100
            #distance = 1
            p = bullet["state"].get_position(distance)
            position = bullet["state"].update_position(distance)
            
            if pyxel.frame_count < 30:
                if bullet["state"].id < 20:
                    print("[%3d] src x: %3d, y: %3d, get_position x: %f, y: %f" % (bullet["state"].id, position[0], position[1], p[0], p[1]))





    def draw(self):
        pyxel.cls(self.bgcolor)  # reset display color
        for o in self.netmap_att["list_obj_maps"]:
            o[5] = self.bgcolor

        # draw network map object
        # select class A or class B address
        if self.netmap_att["netmap"] == env.WORLDMAP or self.netmap_att["netmap"] == env.CLASS_A or self.netmap_att["netmap"] == env.CLASS_B:
            if self.view_object == 0:
                d.draw_network_address(self.netmap_att)

                if(self.netmap_att["selected_obj"] >= 0):
                    # 1つのオブジェクトのみを表示して中央に移動するアニメーション
                    d.draw_network_object(self.netmap_att, [ self.netmap_att["selected_obj"] ], self.node_status)
                    if(len(self.netmap_att["addr_obj"]) == self.netmap_att["netmap"]):
                        # アドレスオブジェクトの要素数とネットワークマップの深さと同一
                        self.netmap_att["addr_obj"].append(self.netmap_att["selected_obj"])
                else:
                    # 256のオブジェクトを表示するアニメーション
                    d.draw_network_object(self.netmap_att, [], self.node_status)

                # イベントログの描画
                self.draw_netmap_event_log()

                # 地球儀とか弾とか時間とか色々表示する
                self.draw_netmap_and_bullets()

            elif self.view_object == 1:
                # 移動後、中央にオブジェクトを表示するアニメーション
                self.switch_object_center()

            elif self.view_object == 2:
                # オブジェクトを全体に広げるアニメーション
                self.switch_object_wide()

            elif self.view_object == 3:
                # 黒いオブジェクトを全体に広げて次のネットワークマップに切り替える
                if(self.netmap_att["netmap"] == env.WORLDMAP):
                    self.switch_next_netmap(env.CLASS_A)
                elif(self.netmap_att["netmap"] == env.CLASS_A):
                    self.switch_next_netmap(env.CLASS_B)
                elif(self.netmap_att["netmap"] == env.CLASS_B):
                    self.switch_next_netmap(env.CLASS_C)




        # network map class C
        if self.netmap_att["netmap"] == env.CLASS_C and self.view_object == 0:
            d.draw_network_address(self.netmap_att)

            if(self.netmap_att["selected_obj"] >= 0):
                # 1つのオブジェクトのみを表示して中央に移動するアニメーション
                d.draw_network_object(self.netmap_att, [ self.netmap_att["selected_obj"] ], self.node_status )
                if len(self.netmap_att["addr_obj"]) == 3:
                    self.netmap_att["addr_obj"].append(self.netmap_att["selected_obj"])

            else:
                # 256のオブジェクトを表示するアニメーション
                d.draw_network_object(self.netmap_att, [], self.node_status)

            # イベントログの描画
            self.draw_netmap_event_log()

            # 地球儀とか弾とか時間とか色々表示する
            self.draw_netmap_and_bullets()


        elif self.netmap_att["netmap"] == env.CLASS_C and self.view_object == 1:
            # 移動後、中央にオブジェクトを表示するアニメーション
            self.switch_object_center()
        
        elif self.netmap_att["netmap"] == env.CLASS_C and self.view_object == 2:
            # オブジェクトの幅を広げるアニメーション
            self.switch_monolith_grow_h()

        elif self.netmap_att["netmap"] == env.CLASS_C and self.view_object == 3:
            # オブジェクトの高さを広げるアニメーション
            self.switch_monolith_grow_v()

        elif self.netmap_att["netmap"] == env.HOST and self.view_object == 4:
            d.draw_network_address(self.netmap_att)
            xy = self.get_center_object_xy()
            x = xy[0]
            y = xy[1]
            d.draw_wide_object(self.netmap_att["selected_obj"], x, y, self.view_object_scale_x, self.view_object_scale_y, False, self.bgcolor, self.bgcolor, env.DARK_GRAY, env.DARK_GRAY)

            # モノリスのアイコン表示
            # コンフィグを読み込んで定義されていれば優先する
            addr_obj = self.netmap_att["addr_obj"]
            network  = '.'.join(map(str,addr_obj))

            if(network in env.hostdata):
                icontype = env.hostdata[network]["icon"]
                self.icon[icontype].put()
            else:
                icontype = env.hostdata["default"]["icon"]
                self.icon[icontype].put()

            # 右下の時間的な何か
            now = self.get_now()
            d.draw_time(now)

            # モノリスのログ
            d.draw_monolith_log_area()

            # 現在時刻を基準とした前後のログを取得
            logs = self.get_filterd_logs(now, True)

            # ページ数が異常だったらいい感じに修正する
            if(self.page["monolith"] < 0):
                self.page["monolith"] = 0
            elif(self.page["monolith"] >= len(logs)):
                self.page["monolith"] = len(logs) - 1

            if(len(logs) > 0):
                log = logs[self.page["monolith"]]
                keys = ["phase","attack","from","to","note"]
                i=0
                d.draw_monolith_log_time(log, None, env.DARK_BLUE, i)
                i=1
                messages = []
                for k in keys:
                    if(type(log[k]) is dict):
                        for kk in sorted(log[k].keys()):
                            messages.append({"key": kk, "value":log[k][kk]})
                    else:
                        messages.append({"key": k, "value":log[k]})

                for m in messages:
                    margin = env.MONOLITH_TITLE_LENGTH * env.CHAR_WIDTH
                    title = "{0:6}:".format(m["key"])
                    d.draw_monolith_log(title,  env.DARK_BLUE, i)
                    d.draw_monolith_log(str(m["value"]), env.DARK_GRAY, i, margin)
                    i += 1
            
                (nextline_margin, nextline_width) = d.draw_monolith_log_next(self.page["monolith"], len(logs))
                self.monolith_nextline_x1 = env.MONOLITH_X1 + env.MONOLITH_MARGIN_LEFT + nextline_margin
                self.monolith_nextline_y1 = env.MONOLITH_Y2 - env.MONOLITH_MARGIN_TOP - env.CHAR_HEIGHT
                self.monolith_nextline_x2 = env.MONOLITH_X2 - nextline_margin
                self.monolith_nextline_y2 = self.monolith_nextline_y1 + env.CHAR_HEIGHT
            else:
                d.draw_monolith_log("---- event not found ----")
            


            # モノリスを表示している状態のフレームのカウンタ
            self.frame_counter += 1


            if(network in env.hostdata):
                icontype = env.hostdata[network]["action"]
                # 条件が揃ったら、10フレーム後か20フレーム後まで脆弱を表示する
                if icontype == "zeijyaku" and self.frame_counter > 10 and self.frame_counter < 31:
                    self.icon["zeijyaku255"].put()






    def is_netmap_move(self):
        return (self.netmap_att["move_down"] + self.netmap_att["move_up"] + self.netmap_att["move_left"] + self.netmap_att["move_right"])

    def get_new_place_x1(self, obj_map):
        return ((pyxel.width  / 2) - (env.NETMAP_OBJ_WIDTH  / 2) - (env.NETMAP_OBJ_MARGIN_RIGHT / 2) - obj_map[1])

    def get_new_place_y1(self, obj_map):
        return ((pyxel.height / 2) - (env.NETMAP_OBJ_HEIGHT / 2) - (env.NETMAP_OBJ_MARGIN_TOP   / 2) - obj_map[2])

    def get_new_place_x2(self, obj_map):
        return ((pyxel.width  / 2) - (env.NETMAP_OBJ_WIDTH  / 2) - (env.NETMAP_OBJ_MARGIN_RIGHT / 2) - obj_map[3])

    def get_new_place_y2(self, obj_map):
        return ((pyxel.height / 2) - (env.NETMAP_OBJ_HEIGHT / 2) - (env.NETMAP_OBJ_MARGIN_TOP   / 2) - obj_map[4])

    def get_center_object_xy(self):
        return [((pyxel.width / 2) - (env.NETMAP_OBJ_WIDTH  / 2) - (env.NETMAP_OBJ_MARGIN_RIGHT / 2)), 
                ((pyxel.width / 2) - (env.NETMAP_OBJ_HEIGHT / 2) - (env.NETMAP_OBJ_MARGIN_TOP   / 2))]
        # 255 / 2 = 127.5
        # 15 / 2  = 7.5
        # 2  / 2  = 1

    def get_center_xy(self):
        return [(pyxel.width / 2), 
                (pyxel.width / 2)]

    def print_move_flags(self):
        print(
            'flags [' + str(self.netmap_att["move_up"]) + ', ' +
            str(self.netmap_att["move_down"]) + ', ' +
            str(self.netmap_att["move_left"]) + ', ' +
            str(self.netmap_att["move_right"]) + '] up, down, left, right'
        )
        return 1

    def print_position(self, obj_map, note):
        print(
            "[+] " + note + ": " +
            str(obj_map) +
            ", " + str(self.netmap_att["offset_x"]) +
            ", " + str(self.get_new_place_x1(obj_map)) +
            ", " + str(self.netmap_att["offset_y"]) +
            ", " + str(self.get_new_place_y1(obj_map)) )
        return 1

    def netmap_reset(self):    
        self.netmap_att["selected_obj"] = -1
        self.view_object = 0
        self.view_object_scale_x  = 0
        self.view_object_scale_y  = 0
        self.view_object_scale_x2 = 0
        self.view_object_scale_y2 = 0
        self.netmap_att["offset_x"]      = 0
        self.netmap_att["offset_y"]      = 0
        # 弾てきなものを詰め込みなおす
        self.bullet_init = 1


    def switch_object_center(self):
        d.draw_network_address(self.netmap_att)
        xy = self.get_center_object_xy()
        x = xy[0]
        y = xy[1]
        d.draw_object(self.netmap_att["selected_obj"], x, y, True, self.bgcolor)
        self.view_object = 2


    def switch_object_wide(self):
        d.draw_network_address(self.netmap_att)
        xy = self.get_center_object_xy()
        x = xy[0]
        y = xy[1]

        max_width  = pyxel.width  / 2
        max_height = pyxel.height / 2

        if( self.view_object_scale_x < max_width - env.GROW_X ):
            self.view_object_scale_x += env.GROW_X
        else:
            self.view_object_scale_x = max_width
        
        if( self.view_object_scale_y < max_height - env.GROW_Y):
            self.view_object_scale_y += env.GROW_Y
        else:
            self.view_object_scale_y = max_height
        
        if( self.view_object_scale_x == max_width and self.view_object_scale_y == max_height):
            self.view_object = 3
        
        d.draw_wide_object(self.netmap_att["selected_obj"], x, y, self.view_object_scale_x, self.view_object_scale_y, False, self.bgcolor, self.bgcolor)


    def switch_next_netmap(self, next_map):
        xy = self.get_center_xy()
        x  = xy[0]
        y  = xy[1]
        x2 = x
        y2 = y
        #print("[+] x:" + str(x) + ", y:" + str(y))

        max_width  = pyxel.width  / 2
        max_height = pyxel.height / 2

        if( self.view_object_scale_x2 < max_width - env.GROW_X ):
            self.view_object_scale_x2 += env.GROW_X
        else:
            self.view_object_scale_x2 = max_width
        
        if( self.view_object_scale_y2 < max_height - env.GROW_Y):
            self.view_object_scale_y2 += env.GROW_Y
        else:
            self.view_object_scale_y2 = max_height
        
        if x >= 0:
            x  = x - self.view_object_scale_x2
            y  = y - self.view_object_scale_y2
            x2 = x2 + self.view_object_scale_x2
            y2 = y2 + self.view_object_scale_y2

        # 表示領域を制限
        pyxel.clip(x, y, x2, y2)

        d.draw_network_object(self.netmap_att, [])

        d.draw_network_address(self.netmap_att)

        if( self.view_object_scale_x2 == max_width and self.view_object_scale_y2 == max_height):
            self.netmap_att["netmap"] = next_map
            self.netmap_reset()


    def switch_monolith_grow_h(self):
            d.draw_network_address(self.netmap_att)
            xy = self.get_center_object_xy()
            x = xy[0]
            y = xy[1]

            max_width = pyxel.width / 2 * env.MONOLITH_WIDTH

            if( self.view_object_scale_x < max_width - env.GROW_X ):
                self.view_object_scale_x += env.GROW_X
            else:
                self.view_object_scale_x = max_width
                self.view_object = 3
            
            d.draw_wide_object(self.netmap_att["selected_obj"], x, y, self.view_object_scale_x, self.view_object_scale_y, False, self.bgcolor, self.bgcolor)


    def switch_monolith_grow_v(self):
            d.draw_network_address(self.netmap_att)
            xy = self.get_center_object_xy()
            x = xy[0]
            y = xy[1]

            max_height = pyxel.height / 2 * env.MONOLITH_HEIGHT

            if( self.view_object_scale_y < max_height - env.GROW_Y):
                self.view_object_scale_y += env.GROW_Y
            else:
                self.view_object_scale_y = max_height
                self.view_object = 4
                self.netmap_att["netmap"] = env.HOST
            
            d.draw_wide_object(self.netmap_att["selected_obj"], x, y, self.view_object_scale_x, self.view_object_scale_y, False, self.bgcolor, self.bgcolor)



    def draw_netmap_and_bullets(self):
        """
        イベント発生時に色々描画する処理
        """
        # ワールドマップ的なアイコンを表示
        self.icon["world"].put()

        # 弾的なものを描画する
        d.draw_bullets(self.bullets, self.icon)

        # 時間的な何か
        now = self.get_now()
        d.draw_time(now)
        return 1



    def draw_netmap_event_log(self, font_color=env.GREEN, time_color=env.YELLOW):
        # ログエリアっぽい何かを表示
        pyxel.rect(env.LOG_FRAME_X1, env.LOG_FRAME_Y1, env.LOG_FRAME_X2, env.LOG_FRAME_Y2, env.BLACK)

        count_h = int(200 / 8)
        count_v = int(56  / 8)
        icon_width  = 8
        icon_height = 8

        logarea_x = env.NETMAP_BASE_X + 32 + 8 - 4
        self.icon["log1"].pmove_abs(logarea_x, 175)

        for i in range(1, count_h):
            self.icon["loght"].pmove_abs(logarea_x + (i * icon_width), 175)

        self.icon["log2"].pmove_abs(logarea_x + (count_h * icon_width), 175)

        for i in range(1, count_v):
            self.icon["logvl"].pmove_abs(logarea_x, 175 + (i * icon_height))
            self.icon["logvr"].pmove_abs(logarea_x + (count_h * icon_width), 175 + (i * icon_height))

        self.icon["log3"].pmove_abs(logarea_x, 175 + (count_v * icon_height))

        for i in range(1, count_h):
            self.icon["loghb"].pmove_abs(logarea_x + (i * icon_width), 175 + (count_v * icon_height))

        self.icon["log4"].pmove_abs(logarea_x + (count_h * icon_width), 175 + (count_v * icon_height))

        # ログ的なものを描画する
        page_max = math.ceil(len(self.targets) / env.LOG_MAX_LINE)
        #util.logger("draw_log:page_log:" + str(self.page["log"]) + ":page_max: " + str(page_max))
        if(self.page["log"] + 1 > page_max):
            self.page["log"] = 0

        # 時間と継続行サインの表示スペース（2行分）を考慮して-2しておく
        start = (env.LOG_MAX_LINE - 2) * self.page["log"]
        end   = start + env.LOG_MAX_LINE - 2

        if len(self.targets) > 0:
            i = 0
            d.draw_target_log_time(self.targets[0], self.targets[-1], time_color, i)
            i = 1
            for idx in range(len(self.targets)):
                if(idx >= start and idx < end):
                    d.draw_target_log(self.targets[idx], "", font_color, i)
                    i += 1
                if(idx >= end):
                    break
            if(self.page["log"] + 1 < page_max):
                d.draw_target_log_next(time_color, i)
        else:
            d.draw_target_log("---- event not found ----")
        #print("log_count: %d" %(len(self.targets)))
        return 1



    def generate_bullets(self):
        """
        職人が弾を丹念に込めて弾のリストを返す
        """
        #util.logger("generate_bullets: in")
        list_obj_maps   = self.netmap_att["list_obj_maps"]
        netmap          = self.netmap_att["netmap"]
        netmap_addr_obj = self.netmap_att["addr_obj"]

        bullets = []
        for t in self.targets:
            if t["draw"]:
                util.logger("generate_bullets:target:" + json.dumps(t) )
                to_addr = t["to"].split(".")
                to_addr = list(map(int, to_addr))
                correct = True
                util.logger("generate_bullets:target:" + json.dumps(to_addr))
                util.logger("generate_bullets:target:" + json.dumps(netmap_addr_obj))
                for idx in range(netmap):
                    # 現在のネットワークマップの階層からtargetが表示対象か確認する
                    if(to_addr[idx] != netmap_addr_obj[idx]):
                        correct = False

                if(correct):
                    # 現在マップに表示する必要がある
                    target_obj = to_addr[netmap]
                    src_xy     = self.icon["world"].get_center_position()
                    obj_map    = list_obj_maps[target_obj]
                    dst_xy     = [obj_map[1] + (env.NETMAP_OBJ_WIDTH / 2), obj_map[2] + (env.NETMAP_OBJ_HEIGHT / 2)]
                    astate     = actor_state.ActorState(src_xy[0], src_xy[1], dst_xy[0], dst_xy[1], target_obj, obj_map)

                    if(self.re_discover.match(t["phase"])):
                        bullets.append({ "icon": self.icon["search"], "state": astate, "line_color": env.YELLOW })
                    elif(self.re_attack.match(t["phase"])):
                        bullets.append({ "icon": self.icon["arrow"],  "state": astate, "line_color": env.RED })

                # for debug
                if pyxel.frame_count < 2:
                    print("[%3d] src x: %3d, y: %3d,  dst x: %3d, y: %3d, distance: %f, degree: %f" % (target_obj, src_xy[0], src_xy[1], dst_xy[0], dst_xy[1], astate.distance, astate.degree))
                    p = astate.get_position(astate.distance)
                    print("[%3d] get_position x: %f, y: %f" % ( target_obj, p[0], p[1]))
                    print("")

        #uril.logger("generate_bullets: out")
        return bullets


    def get_filterd_logs(self, now, reverse_on):
        to_addr      = ".".join(map(str,self.netmap_att["addr_obj"]))
        logs         = []
        filterd_logs = []
        for log in self.log:
            #util.logger("filterd_logs:" +log)
            if(log["to"] == to_addr):
                logs.append(log)
                #util.logger("filterd_logs:" + json.dumps(log))
        for log in logs:
            if(
                log["time"] <= now + env.VISUALIZE_TIME_RANGE
            ):
                filterd_logs.append(log)
                #util.logger("logs:" + json.dumps(log))
            elif(log["time"] > now + env.VISUALIZE_TIME_RANGE):
                break
        if(reverse_on == True):
            filterd_logs = sorted(filterd_logs, key=lambda x: x["time"], reverse=True)
        return filterd_logs


    def get_now(self):
        return self.time_begin + self.passed_seconds

    def reset_params(self):
        self.netmap_att["netmap"]        = 0
        self.netmap_att["selected_obj"]  = -1
        self.netmap_att["addr_obj"]      = []
        self.netmap_att["offset_x"]      = 0
        self.netmap_att["offset_y"]      = 0
        self.netmap_att["move_up"]       = 0
        self.netmap_att["move_down"]     = 0
        self.netmap_att["move_right"]    = 0
        self.netmap_att["move_left"]     = 0
        self.view_object                 = 0
        self.view_object_scale           = 0
        self.view_object_scale_x         = 0
        self.view_object_scale_y         = 0
        self.view_object_scale_x2        = 0
        self.view_object_scale_y2        = 0
        self.frame_counter               = 0
        self.bullet_init                 = 1
        self.monolith_nextline_x1        = 0
        self.monolith_nextline_y1        = 0
        self.monolith_nextline_x2        = 0
        self.monolith_nextline_y2        = 0
        self.page = {
            "log"     : 0,
            "monolith": 0
        }
        return True

App()
