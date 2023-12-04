from fastapi import FastAPI, Request
from pydantic import BaseModel
from starlette.responses import JSONResponse
from chatGPT.test import test_call, get_early_answer, test_db_save, test_db_load
import json

app = FastAPI()

class TestResponseBody(BaseModel):
    test_message:str

with open('./schema.json', encoding='utf-8') as f:
    schema = json.loads(f.read())
dummyUserAPI = schema['dummyUserAPI']

@app.post("/")
def 이름():
    return 'post표주시게'
@app.get("/")
def 이름():
    return 'get표주시게'

@app.post("/test", response_class=TestResponseBody)
def 이름():
    result = {
        "test_message":"안녕하세용가리"
    }
    return JSONResponse(result)

@app.post("/test/kakao")
def 이름():
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
    return JSONResponse(response)

@app.post('/chatgpt')
async def func(request: Request):
    json_data = await request.json()
    return test_call(json_data)

@app.post('/saveTest')
async def func():
    return test_db_save(dummyUserAPI)

@app.post('/loadTest')
def func():
    user_id = dummyUserAPI['userRequest']['user']['id']
    return test_db_load(user_id)

# 이게 진짜!
@app.post('/question')
async def func(request: Request):
    json_data = await request.json()
    return get_early_answer(json_data)