import os
import time
import json
from time import sleep
from os import name, system

try:
  import requests
except ImportError:
    os.system('python -m pip install requests')
try:
  import urllib3
except ImportError:
    os.system('python -m pip install urllib3')
try:
  from bs4 import BeautifulSoup
except ImportError:
    os.system('python -m pip install bs4')

def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

clear()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

srttm = time.time()

usr = input("[?] Username: ")

if usr.startswith("@"):
    usr = usr
else:
    usr = f"@{usr}"

r0 = requests.get(f"https://www.tiktok.com/{usr}", headers={"User-Agent":"Mozilla/5.0 (Linux; Android 11; M2102J20SG Build/RQ3A.210705.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/93.0.4577.62 Mobile Safari/537.36 trill_2022002050 JsSdk/1.0 NetType/WIFI Channel/googleplay AppName/musical_ly app_version/20.2.5 ByteLocale/en ByteFullLocale/en Region/US"})
soup = BeautifulSoup(r0.text, "html.parser")
content = soup.find_all(attrs={"id":"__NEXT_DATA__"})
content = json.loads(content[0].contents[0])
profile_data = {
    "uid":content['props']['pageProps']['userInfo']['user']['id']
    }

uid = f"{profile_data.get('uid')}"

print("\n", end="")

def report():
    h1 = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US",
        "content-type": "application/json",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin"
        }

    d1 = """{
        "reason": "311",
        "object_id": "%s",
        "owner_id": "%s",
        "report_type": "user"
        }""" % (uid, uid)

    r1 = requests.post("https://www.tiktok.com/node/report/reasons_put?", headers=h1, data=d1, verify=False, timeout=999999)

    if r1.ok:
        r1json = r1.json()
        if r1json.get("statusCode") == 0:
            print(f"[+] Report sent successfully")
        else:
            print(f"[-] Report could not be sent")
            return
    else:
        print(f"[-] Report could not be sent")
        return

while True:
    report()
    time.sleep(2.0 - ((time.time() - srttm) % 2.0))