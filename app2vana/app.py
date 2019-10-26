#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import math
import time
import datetime
import codecs
import random
import re
import json
import pyxel
import configparser

import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from app2vana.util import Utility
from app2vana.modules.Hachi_Actor import Actor


# Type of printing.
OK = 'ok'         # [*]
NOTE = 'note'     # [+]
FAIL = 'fail'     # [-]
WARNING = 'warn'  # [!]
NONE = 'none'     # No label.

# Display setting value.
WINDOW_WIDTH = 255
WINDOW_HEIGHT = 255
TM_WIDTH = 100
TM_HEIGHT = 100
MONOLITH_SIZE = 100


# Display banner.
def show_banner(utility):
    banner = """
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
 █████╗  ██╗   ██╗ █████╗ ███╗   ██╗ █████╗ 
██╔══██╗ ██║   ██║██╔══██╗████╗  ██║██╔══██╗
╚█████╔╝ ██║   ██║███████║██╔██╗ ██║███████║
██╔══██╗ ╚██╗ ██╔╝██╔══██║██║╚██╗██║██╔══██║
╚█████╔╝  ╚████╔╝ ██║  ██║██║ ╚████║██║  ██║
 ╚════╝    ╚═══╝  ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝  (beta)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
""" + 'by ' + os.path.basename(__file__)
    utility.print_message(NONE, banner)
    show_credit(utility)
    time.sleep(utility.banner_delay)


# Show credit.
def show_credit(utility):
    credit = u"""
       =[ 8vana v0.0.1-beta                               ]=
+ -- --=[ Author  : Gyoiler (@gyoithon)                   ]=--
+ -- --=[ Website : https://github.com/gyoisamurai/8vana/ ]=--
    """
    utility.print_message(NONE, credit)


# Bullet class.
class Bullet:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.speed = 5
        self.degree = 0
        self.target_idx = 0
        self.target_range_x = [0, 0]
        self.target_range_y = [0, 0]
        self.status = 'normal'

    def update(self, x, y, status='normal'):
        self.x = x
        self.y = y
        self.status = status


# Laser class.
class Laser:
    def __init__(self):
        self.target_idx = 0
        self.attacker_x = 0
        self.attacker_y = 0
        self.target_x = 0
        self.target_y = 0
        self.origin_framecount = 0
        self.wait_framecount = 0


# Monolith class.
class Monolith:
    def __init__(self):
        self.target_type = ''
        self.target_id = ''
        self.disp_hostname = ''
        self.disp_color = 0
        self.info_color = 0
        self.max_size_x1 = 0
        self.max_size_x2 = 0
        self.max_size_y1 = 0
        self.max_size_y2 = 0
        self.x1 = 0
        self.x2 = 0
        self.y1 = 0
        self.y2 = 0
        self.max_page = 0
        self.page_count = 1

    def update(self, x1=0, x2=0, y1=0, y2=0, max_page=0, page=0):
        self.x1 += x1
        self.x2 += x2
        self.y1 += y1
        self.y2 += y2
        self.max_page = max_page
        self.page_count += page


# Display monitor class.
class DisplayText:
    def __init__(self):
        self.x = 10
        self.y = [218, 226, 234, 242]
        self.message = []
        self.msg_color = []

    def push(self, new_msg, msg_color):
        if len(self.message) != 4:
            self.message.append(new_msg)
            self.msg_color.append(msg_color)
        else:
            self.message.pop(0)
            self.msg_color.pop(0)
            self.message.append(new_msg)
            self.msg_color.append(msg_color)


# Main class.
class App2vana:
    def __init__(self, utility):
        self.utility = utility
        self.file_name = os.path.basename(__file__)
        self.full_path = os.path.dirname(os.path.abspath(__file__))
        self.root_path = os.path.join(self.full_path, '..')

        # Read config.ini.
        config = configparser.ConfigParser()
        config.read(os.path.join(self.full_path, 'config.ini'), encoding='utf-8')
        self.mode_name = config['Common']['mode_name']
        self.asset_dir = os.path.join(self.full_path, config['Common']['asset_path'])
        self.resource_file = os.path.join(self.asset_dir, config['Common']['resource_file'])

        # Read settings of Attacker.
        self.attackers = config['Attacker']['attackers'].split('@')
        if len(self.attackers) >= 5:
            self.utility.print_message(WARNING, 'Too many attackers. Clipped : {} -> {}'.format(len(self.attackers), 4))
            self.attackers = self.attackers[0:4]
        self.Attacker = []
        self.attacker_action_flag = False

        # Read settings of Targets.
        self.targets = config['Target']['targets'].split('@')
        if len(self.targets) >= 13:
            self.utility.print_message(WARNING, 'Too many targets. Clipped : {} -> {}'.format(len(self.targets), 8))
            self.targets = self.targets[0:8]
        self.Target = []
        self.wreck_regex = config['Target']['wreck_str']

        # Read setting of inputting log.
        self.watch_period = int(config['LogParser']['watch_period'])
        if self.watch_period < 1:
            self.utility.print_message(WARNING, 'Watching period is exchanged {}s -> 1s.'.format(str(self.watch_period)))
            self.watch_period = 1
        converted_log_dir = os.path.join(self.root_path, config['LogParser']['converted_log_path'])
        self.converted_log_path = os.path.join(converted_log_dir, config['LogParser']['converted_log_file'])
        self.read_start_byte = 0
        self.last_log_loading_time = 0

        # Create Display Text instance.
        self.DisplayText = DisplayText()
        self.DisplayText.push('Game Start!!', self.utility.color_7)

        # Create window.
        pyxel.init(WINDOW_WIDTH, WINDOW_HEIGHT, caption=self.mode_name, fps=self.utility.fps, scale=0)

        # Calculate center of window.
        self.win_center_x = int(WINDOW_WIDTH / 2)
        self.win_center_y = int(WINDOW_HEIGHT / 2)

        # Mouse cursor.
        pyxel.mouse(True)

        # Monolith.
        self.isMonolith = False
        self.Monolith = []
        self.monolith_size = MONOLITH_SIZE

        # Load resource file.
        pyxel.load(self.resource_file)
        self.tilemap = pyxel.tilemap(0)

        # Define tile map settings.
        self.tm_x = 0
        self.tm_y = 0
        self.tm_u = 0
        self.tm_v = 0
        self.tm_w = TM_WIDTH
        self.tm_h = TM_HEIGHT
        self.tm_color_key = 0

        # Create instance.
        self.create_instance()
        self.Bullet = []
        self.Laser = []

        # Get timestamp.
        self.timestamp = time.mktime(datetime.datetime.now().utctimetuple())
        self.read_start_byte = 0

        # Run.
        pyxel.run(self.update, self.draw)

    # Define height of attacker and target.
    def initialize_height(self, target_list, type):
        height = 0
        if type == 'attacker':
            if len(target_list) == 1:
                height = 112
            elif len(target_list) == 2 or len(target_list) == 3:
                height = 78
            elif len(target_list) >= 4:
                height = 60
        else:
            if len(target_list) == 1:
                height = 107
            elif len(target_list) == 2 or len(target_list) == 3:
                height = 73
            elif len(target_list) >= 4:
                height = 55
        return height

    # Create detail information.
    def create_detail_info(self, event_info):
        max_msg_w = 45
        max_msg_h = 16
        disp_info = []
        disp_page = []

        # Write event.
        for event in event_info:
            disp_info.append('{}'.format(event)[:max_msg_w])

        # Create page.
        page = []
        for idx, message in enumerate(disp_info):
            page.append(message)
            if len(page) == max_msg_h:
                disp_page.append(page)
                page = []
        disp_page.append(page)

        return disp_page

    # Create instance that attacker and target.
    def create_instance(self):
        # Set parameter to attacker instance.
        target_width = 210
        target_v = 72
        height = self.initialize_height(self.attackers, 'attacker')
        for idx, hostname in enumerate(self.attackers):
            # Create attacker instance.
            attacker = Actor(self.utility)
            attacker.hostname = hostname
            attacker.x = target_width
            attacker.y = height
            attacker.u = 0
            attacker.v = target_v
            attacker.w = 32
            attacker.h = 24
            attacker.center_x = int((target_width + target_width + attacker.w) / 2)
            attacker.center_y = int((height + height + attacker.h) / 2)
            attacker.shot_x = target_width
            attacker.shot_y = attacker.center_y
            attacker.text_x = target_width - 5
            attacker.text_y = height + 24
            attacker.text_color = self.utility.color_7
            self.Attacker.append(attacker)

            # Adjust coordinate (width and height).
            if len(self.attackers) == 2:
                height += 70
                target_v += 24
            elif len(self.attackers) == 3:
                height += 35
                target_v += 24
            elif len(self.attackers) == 4:
                height += 35
                target_v += 24

        # Set parameter to target instance.
        target_width = 20
        adjust_width = 65
        height = self.initialize_height(self.targets, 'target')
        for idx, hostname in enumerate(self.targets):
            # Create target instance.
            target = Actor(self.utility)
            target.hostname = hostname
            target.x = target_width
            target.y = height
            target.u = 0
            target.v = 176
            target.w = 32
            target.h = 32
            target.center_x = int((target_width + target_width + target.w) / 2)
            target.center_y = int((height + height + target.h) / 2)
            target.shot_x = target_width + target.w
            target.shot_y = target.center_y
            target.text_x = target_width - 15
            target.text_y = height + 30
            target.text_color = self.utility.color_7
            self.Target.append(target)

            # Adjust coordinate (width and height).
            if len(self.targets) == 2:
                height += 70
            elif len(self.targets) == 3:
                height += 35
            elif len(self.targets) == 4:
                height += 35
            # Row 2.
            elif len(self.targets) == 5:
                if idx < 4:
                    height += 35

                # Initialize width and height.
                if idx == 3:
                    height = 107
                    target_width += adjust_width
            elif len(self.targets) == 6:
                if idx < 4:
                    height += 35

                # Initialize width and height.
                if idx == 3:
                    height = 73
                    target_width += adjust_width
                elif idx >= 4:
                    height += 70
            elif len(self.targets) == 7:
                if idx < 4:
                    height += 35

                # Initialize width and height.
                if idx == 3:
                    height = 73
                    target_width += adjust_width
                elif idx >= 4:
                    height += 35
            elif len(self.targets) == 8:
                if idx < 4:
                    height += 35

                # Initialize width and height.
                if idx == 3:
                    height = 55
                    target_width += adjust_width
                elif idx >= 4:
                    height += 35
            # Row 3.
            elif len(self.targets) == 9:
                if idx < 4:
                    height += 35

                # Initialize width and height.
                if idx == 3 or idx == 7:
                    height = 107
                    target_width += adjust_width
            elif len(self.targets) == 10:
                if idx < 4:
                    height += 35

                # Initialize width and height.
                if idx == 3 or idx == 7:
                    height = 73
                    target_width += adjust_width
                elif idx >= 4:
                    height += 70
            elif len(self.targets) == 11:
                if idx < 4:
                    height += 35

                # Initialize width and height.
                if idx == 3 or idx == 7:
                    height = 73
                    target_width += adjust_width
                elif idx >= 4:
                    height += 35
            elif len(self.targets) == 12:
                if idx < 4:
                    height += 35

                # Initialize width and height.
                if idx == 3 or idx == 7:
                    height = 55
                    target_width += adjust_width
                elif idx >= 4:
                    height += 35

    # Draw tile map.
    def draw_tilemap(self):
        # Draw background.
        pyxel.bltm(self.tm_x,
                   self.tm_y,
                   self.utility.tm_id_0,
                   self.tm_u,
                   self.tm_v,
                   self.tm_w,
                   self.tm_h,
                   self.tm_color_key)

    # Draw attackers.
    def draw_attackers(self):
        # Arrange attackers.
        for idx, hostname in enumerate(self.attackers):
            # Draw attackers.
            text_color = self.utility.color_7
            if self.Target[idx].status == 'exploit':
                text_color = self.utility.color_10
            elif self.Target[idx].status == 'down':
                text_color = self.utility.color_8
            pyxel.blt(self.Attacker[idx].x,
                      self.Attacker[idx].y,
                      self.utility.image_id_0,
                      self.Attacker[idx].u,
                      self.Attacker[idx].v,
                      self.Attacker[idx].w,
                      self.Attacker[idx].h,
                      self.utility.color_0)
            pyxel.text(self.Attacker[idx].text_x,
                       self.Attacker[idx].text_y,
                       hostname,
                       self.Attacker[idx].text_color)

    # Draw targets.
    def draw_targets(self):
        # Arrange targets.
        for idx, hostname in enumerate(self.targets):
            # Draw targets.
            pyxel.blt(self.Target[idx].x,
                      self.Target[idx].y,
                      self.utility.image_id_0,
                      self.Target[idx].u,
                      self.Target[idx].v,
                      -self.Target[idx].w,
                      self.Target[idx].h,
                      self.utility.color_0)
            pyxel.text(self.Target[idx].x - 15,
                       self.Target[idx].y + 30,
                       self.Target[idx].hostname,
                       self.Target[idx].text_color)

    # Draw bullets.
    def draw_bullets(self):
        for bullet in self.Bullet:
            # Bullet's animation (rolling).
            if pyxel.frame_count % 4 == 0:
                pyxel.blt(bullet.x, bullet.y, self.utility.image_id_0, 0, 168, 7, 7, self.utility.color_0)
            elif pyxel.frame_count % 4 == 1:
                pyxel.blt(bullet.x, bullet.y, self.utility.image_id_0, 8, 168, 7, 7, self.utility.color_0)
            elif pyxel.frame_count % 4 == 2:
                pyxel.blt(bullet.x, bullet.y, self.utility.image_id_0, 16, 168, 7, 7, self.utility.color_0)
            elif pyxel.frame_count % 4 == 3:
                pyxel.blt(bullet.x, bullet.y, self.utility.image_id_0, 8, 168, 7, 7, self.utility.color_0)

    # Draw lasers.
    def draw_lasers(self):
        for laser in self.Laser:
            # Laser's animation (change color).
            pyxel.circ(laser.target_x, laser.target_y, 3, self.utility.color_7)
            if pyxel.frame_count % 4 == 0:
                pyxel.line(laser.attacker_x, laser.attacker_y, laser.target_x, laser.target_y, self.utility.color_7)
            if pyxel.frame_count % 4 == 1:
                pyxel.line(laser.attacker_x, laser.attacker_y, laser.target_x, laser.target_y, self.utility.color_10)
            if pyxel.frame_count % 4 == 2:
                pyxel.line(laser.attacker_x, laser.attacker_y, laser.target_x, laser.target_y, self.utility.color_9)
            if pyxel.frame_count % 4 == 3:
                pyxel.line(laser.attacker_x, laser.attacker_y, laser.target_x, laser.target_y, self.utility.color_8)

    # Draw explosion.
    def draw_target_effect(self):
        for target in self.Target:
            # Probe.
            if target.status == self.utility.status_attack_probe:
                pyxel.blt(target.x, target.y, self.utility.image_id_0, 64, 176, target.w, target.h,
                          self.utility.color_0)
            # Shoot.
            elif target.status == self.utility.status_attack_main:
                pyxel.blt(target.x, target.y, self.utility.image_id_0, 32, 176, target.w, target.h,
                          self.utility.color_0)
            # Machine gun.
            elif target.status == self.utility.status_attack_sub:
                pyxel.blt(target.x, target.y, self.utility.image_id_0, 96, 176, target.w, target.h,
                          self.utility.color_0)

    # Draw monolith.
    def draw_monolith(self):
        for monolith in self.Monolith:
            # Monolith's animation (extend).
            pyxel.rect(monolith.x1, monolith.y1, monolith.x2, monolith.y2, monolith.disp_color)

            # Draw detail information (already extend).
            if monolith.x1 <= monolith.max_size_x1:
                pyxel.rectb(monolith.max_size_x1 + 5, monolith.max_size_y1 + 10,
                            monolith.max_size_x2 - 5, monolith.max_size_y2, self.utility.color_7)

                # Extract message from Target or Attacker.
                message = []
                if monolith.target_type == 'Target':
                    message = self.create_detail_info(self.Target[monolith.target_id].event_info)
                else:
                    message = self.create_detail_info(self.Attacker[monolith.target_id].event_info)

                # Write message.
                monolith.update(max_page=len(message))
                # Write title.
                msg = '{} Information.  [{}/{}]'.format(monolith.disp_hostname, monolith.page_count, monolith.max_page)
                pyxel.text(monolith.x1 + 10, monolith.y1 + 4, msg, pyxel.frame_count % 15)

                if monolith.max_page != 0:
                    for idx, msg_line in enumerate(message[monolith.page_count - 1]):
                        pyxel.text(monolith.x1 + 12, monolith.y1 + 17 + (idx * 8), msg_line, monolith.info_color)

    # Draw mouse pointer.
    def draw_mouse_pointer(self):
        pyxel.blt(pyxel.mouse_x, pyxel.mouse_y, self.utility.image_id_0, 32, 208, 8, 8, self.utility.color_0)

    # Draw text of status.
    def draw_status_text(self):
        idx = 0
        for msg, msg_color in zip(self.DisplayText.message, self.DisplayText.msg_color):
            pyxel.text(self.DisplayText.x, self.DisplayText.y[idx], msg, msg_color)
            idx += 1

    # Draw scene.
    def draw(self):
        # Draw background color (0=black).
        pyxel.cls(self.utility.color_0)

        # Draw text.
        self.draw_status_text()

        # Draw attackers.
        self.draw_attackers()

        # Draw targets.
        self.draw_targets()

        # Draw bullets.
        self.draw_bullets()

        # Draw lasers.
        self.draw_lasers()

        # Draw explosion.
        self.draw_target_effect()

        # Draw mouse pointer.
        self.draw_mouse_pointer()

        # Draw monolith.
        self.draw_monolith()

        # Draw tile map.
        self.draw_tilemap()

    # Check the object that is indicated by mouse cursor.
    def check_indicate_object(self, mouse_cursor):
        # Check attacker.
        for attacker_id, attacker in enumerate(self.Attacker):
            if attacker.x < mouse_cursor[0] < attacker.x + attacker.w and \
                    attacker.y < mouse_cursor[1] < attacker.y + attacker.h:
                return attacker_id, 'Attacker'

        # Check target.
        for target_id, target in enumerate(self.Target):
            if target.x < mouse_cursor[0] < target.x + target.w and target.y < mouse_cursor[1] < target.y + target.h:
                return target_id, 'Target'
        return -1, None

    # Get object (attacker, target) index.
    def get_object_index(self, target_list, obj_name):
        get_index = None
        for idx, target_name in enumerate(target_list):
            if target_name == obj_name:
                get_index = idx
                break
        return get_index

    # Monitor log files.
    def watch(self, read_start_byte):
        # Check updated date of target log.
        if os.path.exists(self.converted_log_path):
            # Read log.
            with codecs.open(self.converted_log_path, mode='r', encoding='utf-8') as fin:
                fin.seek(read_start_byte)
                raw_content = fin.read()
                if raw_content == '':
                    return []
                elif raw_content.startswith(','):
                    raw_content = raw_content[:0] + '[' + raw_content[1:]
                self.read_start_byte += len(raw_content)
                content = json.loads(raw_content)
            return content
        else:
            return []

    # Update drawing.
    def update(self):
        # Quit.
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        # Control monolith.
        if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON) and self.isMonolith is False:
            new_monolith = Monolith()
            checked_id, checked_type = self.check_indicate_object([pyxel.mouse_x, pyxel.mouse_y])

            # Create Monolith of target.
            if checked_id != -1 and checked_type == 'Target':
                self.isMonolith = True
                new_monolith.target_type = checked_type
                new_monolith.target_id = checked_id
                new_monolith.disp_hostname = self.Target[checked_id].hostname
                new_monolith.disp_color = self.utility.color_1
                new_monolith.info_color = self.utility.color_7
                new_monolith.max_size_x1 = self.win_center_x - self.monolith_size
                new_monolith.max_size_x2 = self.win_center_x + self.monolith_size
                new_monolith.max_size_y1 = self.win_center_y - self.monolith_size + 30
                new_monolith.max_size_y2 = self.win_center_y + self.monolith_size - 25
                new_monolith.x1 = self.win_center_x
                new_monolith.x2 = self.win_center_x
                new_monolith.y1 = self.win_center_y
                new_monolith.y2 = self.win_center_y
                self.Monolith.append(new_monolith)

            # Create Monolith of attacker.
            if checked_id != -1 and checked_type == 'Attacker':
                self.isMonolith = True
                new_monolith.target_type = checked_type
                new_monolith.target_id = checked_id
                new_monolith.disp_hostname = self.Attacker[checked_id].hostname
                new_monolith.disp_color = self.utility.color_5
                new_monolith.info_color = self.utility.color_7
                new_monolith.max_size_x1 = self.win_center_x - self.monolith_size
                new_monolith.max_size_x2 = self.win_center_x + self.monolith_size
                new_monolith.max_size_y1 = self.win_center_y - self.monolith_size + 30
                new_monolith.max_size_y2 = self.win_center_y + self.monolith_size - 25
                new_monolith.x1 = self.win_center_x
                new_monolith.x2 = self.win_center_x
                new_monolith.y1 = self.win_center_y
                new_monolith.y2 = self.win_center_y
                self.Monolith.append(new_monolith)

        # Control Actor's action.
        log_contents = ''
        if pyxel.frame_count % self.utility.wait_framecount(self.watch_period) == 0:
            log_contents = self.watch(self.read_start_byte)

            # Get event information.
            for log_info in log_contents:
                # Select target.
                t_idx = self.get_object_index(self.targets, log_info['to'])
                if t_idx is None:
                    continue
                if len(log_info['note']['CVE']) != 0:
                    date_obj = self.utility.transform_epoch_object(float(log_info['time']))
                    log_time = self.utility.transform_date_string(date_obj, '%Y%m%d%H%M%S')
                    self.Target[t_idx].event_info.insert(0, log_time + ':' + log_info['note']['option'])
                    self.Target[t_idx].corruption_flag = True
                    if re.search(self.wreck_regex, log_info['note']['option']) is not None:
                        self.Target[t_idx].wreck_flag = True

            # Decide Actor's action using log.
            for log_info in log_contents:
                # Select attacker and target.
                a_idx = self.get_object_index(self.attackers, log_info['from'])
                t_idx = self.get_object_index(self.targets, log_info['to'])
                if a_idx is None or t_idx is None:
                    continue

                # Calculate degree from attacker to target.
                x = self.Attacker[a_idx].center_x - self.Target[t_idx].center_x
                y = self.Attacker[a_idx].center_y - self.Target[t_idx].center_y
                degree = math.degrees(math.atan2(y, x))

                # Attacker's attacking animation.
                self.Attacker[a_idx].origin_framecount = pyxel.frame_count
                action_idx = 0
                if log_info['phase'] == 'Attack':
                    action_idx = random.randint(0, 2)
                else:
                    action_idx = 3

                # Make message.
                msg = '{} executes {} to Dest={}'.format(log_info['from'],
                                                          log_info['attack'],
                                                          log_info['to'])
                self.DisplayText.push(msg, self.utility.color_7)
                if len(log_info['note']['CVE']) != 0:
                    msg = log_info['note']['option']
                    self.DisplayText.push(msg, self.utility.color_10)

                # Check attacker's action flag.
                if self.attacker_action_flag:
                    break

                # Shoot bullet.
                if action_idx == 0:
                    # Attacker's action flag on.
                    self.attacker_action_flag = True

                    wait_framecount = 0.5
                    self.Attacker[a_idx].wait_framecount = wait_framecount
                    self.Attacker[a_idx].update(x=-8, u=40, w=8,
                                                status=self.utility.status_attack_main,
                                                text_color=self.utility.color_10)

                    # Set target information to bullet instance.
                    new_bullet = Bullet()
                    new_bullet.degree = degree
                    new_bullet.target_idx = t_idx
                    new_bullet.target_range_x[0] = self.Target[t_idx].x
                    new_bullet.target_range_x[1] = self.Target[t_idx].x + self.Target[t_idx].w
                    new_bullet.target_range_y[0] = self.Target[t_idx].y
                    new_bullet.target_range_y[1] = self.Target[t_idx].y + self.Target[t_idx].h
                    new_bullet.update(self.Attacker[a_idx].shot_x - 6, self.Attacker[a_idx].shot_y - 8)
                    self.Bullet.append(new_bullet)
                # Shoot laser.
                elif action_idx == 1:
                    # Attacker's action flag on.
                    self.attacker_action_flag = True

                    wait_framecount = 1.0
                    self.Attacker[a_idx].wait_framecount = wait_framecount
                    self.Attacker[a_idx].update(u=168,
                                                status=self.utility.status_attack_se,
                                                text_color=self.utility.color_14)
                    self.Target[t_idx].origin_framecount = pyxel.frame_count
                    self.Target[t_idx].wait_framecount = wait_framecount
                    self.Target[t_idx].update(status=self.utility.status_attack_se,
                                              text_color=self.utility.color_14)

                    # Set target information to laser instance.
                    new_laser = Laser()
                    new_laser.attacker_x = self.Attacker[a_idx].shot_x + 5
                    new_laser.attacker_y = self.Attacker[a_idx].shot_y - 10
                    new_laser.target_idx = t_idx
                    new_laser.target_x = self.Target[t_idx].center_x
                    new_laser.target_y = self.Target[t_idx].center_y
                    new_laser.origin_framecount = self.Target[t_idx].origin_framecount
                    new_laser.wait_framecount = wait_framecount
                    self.Laser.append(new_laser)
                # Shoot machine gun.
                elif action_idx == 2:
                    # Attacker's action flag on.
                    self.attacker_action_flag = True

                    wait_framecount = 0.5
                    self.Attacker[a_idx].wait_framecount = wait_framecount
                    self.Attacker[a_idx].update(u=88,
                                                status=self.utility.status_attack_sub,
                                                text_color=self.utility.color_11)
                    self.Target[t_idx].origin_framecount = pyxel.frame_count
                    self.Target[t_idx].wait_framecount = wait_framecount
                    self.Target[t_idx].update(status=self.utility.status_attack_sub,
                                              text_color=self.utility.color_10)
                # Execute probe.
                elif action_idx == 3:
                    # Attacker's action flag on.
                    self.attacker_action_flag = True

                    wait_framecount = 1.5
                    self.Attacker[a_idx].wait_framecount = wait_framecount
                    self.Attacker[a_idx].update(u=128,
                                                status=self.utility.status_attack_probe,
                                                text_color=self.utility.color_12)
                    self.Target[t_idx].origin_framecount = pyxel.frame_count
                    self.Target[t_idx].wait_framecount = wait_framecount
                    self.Target[t_idx].update(status=self.utility.status_attack_probe,
                                              text_color=self.utility.color_10)

        # Bullet animation.
        bullet_count = len(self.Bullet)
        for idx in range(bullet_count):
            try:
                dx = self.Bullet[idx].x - math.cos(math.radians(self.Bullet[idx].degree)) * self.Bullet[idx].speed
                dy = self.Bullet[idx].y - math.sin(math.radians(self.Bullet[idx].degree)) * self.Bullet[idx].speed

                # Check window range.
                if 0 < self.Bullet[idx].x < 255:
                    self.Bullet[idx].update(dx, dy)
                else:
                    del self.Bullet[idx]

                # Check collision.
                if self.Bullet[idx].target_range_x[0] <= self.Bullet[idx].x <= self.Bullet[idx].target_range_x[1] and \
                        self.Bullet[idx].target_range_y[0] <= self.Bullet[idx].y <= self.Bullet[idx].target_range_y[1]:
                    # Target's animation.
                    self.Target[self.Bullet[idx].target_idx].origin_framecount = pyxel.frame_count
                    self.Target[self.Bullet[idx].target_idx].wait_framecount = 0.5
                    self.Target[self.Bullet[idx].target_idx].update(x=-1,
                                                                    status=self.utility.status_attack_main,
                                                                    text_color=self.utility.color_8)
                    self.Bullet[idx].update(dx, dy, self.utility.status_attack_main)
                    del self.Bullet[idx]
            except Exception as e:
                self.utility.print_exception(e, 'Bullet animation is failure.')
                continue

        # Monolith animation.
        monolith_count = len(self.Monolith)
        for idx in range(monolith_count):
            # Update size of monolith.
            if self.Monolith[idx].max_size_x1 <= self.Monolith[idx].x1:
                self.Monolith[idx].update(x1=-3)
            if self.Monolith[idx].max_size_x2 >= self.Monolith[idx].x2:
                self.Monolith[idx].update(x2=3)
            if self.Monolith[idx].max_size_y1 <= self.Monolith[idx].y1:
                self.Monolith[idx].update(y1=-3)
            if self.Monolith[idx].max_size_y2 >= self.Monolith[idx].y2:
                self.Monolith[idx].update(y2=3)

            # Sending Monolith's page.
            if self.isMonolith:
                if self.Monolith[idx].max_page > self.Monolith[idx].page_count and pyxel.btnp(pyxel.KEY_S):
                    self.Monolith[idx].update(page=1)
                if self.Monolith[idx].page_count > 1 and pyxel.btnp(pyxel.KEY_A):
                    self.Monolith[idx].update(page=-1)

            # Discard the monolith.
            if self.isMonolith and pyxel.btnp(pyxel.KEY_BACKSPACE):
                del self.Monolith[idx]
                self.isMonolith = False

        # Laser animation.
        laser_count = len(self.Laser)
        try:
            for idx in range(laser_count):
                drawing_fc = self.Laser[idx].origin_framecount + self.utility.wait_framecount(self.Laser[idx].wait_framecount)
                if drawing_fc < pyxel.frame_count:
                    del self.Laser[idx]
        except Exception as e:
            print('{}'.format(e.args))

        # Reset animation for Attackers.
        for attacker in self.Attacker:
            drawing_fc = attacker.origin_framecount + self.utility.wait_framecount(attacker.wait_framecount)
            if drawing_fc < pyxel.frame_count:
                if attacker.status == self.utility.status_attack_main:
                    attacker.update(x=8, u=0, w=-8,
                                    status=self.utility.status_normal,
                                    text_color=self.utility.color_7)
                elif attacker.status == self.utility.status_attack_sub:
                    attacker.update(u=0,
                                    status=self.utility.status_normal,
                                    text_color=self.utility.color_7)
                elif attacker.status == self.utility.status_attack_probe:
                    attacker.update(u=0,
                                    status=self.utility.status_normal,
                                    text_color=self.utility.color_7)
                elif attacker.status == self.utility.status_attack_se:
                    attacker.update(u=0,
                                    status=self.utility.status_normal,
                                    text_color=self.utility.color_7)
                attacker.origin_framecount = 0
                attacker.wait_framecount = 0.0

                # Attacker's action flag off.
                self.attacker_action_flag = False

        # Reset animation for Targets.
        for target in self.Target:
            drawing_fc = target.origin_framecount + self.utility.wait_framecount(target.wait_framecount)
            if drawing_fc < pyxel.frame_count:
                # Shoot bullet.
                if target.status == self.utility.status_attack_main:
                    target.update(x=1, status=self.utility.status_normal, text_color=self.utility.color_7)
                    # msg = 'The {} is critically damaged.'.format(target.hostname)
                    # self.DisplayText.push(msg, self.utility.color_10)
                # Shoot laser.
                elif target.status == self.utility.status_attack_se:
                    target.update(status=self.utility.status_normal, text_color=self.utility.color_7)
                    # msg = 'The {} is seriously damaged.'.format(target.hostname)
                    # self.DisplayText.push(msg, self.utility.color_14)
                # Shoot machine gun.
                elif target.status == self.utility.status_attack_sub:
                    target.update(status=self.utility.status_normal, text_color=self.utility.color_7)
                    # msg = 'The {} is slightly damaged.'.format(target.hostname)
                    # self.DisplayText.push(msg, self.utility.color_11)
                # Probe.
                elif target.status == self.utility.status_attack_probe:
                    target.update(status=self.utility.status_normal, text_color=self.utility.color_7)
                    # msg = 'The {} is being investigated.'.format(target.hostname)
                    # self.DisplayText.push(msg, self.utility.color_12)
                target.origin_framecount = 0
                target.wait_framecount = 0.0


# main.
if __name__ == '__main__':
    file_name = os.path.basename(__file__)
    full_path = os.path.dirname(os.path.abspath(__file__))

    utility = Utility()
    utility.write_log(20, '[In] 8Vana [{}].'.format(file_name))

    # Start application
    App2vana(utility)

    print(os.path.basename(__file__) + ' finish!!')
    utility.write_log(20, '[Out] 8Vana [{}].'.format(file_name))
