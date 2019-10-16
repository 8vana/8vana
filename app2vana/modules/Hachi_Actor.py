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
        self.system_info = {'OS': 'Debian',
                            'Web': 'Apache 2.2',
                            'Lang': 'PHP 5.6',
                            'CMS': 'WordPress 4.2'}
        self.other_info = []
        self.vuln_info = []

        # Actor text information.
        self.text_x = 0
        self.text_y = 0
        self.text_color = self.utility.color_7

        # TODO: テキスト描画テスト用のコード
        cve_list = ['CVE-2013-2249 : Apache HTTP Server 2.2.10',
                    'CVE-2013-1862 : Apache HTTP Server 2.2.18',
                    'CVE-2016-8612 : Apache HTTP Server 2.2.9',
                    'CVE-2014-0098 : Apache HTTP Server 2.2.25',
                    'CVE-2014-9426 : PHP 5.6.4',
                    'CVE-2014-9425 : PHP 5.6.2',
                    'CVE-2014-8142 : PHP 5.6.0',
                    'CVE-2014-5459 : PHP 5.6.0',
                    'CVE-2015-5734 : WordPress 4.2.3',
                    'CVE-2015-5731 : WordPress 4.2.3',
                    'CVE-2015-5730 : WordPress 4.2.3',
                    'CVE-2015-3440 : WordPress 4.2']
        for idx in range(50):
            self.other_info.append('other_text{}'.format(idx + 1))
        for idx in range(50):
            if idx < 12:
                self.vuln_info.append(cve_list[idx])
            else:
                self.vuln_info.append('cve_text{}'.format(idx + 1))

    # Update.
    def update(self, x=0, u=0, w=0, status='normal', text_color=7):
        self.x += x
        self.u = u
        self.w += w
        self.status = status
        self.text_color = text_color
