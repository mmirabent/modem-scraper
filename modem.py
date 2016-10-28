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

import re
import requests
from bs4 import BeautifulSoup

class Modem:

    def __init__(self,modem = None):
        if modem is None:
            self.modem_name = "127.0.0.1"
        else:
            self.modem_name = modem
        self.downstream_power = None
        self.downstream_snr = None
        self.upstream_power = None
        self.__dbmv = re.compile('dBmV')

    def refresh_data(self):
        r = requests.get("http://" + self.modem_name + "/RgSignal.asp")
        soup = BeautifulSoup(r.text, 'html.parser')

        downstream_table = soup.find('td',string="Downstream").find_parent('table')
        self.downstream_power = downstream_table.find(string=self.__dbmv)
        self.downstream_snr = downstream_table.find('td', string="Signal To Noise Ratio").next_sibling.text

        upstream_table = soup.find('td',string="Upstream").find_parent('table')
        self.upstream_power = upstream_table.find(string=self.__dbmv)

