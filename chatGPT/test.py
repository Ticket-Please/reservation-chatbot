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

    completion = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = completion.choices[0].text
    print(message)
    response["template"]["outputs"][0]["simpleText"]["text"] = message
    return response


def get_answer(request_data):
    print(request_data)
    params = request_data['userRequest']['utterance']
    print(params)

    # prompt = request.get_data()

    # completion = openai.Completion.create(
    #     model="text-davinci-003",
    #     prompt=prompt,
    #     max_tokens=100,
    #     n=1,
    #     stop=None,
    #     temperature=0.5,
    # )

    # message = completion.choices[0].text
    # print(message)
    # response["template"]["outputs"][0]["simpleText"]["text"] = message
    # return response