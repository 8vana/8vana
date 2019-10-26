#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys
import codecs
import re
import configparser

# Type of printing.
OK = 'ok'         # [*]
NOTE = 'note'     # [+]
FAIL = 'fail'     # [-]
WARNING = 'warn'  # [!]
NONE = 'none'     # No label.


# Paerser class.
class Parser:
    def __init__(self, utility):
        self.utility = utility
        self.file_name = os.path.basename(__file__)
        self.full_path = os.path.dirname(os.path.abspath(__file__))
        self.root_path = os.path.join(self.full_path, '..')

        # Read config.ini.
        config = configparser.ConfigParser()
        config.read(os.path.join(self.root_path, 'config.ini'), encoding='utf-8')
        try:
            self.max_read_size = int(config['LogParser']['max_read_size'])
            target_log_dir = os.path.join(self.root_path, config['LogParser']['target_log_path'])
            self.target_log_path = os.path.join(target_log_dir, config['LogParser']['target_log_file'])
            self.divide_regex = config['LogParser']['divide_regex']
            self.date_regex = config['LogParser']['date_regex']
            self.phase_regex = config['LogParser']['phase_regex']
            self.action_regex = config['LogParser']['action_regex']
            self.note_regex = config['LogParser']['note_regex']
            self.from_regex = config['LogParser']['from_regex']
            self.to_regex = config['LogParser']['to_regex']
            self.fire_regex_list = config['LogParser']['fire_regex'].split('@')
        except Exception as e:
            self.utility.print_message(FAIL, 'Reading config.ini is failure : {}'.format(e))
            sys.exit(1)

    # Get object (attacker, target) index.
    def get_object_index(self, target_list, obj_name):
        get_index = 0
        for idx, target_name in enumerate(target_list):
            if target_name == obj_name:
                get_index = idx
                break
        return get_index

    # Parse log.
    def parse_log(self, contents):
        # Extract response time from log.
        all_logs = re.split(self.divide_regex, contents)

        parsed_logs = []
        for log in all_logs:
            fire_flag = False
            date = re.findall(self.date_regex, log)
            phase = re.findall(self.phase_regex, log)
            action = re.findall(self.action_regex, log)
            note = re.findall(self.note_regex, log)
            src = re.findall(self.from_regex, log)
            dest = re.findall(self.to_regex, log)

            if len(date) != 0 and len(phase) != 0 and len(action) != 0 and len(note) != 0 and len(src) != 0 and len(dest) != 0:
                if note[0] != '':
                    for fire_regex in self.fire_regex_list:
                        result = re.findall(fire_regex, note[0])
                        if len(result) != 0:
                            fire_flag = True
                            break

                parsed_logs.append({'Date': date[0],
                                    'Phase': phase[0],
                                    'Action': action[0],
                                    'Note': note[0],
                                    'From': src[0],
                                    'To': dest[0],
                                    'Vulnerability': fire_flag})
        return parsed_logs

    # Monitor log files.
    def watch(self, read_start_byte):
        # Check updated date of target log.
        if os.path.exists(self.target_log_path):
            # Read log.
            with codecs.open(self.target_log_path, mode='r', encoding='utf-8') as fin:
                fin.seek(read_start_byte)
                content = fin.read()
            return content

        return ''
