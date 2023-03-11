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
    if "維運" in user_msg:
        source_path = f'{root_path}DataSource\MantainSulotion.txt'

    if source_path != '':
        f = open(source_path, "r", encoding = 'utf-8')
        source_context = f.read()
        user_msg = f'請給我下列資料中:\n{source_context}\n最接近{user_msg}的解決方案'
    
    print(f'你的問題是:{user_msg}')

    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
            {"role": "system", "content": "系統訊息，目前無用"},
            {"role": "assistant", "content": "此處填入機器人訊息"},
            {"role": "user", "content": user_msg}
        ],
    )

    print(completion.choices[0].message.content)