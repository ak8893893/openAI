"""
標題 : GPT Line 機器人
作者 : 賴韋銘 AK
時間 : 2023/3/29
"""
import openai
import socketserver as socketserver
from http.server import SimpleHTTPRequestHandler as RequestHandler
import json
import requests
from openpyxl import load_workbook  # 匯入 excel 資料庫
from datetime import datetime

# 讀取 secret_key.json
with open("secret_key.json") as f:
    data = json.load(f)

# 輸入 使用者ID 和 token
YouruserID = data["YouruserID"]
auth_token = data["auth_token"]

# # 讀取 excel 檔案 把關鍵字索引和回答資料庫建成列表
# wb = load_workbook('KitKat客服機器人資料庫.xlsx')  # 讀取 excel 檔案
# sheetQA = wb["問答表"]  # 選擇 excel 內的 問答表 table
# searchList = []  # 建立 一個空的List 當作關鍵字索引
# for x in range(2, sheetQA.max_row + 1):  # 第一欄除標頭第一筆到最後一筆
#     searchList.append(sheetQA.cell(row=x, column=1).value)  # 把關鍵字加入關鍵字列表中
# print(searchList)  # 印出關鍵字列表
# answerList = []  # 建立一個空的List 當作回答資料庫
# for x in range(2, sheetQA.max_row + 1):  # 第二欄除標頭第一筆到最後一筆
#     answerList.append(sheetQA.cell(row=x, column=2).value)  # 把回答資料加入回答列表中
# print(answerList)  # 印出回答列表


# 定義一個函式 找尋要回復給客戶的訊息
def Answer(text):  # 參數放入客戶給入的訊息




    message = [{
      "type": "text",
      "text": openai.call_AI(text)
    }]

    return message  # 回傳找不到關鍵字時的訊息


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
        message = {
            "replyToken": replyToken,  # 回應哪一個人 ( 用他打過來的replytoken打回去)
            "messages": Answer(text)  # 回復的訊息內容
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