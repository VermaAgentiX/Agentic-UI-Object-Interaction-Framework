# Hugging face Api code for using model

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv("token.env")

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ["HF_TOKEN"],
    #api_key="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",
)

completion = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-V4-Pro:novita",
    temperature=1.5,
    messages=[
        {
            "role": "user",
            "content": "what is langflow"
        }
    ],
)

print('AI----------x-----------------------\n')
print(completion.choices[0].message.content)
#print('-----------------------------x-----------------------\n')
#print(completion.choices[0].finish_reason)
