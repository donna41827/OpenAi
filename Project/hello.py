import openai

root_path = 'C:\\OpenAI\\'
key_file_path = f'{root_path}SECRET_KEY.txt'
key_file = open(key_file_path, "r", encoding='utf-8')
key = key_file.read()
print(f'key={key}')
openai.api_key = key

while True:  
    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
            {"role": "system", "content": "系統訊息，目前無用"},
            {"role": "assistant", "content": "此處填入機器人訊息"},
            {"role": "user", "content": input("You: ")}
        ]
    )
    print(completion.choices[0].message.content)