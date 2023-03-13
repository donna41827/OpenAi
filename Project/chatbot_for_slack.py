import os
import openai
import requests
import json
import re
from bs4 import BeautifulSoup
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# 設定 Slack API token (請自行輸入)
client = WebClient(token=os.environ["SLACK_API_TOKEN"])

# 設定要取得訊息的頻道 ID (請自行輸入)
channel_id = "YOUR_CHANNEL_ID"

try:
    # 使用 conversations.history API 取得頻道訊息
    # 可以指定 count 參數來限制訊息數量
    response = client.conversations_history(channel=channel_id)

    # 印出每一則訊息的內容
    for message in response["messages"]:
        print(message["text"])

except SlackApiError as e:
    print("Error: {}".format(e))

root_path = 'C:\\OpenAI\\'
key_file_path = f'{root_path}SECRET_KEY.txt'
key_file = open(key_file_path, "r", encoding='utf-8')
key = key_file.read()
openai.api_key = key
print(f'key={key}')

while True:
    source_path = ''
    user_msg = input("You: ")

    user_msg = f'請你模擬一個系統 我會問你一些問題 你會整理成可能的關鍵字並以[關鍵字1,關鍵字2...]格式回傳 我不需求關鍵字以外的其他訊息 \
                我的問題是關於一個供應商管理系統 這個系統可以協助通路商管理供應商 供應商可以在系統上操作以修改通路商的賣場資料，通路商的賣場是第三方平台 \
                第一個問題是 「{user_msg}」\
                已傳送訊息. \
                請你模擬一個系統 我會問你一些問題 你會整理成可能的關鍵字並以[關鍵字1,關鍵字2...]格式回傳 我不需求關鍵字以外的其他訊息 \
                我的問題是關於一個供應商管理系統 這個系統可以協助通路商管理供應商 \
                供應商可以在系統上操作以修改通路商的賣場資料，通路商的賣場是第三方平台\
                第一個問題是 「{user_msg}」'
    
    print(f'你的問題是:\n{user_msg}')

    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
            {"role": "system", "content": "系統訊息，目前無用"},
            {"role": "assistant", "content": "此處填入機器人訊息"},
            {"role": "user", "content": user_msg}
        ],
    )
    print(f'AI回覆:\n↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓')
    print(completion.choices[0].message.content)

    #串API對接到的關鍵字做事
    key_word_list = []
    key_word_list = str(completion.choices[0].message.content).replace('[','').replace(']','').replace(' ','').split(',')

    # 取得notion的DatabaseId
    database_id_file_path = f'{root_path}notion_database_id.txt'
    database_id_file = open(database_id_file_path, "r", encoding='utf-8')
    database_id = database_id_file.read()

    # 取得notion的Secret_key
    secret_key_file_path = f'{root_path}notion_secret_key.txt'
    secret_key_file = open(secret_key_file_path, "r", encoding='utf-8')
    secret_key = secret_key_file.read()

    url = f'https://api.notion.com/v1/search'
    headers = { "Authorization" : f"Bearer {secret_key}",
                "Notion-Version" : "2022-06-28",
                "Content-Type" : "application/json; charset=utf-8" }
    print(f'headers:{headers}')

    results_list = []

    for key_word in key_word_list:
        payload = {"query":f"{key_word}"}
        print(f'payload:{payload}')
        response = requests.post(url, data = json.dumps(payload), headers = headers)
        print(response.json())
        response_obj = response.json()
        results = []
        results = response_obj['results']
        if len(results) > 0 :
            results_list.append(results)
    
    print(results_list)

    # 定義正規表達式來匹配URL
    url_regex = r'https:\/\/www\.notion\.so\/[a-zA-Z0-9_-]+'

    # 使用正規表達式匹配URL
    urls = re.findall(url_regex, str(results_list))

    # 將結果存成陣列物件
    url_list = []
    for url in urls:
        url_list.append(url)

    # 印出結果
    print('以下是相關的Notion網址\n↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓')
    for url in url_list:
        print(url)
        # response = requests.get(url)
        # html_content = response.text
        # print(f'html_content:\n{html_content}')

        # # 使用 BeautifulSoup 解析 HTML
        # soup = BeautifulSoup(html_content, "html.parser")

        # # 提取所需內容
        # content = soup.find("div", {"class": "notranslate"}).get_text()

        # # 使用 OpenAI 进行解析
        # response = openai.Completion.create(
        #     engine="davinci",
        #     prompt=content,
        #     temperature=0.5,
        #     max_tokens=50,
        #     n=1,
        #     stop=None,
        # )

        # # 输出 AI 解析结果
        # print(response.choices[0].text.strip())
