#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys
import codecs
import json
import re
import time
import configparser
from datetime import datetime

# Type of printing.
OK = 'ok'         # [*]
NOTE = 'note'     # [+]
FAIL = 'fail'     # [-]
WARNING = 'warn'  # [!]
NONE = 'none'     # No label.


# Paerser class.
class Parser:
    def __init__(self):
        self.file_name = os.path.basename(__file__)
        self.full_path = os.path.dirname(os.path.abspath(__file__))
        self.root_path = os.path.join(self.full_path, '..')

        # Read config.ini.
        config = configparser.ConfigParser()
        config.read(os.path.join(self.full_path, 'config.ini'), encoding='utf-8')
        try:
            self.date_format = config['Common']['date_format']
            self.default_charset = config['Common']['default_charset']
            self.watch_period = int(config['Common']['watch_period'])
            if self.watch_period < 5:
                print('Watching period is too short. >= 5[s]')
                self.watch_period = 5

            origin_log_dir = os.path.join(self.root_path, config['LogParser']['origin_log_path'])
            self.origin_log_path = os.path.join(origin_log_dir, config['LogParser']['origin_log_file'])
            converted_log_dir = os.path.join(self.root_path, config['LogParser']['converted_log_path'])
            self.converted_log_path = os.path.join(converted_log_dir, config['LogParser']['converted_log_file'])
            self.divide_regex = config['LogParser']['divide_regex']
            self.date_regex = config['LogParser']['date_regex']
            self.phase_regex = config['LogParser']['phase_regex']
            self.action_regex = config['LogParser']['action_regex']
            self.note_regex = config['LogParser']['note_regex']
            self.from_regex = config['LogParser']['from_regex']
            self.to_regex = config['LogParser']['to_regex']
            self.fire_regex_list = config['LogParser']['fire_regex'].split('@')
        except Exception as e:
            print('Reading config.ini is failure : {}'.format(e))
            sys.exit(1)

    # Add log to JSON file.
    def append_json_to_file(self, data):
        with codecs.open(self.converted_log_path, mode='a', encoding=self.default_charset) as fout:
            fout.seek(0, 2)
            if fout.tell() == 0:
                fout.write(json.dumps([data], indent=4))
            else:
                fout.seek(-1, 2)
                fout.truncate()
                fout.write(' , ')
                fout.write(json.dumps(data, indent=4))
                fout.write(']')
            print('Wrote logs: {}'.format(data))

    # Parse log.
    def parse_log(self, contents):
        # Extract response time from log.
        all_logs = re.split(self.divide_regex, contents)

        with codecs.open(self.converted_log_path, mode='a', encoding='utf-8') as fout:
            parsed_logs = []
            for log in all_logs:
                fire_list = []
                phase = re.findall(self.phase_regex, log)
                attack = re.findall(self.action_regex, log)
                date = re.findall(self.date_regex, log)
                src = re.findall(self.from_regex, log)
                dest = re.findall(self.to_regex, log)
                note = re.findall(self.note_regex, log)

                if len(date) != 0 and len(phase) != 0 and len(attack) != 0 and len(note) != 0 and len(src) != 0 and len(dest) != 0:
                    if note[0] != '':
                        for fire_regex in self.fire_regex_list:
                            fire_list = re.findall(fire_regex, note[0])
                            if len(fire_list) != 0:
                                break

                    date_epoc = datetime.strptime(date[0], self.date_format).timestamp()
                    log_content = {'phase': phase[0],
                                   'attack': attack[0],
                                   'time': date_epoc,
                                   'from': src[0],
                                   'to': dest[0],
                                   'note': {'option': note[0], 'CVE': fire_list}}
                    self.append_json_to_file(log_content)

        return parsed_logs

    # Monitor log files.
    def watch(self, read_start_byte):
        # Check updated date of target log.
        if os.path.exists(self.origin_log_path):
            # Read log.
            with codecs.open(self.origin_log_path, mode='r', encoding='utf-8') as fin:
                fin.seek(read_start_byte)
                content = fin.read()
            return content
        else:
            return ''


# main.
if __name__ == '__main__':
    file_name = os.path.basename(__file__)
    full_path = os.path.dirname(os.path.abspath(__file__))
    # Create instance.
    parser = Parser()

    # Watching loop.
    read_start_byte = 0
    while True:
        log_contents = parser.watch(read_start_byte)

        if len(log_contents) != 0:
            read_start_byte += len(log_contents)
            parsed_log_list = parser.parse_log(log_contents)

        # Wait.
        print('waiting.. {}[s]'.format(parser.watch_period))
        time.sleep(parser.watch_period)
