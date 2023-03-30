import openai

# 定義一個函式 找尋要回復給客戶的訊息
def Answer(text):  # 參數放入客戶給入的訊息
    if text == "請告訴我使用流程":
        message = [{
              "type": "text",
              "text": "1. 填入你的gpt api token    \n2. 開始問問題    \n3. 輸入   0    來清除前文\n"
            }]
        return message




    message = [{
      "type": "text",
      "text": openai.call_AI(text)
    }]

    return message  # 回傳找不到關鍵字時的訊息