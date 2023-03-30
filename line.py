"""
標題 : GPT Line 機器人
作者 : 賴韋銘 AK
時間 : 2023/3/29
todo : 1.optimized     2. deployed onto GCE  3.讓用戶可以輸入他的 gpt API token(目前我先用手動加token的方法)
"""
import openai
import socketserver as socketserver
from http.server import SimpleHTTPRequestHandler as RequestHandler
import json
import requests
from openpyxl import load_workbook  # 匯入 excel 資料庫
from datetime import datetime
import Chat
import re

# 讀取 secret_key.json
with open("secret_key.json") as f:
    secret = json.load(f)

# 輸入 使用者ID 和 token
YouruserID = secret["YouruserID"]
auth_token = secret["auth_token"]




class MyHandler(RequestHandler):  # 定義一個類別 繼承於 RequestHandler
    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        userId = YouruserID
        varLen = int(self.headers['Content-Length'])
        if varLen > 0:
            post_data = self.rfile.read(varLen)
            data = json.loads(post_data)
            print(data)  # 印出用戶傳過來訊息的所有資訊
            replyToken = data['events'][0]['replyToken']
            userId = data['events'][0]['source']['userId']
            text = data['events'][0]['message']['text']  # 用戶傳遞過來的文字內容
            dataType = data['events'][0]['message']['type']  # 用戶傳遞過來的資料型態
            timeStamp = data['events'][0]['timestamp'] // 1000  # 時間戳 改成秒的形式
            stampTime = datetime.fromtimestamp(int(timeStamp))  # 把時間戳變成 年月日時分秒的格式




        self.do_HEAD()
        # print(self.wfile)

        #match = re.search(r'^sk-[A-Za-z0-9]{60}$', text)
        #print(text[0:3], len(text))

        if text[0:3]=="sk-" and len(text) == 51 :
            with open("secret_key.json") as f:
                secret = json.load(f)
            secret["userId_gpt_key"][userId] = text
            # 將更新後的資料庫寫回.json檔案
            with open('secret_key.json', 'w') as f:
                json.dump(secret, f)
            message = {
                "replyToken": replyToken,  # 回應哪一個人 ( 用他打過來的replytoken打回去)
                "messages": [{
                  "type": "text",
                  "text": "已將您的chat GPT token 存入您的用戶資料庫中:\n" + "您的用戶ID為: " + userId + "\n" + "您的chat GPT token為: " + text
                }]  # 回復的訊息內容
            }

        else:
            # 依據使用者來使用 key
            with open("secret_key.json") as f:
                secret = json.load(f)
                openai.api_key = secret["userId_gpt_key"][userId]


            message = {
                "replyToken": replyToken,  # 回應哪一個人 ( 用他打過來的replytoken打回去)
                "messages": Chat.Answer(text)  # 回復的訊息內容
            }

        # 紀錄和客戶對話的所有訊息
        # wb = load_workbook("Log.xlsx")  # 開啟 Log excel 準備存資料
        # sheet = wb.active  # create Workbook object
        # interactData = (stampTime, userId, dataType, text, answer)  # 把資料變成tuple準備放入excel
        # sheet.append(interactData)  # Appending group of values at the bottom of the current sheet
        # wb.save("Log.xlsx")  # 存檔

        # 發出post請求
        hed = {'Authorization': 'Bearer ' + auth_token}  # 標頭 (Line規定要寫這樣) + auth_token
        url = 'https://api.line.me/v2/bot/message/reply'  # line API url
        response = requests.post(url, json=message, headers=hed)  # 用 post 的方法打過去
        print(response)  # 把結果印出來 200 代表成功
        print(response.json())  # 印出結果的的JSON資料


# ngrok端口 先設定好本機端口 再去cmd /d (ngrok檔案位置) 輸入 ngrok http 8888 發訊息給機器人就可以收到你發的資料了
socketserver.TCPServer.allow_reuse_address = True
httpd = socketserver.TCPServer(('0.0.0.0', 8888), MyHandler)
httpd.serve_forever()