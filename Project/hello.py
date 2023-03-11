import openai

root_path = 'C:\\OpenAI\\'
key_file_path = f'{root_path}SECRET_KEY.txt'
key_file = open(key_file_path, "r", encoding='utf-8')
key = key_file.read()
print(f'key={key}')
openai.api_key = key

while True:  
    completion = openai.Completion.create(
      model="text-davinci-003",
      prompt=input("You: ")
    )
    print(completion.choices[0]['text'])