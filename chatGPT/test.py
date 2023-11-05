import json
import openai
from fastapi import FastAPI
import httpx
import asyncio

app = FastAPI()


with open('./secret.json') as f:
    secrets = json.loads(f.read())
API_KEY = secrets["ChatGPT-key"]

openai.api_key = API_KEY

response = {
    "version": "2.0",
    "template": {
        "outputs": [
            {
                "simpleText": {
                    "text": "안녕하세용가리치킨"
                }
            }
        ]
    }
}


def test_call():
    prompt = "기차 예매를 하는 방법을 쉽게 설명해줘"
    messages = [{'role':'user', 'content':prompt}]

    completion = openai.ChatCompletion.create(
        model='gpt-3.5-turbo-0613',
        messages=messages,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )


    answer = completion['choices'][0]['message']['content']
    print(answer)

    response["template"]["outputs"][0]["simpleText"]["text"] = answer
    return response



def get_answer(request_data):
    user_message = request_data['userRequest']['utterance']
    callback_url = request_data['userRequest']['callbackUrl']

    response_callback = {
        "version": "2.0",
        "useCallback": True,
    }
    asyncio.create_task(send_callback(callback_url, user_message))  # 콜백 요청을 비동기적으로 보냄
    return response_callback

    
async def send_callback(callback_url: str, user_message: str):
    messages = [{'role':'user', 'content':user_message}]
    
    completion = await openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.5,
    )
    gpt_answer = completion['choices'][0]['message']['content']
    print(gpt_answer)
    response["template"]["outputs"][0]["simpleText"]["text"] = gpt_answer
    
    # HTTP 클라이언트를 사용하여 비동기적으로 POST 요청을 보냄
    async with httpx.AsyncClient() as client:
        await client.post(callback_url, json=response)