import json
import openai
import httpx
import asyncio
from pymongo import MongoClient

with open('./secret.json', encoding='utf-8') as f:
    secrets = json.loads(f.read())
API_KEY = secrets["ChatGPT-key"]
MONGO_URI = secrets["MONGO_URI"]

openai.api_key = API_KEY
mongoose = MongoClient(MONGO_URI)
db = mongoose['TicketPlz']
collection = db['userMessages']

with open('./schema.json', encoding='utf-8') as f:
    schema = json.loads(f.read())
response = schema['response']
response_callback = schema['response_callback']


# 테스트 함수들
def test_call(request_data):
    user_message = "기차 예매를 하는 방법을 쉽게 설명해줘"
    callback_url = request_data['userRequest']['callbackUrl']
    asyncio.create_task(get_real_answer(callback_url, user_message))
    return response_callback

def test_db_save(request_data):
    user_message = request_data['userRequest']['utterance']
    user_id = request_data['userRequest']['user']['id']
    print(user_message)
    collection.insert_one({'user_id':user_id, 'role':'user', 'content':user_message})
    return {"굿굿"}

def test_db_load(user_id: str):
    messages = []
    conversations = collection.find({"user_id":user_id})
    for converstaion in conversations:
        del converstaion['_id']
        print(converstaion)
        messages.append(converstaion)
    print(messages)
    return messages

# 여기부터 진짜!
def get_early_answer(request_data):
    asyncio.create_task(get_real_answer(request_data))
    return response_callback

async def get_real_answer(request_data):
    # 유저 대화 DB저장
    user_message = request_data['userRequest']['utterance']
    user_id = request_data['userRequest']['user']['id']
    callback_url = request_data['userRequest']['callbackUrl']
    collection.insert_one({'user_id':user_id, 'role':'user', 'content':user_message})

    # DB에서 대화들 불러와 매개변수에 넣기
    role_message = {"role": "system",
                "content": "You are a capable assistant who finds and books suitable trains for the user."}
    messages = []
    conversations = collection.find({"user_id":user_id})
    conversationCount = 0
    for conversation in conversations:
        if conversationCount % 10 == 0:
            messages.append(role_message)
        del conversation['_id']
        del conversation['user_id']
        messages.append(conversation)

    # gpt답변 생성
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.5,
    )

    # gpt답변 DB에 저장
    gpt_answer = completion['choices'][0]['message']['content']
    collection.insert_one({'user_id':user_id, 'role':'system', 'content':gpt_answer})

    # HTTP 클라이언트를 사용하여 비동기적으로 POST 요청을 보냄
    response["template"]["outputs"][0]["simpleText"]["text"] = gpt_answer
    async with httpx.AsyncClient() as client:
        await client.post(callback_url, json=response)