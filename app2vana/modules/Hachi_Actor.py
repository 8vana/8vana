#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys
import configparser

# Type of printing.
OK = 'ok'         # [*]
NOTE = 'note'     # [+]
FAIL = 'fail'     # [-]
WARNING = 'warn'  # [!]
NONE = 'none'     # No label.


# Actor (Attacker and Target) class.
class Actor:
    def __init__(self, utility):
        self.utility = utility
        self.file_name = os.path.basename(__file__)
        self.full_path = os.path.dirname(os.path.abspath(__file__))
        self.root_path = os.path.join(self.full_path, '..')

        # Read config.ini.
        config = configparser.ConfigParser()
        config.read(os.path.join(self.root_path, 'config.ini'), encoding='utf-8')
        try:
            print()
        except Exception as e:
            self.utility.print_message(FAIL, 'Reading config.ini is failure : {}'.format(e))
            sys.exit(1)

        # Actor information.
        self.hostname = ''
        self.x = 0
        self.y = 0
        self.u = 0
        self.v = 0
        self.w = 0
        self.h = 0
        self.center_x = 0
        self.center_y = 0
        self.shot_x = 0
        self.shot_y = 0
        self.status = 'normal'
        self.origin_framecount = 0
        self.wait_framecount = 0.0
        self.corruption_flag = False
        self.wreck_flag = False

        # Actor text information.
        self.text_x = 0
        self.text_y = 0
        self.text_color = self.utility.color_7

        # Event information for monolith.
        self.event_info = []

    # Update.
    def update(self, x=0, u=0, w=0, status='normal', text_color=7):
        self.x += x
        self.u = u
        self.w += w
        self.status = status
        if self.corruption_flag:
            text_color = 10
        if self.wreck_flag:
            text_color = 8
        self.text_color = text_color
