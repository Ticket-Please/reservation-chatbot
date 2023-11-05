import json
import openai
from fastapi import FastAPI, Request

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



async def get_answer(request_data):
    callback_URL = request_data['userRequest']['callbackUrl']
    prompt = request_data['userRequest']['utterance']
    messages = [{'role':'user', 'content':prompt}]
    
    completion = await openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.5,
    )



    answer = completion['choices'][0]['message']['content']
    print(answer)
    
    response["template"]["outputs"][0]["simpleText"]["text"] = answer

    @app.post("callback_URL")
    def func(request: Request):
        callback_response = {
                                "version" : "2.0",
                                "useCallback" : True,
                                "data": {
                                    "text" : "생각하고 있는 중이에요😘 \n15초 정도 소요될 거 같아요 기다려 주실래요?!"
                                }
                            }
        return callback_response
    
    return response

