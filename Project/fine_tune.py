import os
import openai
import json
import time

root_path = 'C:\\OpenAI\\'
key_file_path = f'{root_path}SECRET_KEY.txt'
key_file = open(key_file_path, "r", encoding='utf-8')
key = key_file.read()
print(f'key={key}')
openai.api_key = key

training_data_path = f"{root_path}DataSource\ImsSystemMaintainSulotion.jsonl"

upload_response = openai.File.create(
  file=open(training_data_path, "rb"),
  purpose='fine-tune'
)

file_id = upload_response.id

FineTune = openai.FineTune.create(
    model = 'ada',
    training_file=file_id
)
print(FineTune)

response = openai.FineTune.retrieve(FineTune.id)

total_time = 0

while response.fine_tuned_model is None:
    time.sleep(10)
    total_time += 10
    response = openai.FineTune.retrieve(FineTune.id)
    print(response)
    print(f'total time:{total_time}sec')

model_name = response.fine_tuned_model

while True:  
    completion = openai.Completion.create(
      model = model_name,
      prompt = [
            {"role": "system", "content": "系統訊息，目前無用"},
            {"role": "assistant", "content": "此處填入機器人訊息"},
            {"role": "user", "content": input("You: ")}
        ]
    )
    print(completion.choices[0].message.content)