import json
import openai


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


    response = completion['choices'][0]['message']['content']
    print(response)
    return response


def get_answer(request_data):
    prompt = request_data['userRequest']['utterance']
    messages = [{'role':'user', 'content':prompt}]
    
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.5,
    )

    response = completion['choices'][0]['message']['content']
    print(response)
    return response

