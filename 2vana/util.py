#!/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import string
import random
import ipaddress
import configparser
from datetime import datetime
from logging import getLogger, FileHandler, Formatter

# Printing colors.
OK_BLUE = '\033[94m'      # [*]
NOTE_GREEN = '\033[92m'   # [+]
FAIL_RED = '\033[91m'     # [-]
WARN_YELLOW = '\033[93m'  # [!]
ENDC = '\033[0m'
PRINT_OK = OK_BLUE + '[*]' + ENDC
PRINT_NOTE = NOTE_GREEN + '[+]' + ENDC
PRINT_FAIL = FAIL_RED + '[-]' + ENDC
PRINT_WARN = WARN_YELLOW + '[!]' + ENDC

# Type of printing.
OK = 'ok'         # [*]
NOTE = 'note'     # [+]
FAIL = 'fail'     # [-]
WARNING = 'warn'  # [!]
NONE = 'none'     # No label.


# Utility class.
class Utility:
    def __init__(self):
        # Read config.ini.
        full_path = os.path.dirname(os.path.abspath(__file__))
        config = configparser.ConfigParser()
        config.read(os.path.join(full_path, 'config.ini'), encoding='utf-8')

        try:
            self.banner_delay = float(config['Common']['banner_delay'])
            self.report_date_format = config['Common']['date_format']
            self.modules_dir = config['Common']['module_path']
            self.log_dir = os.path.join(full_path, config['Common']['log_path'])
            if os.path.exists(self.log_dir) is False:
                os.mkdir(self.log_dir)
                self.print_message(NOTE, 'Created directory : {}'.format(self.log_dir))
            self.log_file = config['Common']['log_file']
            self.log_path = os.path.join(self.log_dir, self.log_file)

            # Load fps rate.
            self.fps = int(config['Common']['fps'])
            if self.fps < 30:
                self.print_message(WARNING, 'Too short fps. Change : {} -> 30'.format(str(self.fps)))
                self.fps = 30
            elif self.fps > 60:
                self.print_message(WARNING, 'Too short fps. Change : {} -> 60'.format(str(self.fps)))
                self.fps = 60

        except Exception as e:
            self.print_message(FAIL, 'Reading config.ini is failure : {}'.format(e))
            sys.exit(1)

        # Define image bank Id.
        self.image_id_0 = 0
        self.image_id_1 = 1
        self.image_id_2 = 2

        # Define tile map Id.
        self.tm_id_0 = 0
        self.tm_id_1 = 1
        self.tm_id_2 = 2
        self.tm_id_3 = 3
        self.tm_id_4 = 4
        self.tm_id_5 = 5
        self.tm_id_6 = 6
        self.tm_id_7 = 7

        # Define color key.
        self.color_0 = 0
        self.color_1 = 1
        self.color_2 = 2
        self.color_3 = 3
        self.color_4 = 4
        self.color_5 = 5
        self.color_6 = 6
        self.color_7 = 7
        self.color_8 = 8
        self.color_9 = 9
        self.color_10 = 10
        self.color_11 = 11
        self.color_12 = 12
        self.color_13 = 13
        self.color_14 = 14
        self.color_15 = 15

        # Define status.
        self.status_normal = 'normal'
        self.status_attack_main = 'main_gun'
        self.status_attack_sub = 'sub_gun'
        self.status_attack_se = 'special_enquipment'
        self.status_attack_probe = 'probe'

        # Setting logger.
        self.logger = getLogger('8Vana')
        self.logger.setLevel(20)
        file_handler = FileHandler(self.log_path)
        self.logger.addHandler(file_handler)
        formatter = Formatter('%(levelname)s,%(message)s')
        file_handler.setFormatter(formatter)

    # Print metasploit's symbol.
    def print_message(self, type, message):
        if os.name == 'nt':
            if type == NOTE:
                print('[+] ' + message)
            elif type == FAIL:
                print('[-] ' + message)
            elif type == WARNING:
                print('[!] ' + message)
            elif type == NONE:
                print(message)
            else:
                print('[*] ' + message)
        else:
            if type == NOTE:
                print(PRINT_NOTE + ' ' + message)
            elif type == FAIL:
                print(PRINT_FAIL + ' ' + message)
            elif type == WARNING:
                print(PRINT_WARN + ' ' + message)
            elif type == NONE:
                print(NOTE_GREEN + message + ENDC)
            else:
                print(PRINT_OK + ' ' + message)

    # Print exception messages.
    def print_exception(self, e, message):
        self.print_message(WARNING, 'type:{}'.format(type(e)))
        self.print_message(WARNING, 'args:{}'.format(e.args))
        self.print_message(WARNING, '{}'.format(e))
        self.print_message(WARNING, message)

    # Write logs.
    def write_log(self, loglevel, message):
        self.logger.log(loglevel, self.get_current_date() + ' ' + message)

    # Count wait time using FPS.
    def wait_framecount(self, second):
        return int(self.fps * second)

    # Create random string.
    def get_random_token(self, length):
        chars = string.digits + string.ascii_letters
        return ''.join([random.choice(chars) for _ in range(length)])

    # Get current date.
    def get_current_date(self, indicate_format=None):
        if indicate_format is not None:
            date_format = indicate_format
        else:
            date_format = self.report_date_format
        return datetime.now().strftime(date_format)

    # Transform date from string to object.
    def transform_date_object(self, target_date, format=None):
        if format is None:
            return datetime.strptime(target_date, self.report_date_format)
        else:
            return datetime.strptime(target_date, format)

    # Transform date from object to string.
    def transform_date_string(self, target_date):
        return target_date.strftime(self.report_date_format)

    # Delete control character.
    def delete_ctrl_char(self, origin_text):
        clean_text = ''
        for char in origin_text:
            ord_num = ord(char)
            # Allow LF,CR,SP and symbol, character and numeric.
            if (ord_num == 10 or ord_num == 13) or (32 <= ord_num <= 126):
                clean_text += chr(ord_num)
        return clean_text

    # Check IP address format.
    def is_valid_ip(self, arg):
        try:
            ipaddress.ip_address(arg)
            return True
        except ValueError:
            return False
