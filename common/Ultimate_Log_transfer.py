#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import os
import configparser
import sqlite3
import requests
import shutil
import re
import json
import codecs
import datetime
import time


# Transfer class.
class Transfer:
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

            converted_log_dir = os.path.join(self.root_path, config['LogParser']['converted_log_path'])
            self.converted_log_path = os.path.join(converted_log_dir, config['LogParser']['converted_log_file'])
        except Exception as e:
            print('Reading config.ini is failure : {}'.format(e))
            sys.exit(1)

        self.attack = {"nmap": {"phase": "discover", "cve": ["N/A"]},
                       "nikto": {"phase": "discover", "cve": ["N/A"]},
                       "drupal": {"phase": "attack", "cve": ["CVE-2018-7600"]},
                       "tomcat": {"phase": "attack", "cve": ["CVE-2017-12615", "CVE-2017-12617"]},
                       "tomcat_manager_upload": {"phase": "attack", "cve": ["N/A"]},
                       "ghost": {"phase": "attack", "cve": ["N/A"]},
                       "arraywebshell.jsp": {"phase": "attack", "cve": ["N/A"]},
                       "password_crack": {"phase": "attack",   "cve": ["N/A"]},
                       "sqli": {"phase": "attack", "cve": ["N/A"]},
                       "drupal1": {"phase": "attack", "cve": ["N/A"]}}
        self.regex_ipaddr = re.compile(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}")

    # Extract json file from DB.
    def export_from_db(self, db_path, from_ipaddr):
        logs = []
        if os.path.exists(db_path):
            conn = sqlite3.connect(db_path)
            # conn.text_factory = bytes
            conn.text_factory = lambda b: b.decode(errors='ignore')
            cur = conn.cursor()
            cur.execute('SELECT id, created_at, type, log FROM log ORDER BY id')
            rows = cur.fetchall()

            for row in rows:
                lines = row[3].split("\n")
                print("#### %s %s %s ####" % (row[0], row[1], row[2]))
                date, time = row[1].split(" ")
                year, month, day = date.split("-")
                h, m, s = time.split(":")
                dt = datetime.datetime(int(year), int(month), int(day), int(h), int(m), int(s))

                for line in lines:
                    pattern = '^execute:'
                    if re.match(pattern, line):
                        try:
                            data = line.split(" ")
                            to_ipaddr = (self.regex_ipaddr.findall(data[3]))[0]
                            option = data[5:]
                            option = re.sub(r"^\(|\)$", "", " ".join(option))
                            params = {"phase": self.attack[row[2]]["phase"],
                                      "attack": row[2],
                                      "time": dt.timestamp(),
                                      "from": from_ipaddr,
                                      "to": to_ipaddr,
                                      "note": {"option": option, "CVE": self.attack[row[2]]["cve"]}}
                            logs.append(params)
                        except Exception as e:
                            print(e.args)

        return logs


# main.
if __name__ == '__main__':
    file_name = os.path.basename(__file__)
    full_path = os.path.dirname(os.path.abspath(__file__))

    transfer = Transfer()

    # Target information.
    kali_url = ['http://localhost:18080/staff_upload/8vana.db', 'http://localhost:28080/staff_upload/8vana.db']
    kali_ip = ['172.31.200.91', '172.31.200.92']
    db_name = ['8vana_1.db', '8vana_2.db']

    # Get Database from remote server.
    while True:
        non_sort_log = []
        for idx, target_url in enumerate(kali_url):
            res = requests.get(target_url, stream=True)
            db_path = os.path.join(full_path, db_name[idx])
            with open(db_path, 'wb') as fout:
                shutil.copyfileobj(res.raw, fout)

            non_sort_log.extend(transfer.export_from_db(db_path, kali_ip[idx]))

        # Merge JSON files
        sorted_log = sorted(non_sort_log, key=lambda s:s['time'])
        with codecs.open(transfer.converted_log_path, 'w') as fout:
            json.dump(sorted_log, fout, indent=4)

        time.sleep(transfer.watch_period)
