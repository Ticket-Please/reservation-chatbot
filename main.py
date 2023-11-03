from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import JSONResponse
from chatGPT.test import test_call

app = FastAPI()

class TestResponseBody(BaseModel):
    test_message:str



@app.post("/")
def 이름():
    return '표주시게'

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
def func():
    return test_call()