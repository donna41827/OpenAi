import openai

root_path = 'C:\\OpenAI\\'
key_file_path = f'{root_path}SECRET_KEY.txt'
key_file = open(key_file_path, "r", encoding='utf-8')
key = key_file.read()
openai.api_key = key
print(f'key={key}')

while True:
    source_path = ''
    user_msg = input("You: ")

    user_msg = f'請你模擬一個系統 我會問你一些問題 你會整理成可能的關鍵字並組成notion用的查詢物件並回傳 我不需求查詢物件以外的其他訊息 \
                我的問題是關於一個供應商管理系統 這個系統可以協助通路商管理供應商 供應商可以在系統上操作以修改通路商的賣場資料，通路商的賣場是第三方平台 \
                第一個問題是 「{user_msg}」\
                已傳送訊息. \
                請你模擬一個系統 我會問你一些問題 你會整理成可能的關鍵字並組成notion用的查詢物件並回傳 我不需求查詢物件以外的其他訊息 \
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