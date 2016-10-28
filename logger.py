#
#  Copyright 2016 Marcos Mirabent
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

from modem import Modem
import sched
import sqlite3
import datetime
import sys

m = Modem("192.168.100.1")
conn = sqlite3.connect('modem_stats.db')


def signal_handler(signal, frame):
    conn.close()
    sys.exit(0)

def create_db():
    c = conn.cursor()
    c.execute('''DROP TABLE IF EXISTS stats''')
    c.execute('''CREATE TABLE stats (time text, dstream_pwr text, dstream_snr text, ustream_pwr text)''')
    conn.commit()


def get_new_stats():
    m.refresh_data()
    c = conn.cursor()
    now = datetime.datetime.utcnow()
    date = now.strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO stats VALUES (?,?,?,?)",[date,m.downstream_power,m.downstream_snr,m.upstream_power])
    conn.commit()

create_db()
scheduler = sched.scheduler()

try:
    while True:
        scheduler.enter(5,1,get_new_stats)
        scheduler.run()

except KeyboardInterrupt:
    conn.close()
    sys.exit(0)

