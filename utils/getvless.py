# -------------------------------------------------------------------------------
# Copyright (c) 2024. 挥杯劝, Inc. All Rights Reserved
# @作者         : 挥杯劝(Huibq)
# @邮件         : huibq120@gmail.com
# @文件         : TrojanLinks - getvless.py
# @创建时间     : 2024/01/10 20:08
# -------------------------------------------------------------------------------
# -*- coding: utf-8 -*-
import json
import os
import time
import uuid
from datetime import datetime
import requests
import urllib3
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import AES
from Crypto.Hash import MD5
from Crypto.Util.Padding import pad, unpad
from binascii import a2b_hex, b2a_hex
import base64
from base64 import b64decode
from Telegram_bot import send_message

urllib3.disable_warnings()


def decrypt_aes(data):
    iv = b'\x08\x08\x0c\x0a\x00\x0f\x00\x0e\x0a\x01\x0e\x0c\x0f\x09\x07\x05'
    cipher = AES.new(private_key.encode(), AES.MODE_CBC, authorization.encode())
    # data_len = len(data)
    # print(data_len)
    decrypted_data = unpad(cipher.decrypt(a2b_hex(data)), AES.block_size)
    # print(decrypted_data)
    return decrypted_data.decode('utf8')


def get_node():
    url = api
    headers = {"User-Agent": "Dalvik/2.1.0 (Linux; U; Android 10; MI 9 MIUI/20.9.4)"}
    req = requests.get(url, headers=headers, verify=False).content
    #print(req)
    node_list = json.loads(str(decrypt_aes(req)))['data']
    Vless = ''
    for i in node_list :
        host = i['ip']
        vless = 'ss://YWVzLTI1Ni1jZmI6YW1hem9uc2tyMDU=' + '@' + host + ':' + '443' + '#' + '%F0%9F%87%AD%F0%9F%87%B0%20%F0%9D%99%8F%F0%9D%99%82%40%F0%9D%99%88%F0%9D%99%81%F0%9D%98%BD%F0%9D%99%8B%F0%9D%99%89'
        Vless += vless + '\n'
        if i == node_list[11]:
            break
    with open("./links/vless", "w") as f:
        f.write(base64.b64encode(Vless.encode()).decode())
    return None

if __name__ == '__main__':
    api = os.environ['vless_api']
    private_key = os.environ['vless_private_key']
    authorization = os.environ['vless_authorization']
    #text = os.environ['vless_text']
    #invite()
    get_node()
    message = '#vless ' + '#订阅' + '\n' + datetime.now().strftime("%Y年%m月%d日%H:%M:%S") + '\n' + 'vless订阅每天自动更新：' + '\n' + 'https://raw.githubusercontent.com/mfbpn/TrojanLinks/master/links/vless'
    send_message(os.environ['chat_id'], message, os.environ['bot_token'])
