import openai

# 定義一個函式 找尋要回復給客戶的訊息
def Answer(text):  # 參數放入客戶給入的訊息
    if text == "1":
        message = [{
              "type": "text",
              "text": "歡迎使用 AK-GPT-Assistant  有任何軟體合作發案歡迎來訊 @ak8893893\n\n使用說明:\n1. 第一次使用請先到 https://platform.openai.com/account/api-keys 申請一個你的 gpt api token 並貼到這個機器人聊天窗 例如 : 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\n\n2. gpt 因為有前後文的關係   所以每次詢問都是連同上次的問答一同發送過去 久了會造訊息過長產生錯誤  可以輸入   0   清除前文紀錄\n\n3. 呼叫使用說明請輸入   1"
            }]
        return message




    message = [{
      "type": "text",
      "text": openai.call_AI(text)
    }]

    return message  # 回傳找不到關鍵字時的訊息