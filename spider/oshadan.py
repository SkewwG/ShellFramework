# coding:utf-8
# __Author__ : Loid
# http://loid.online
import requests

class oshadan():

    def __init__(self):
        self.loginSession = requests.Session()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0",
            "X-Requested-With": "XMLHttpRequest"
                   }

    def login(self):
        data = {'info': '{"username":"2375743231@qq.com","password":"0b4ad2ec172c586e2150770fbf9eLZOB","code":"","autologin":false}'}
        response = self.loginSession.post("https://www.oshadan.com/validateLogin", headers=self.headers,data=data)
        return response.json().get("type") == "success"

    def search(self, keyword, page=1):
        keyword, retValues = keyword.replace(" ", "+"), []
        response = self.loginSession.get('https://www.oshadan.com/search?info={"c":"%s","q":1,"p":%s}'%(keyword, page), headers=self.headers)
        retstatus = response.json().get("type")

        if response.status_code == 200 and retstatus == "success":
            datas = response.json()["result"]["result"]["data"]
            for data in datas:
                notcomponentFields, componentFields, titleFields = data.get("notcomponentFields"), data.get("componentFields"), data.get(
                "titleFields")
                url, ip, port, title, http_status, x_powered_by, webserver = notcomponentFields.get("url"), \
                                                                                notcomponentFields.get("ip"), \
                                                                                notcomponentFields.get("port"), \
                                                                                titleFields.get("keywords"), \
                                                                                titleFields.get("http_status"), \
                                                                                componentFields.get("x_powered_by"), \
                                                                                componentFields.get(u"应用")
                result = {"url": url, "ip": ip, "port": port, "title": title, "httpstatus": http_status, "x_powered_by": x_powered_by, "webserver": webserver}
                retValues.append(result)
            return retValues
        return

# a = oshadan()
# if a.login():
#     for i in a.search("phpcms"):
#         print i