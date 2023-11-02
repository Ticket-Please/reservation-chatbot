import json
import openai

with open('./secret.json') as f:
    secrets = json.loads(f.read())
API_KEY = secrets["ChatGPT-key"]

openai.api_key = API_KEY

def test_call():
    prompt = "어르신들이 인터넷으로 기차예매를 할 수 있는 방법을 쉽게 설명해줘"

    completion = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = completion.choices[0].text
    print(message)
    return message