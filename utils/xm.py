import requests
import json
import base64
import random
import os
import string
from datetime import datetime
from Telegram_bot import send_message

def uuid_a():
    characters = string.ascii_lowercase + string.digits
    random_string = ''.join(random.choice(characters) for i in range(8))
    return random_string

def login(base_url, login_data):
    login_url = f"{base_url}/api/setMobileMemberLogin"
    headers = {
        "User-Agent": "mobile_app",
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "gpanda.co.kr",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip"
    }
    response = requests.post(login_url, headers=headers, data=login_data)
    # print(response.json())
    if response.status_code == 200:
        retftoken=response.json()['REFTokenID']
        accoken=response.json()['ACCTokenID']
    else:
        accoken = None
    return retftoken, accoken


def getserver(base_url, getvpn_data):
    global SS_link
    getserver_url = f"{base_url}/api/getVpnServerlist"
    headers = {
        "User-Agent": "mobile_app",
        "Cookie": f"REFTOKEN_ID={retftoken};ACCTOKEN_ID={accoken}",
        "Content-Type": "application/x-www-form-urlencoded",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        'content-length': '24'
    }
    response = requests.post(getserver_url, headers=headers, data=getvpn_data)
    for item in response.json()['data']:
        server_name = item['server_name'],
        link_format = "{method}:{password}@{hostname}:{port}".format(
            method='aes-256-cfb',
            password=os.environ['xm_pass'],
            hostname = item['server_ip'],
            # hostname = item['server_domain'],
            port = item['server_port'])
        ss_link_unencoded = "ss://" + base64.urlsafe_b64encode(link_format.encode()).decode()
        ss_link = ss_link_unencoded + "#" + ''.join(server_name)
        SS_link += ss_link + ' @𝙢𝙛𝙗𝙥𝙣\n'

SS_link = ''

base_url = os.environ['xm_url']
login_data = os.environ['xm_data']
getvpn_data = os.environ['xm_ssr']
retftoken, accoken = login(base_url, login_data)
getserver(base_url, getvpn_data)
# print(SS_link)
with open("./links/xm", "w") as f:
    f.write(base64.b64encode(SS_link.encode()).decode())
message = '#SS ' + '#订阅' + '\n' + datetime.now().strftime(
        "%Y年%m月%d日%H:%M:%S") + '\n' + 'XM订阅每天自动更新：' + '\n' + 'https://raw.githubusercontent.com/mfbpn/sublink/master/links/ss'
send_message(os.environ['chat_id'], message, os.environ['bot_token'])
