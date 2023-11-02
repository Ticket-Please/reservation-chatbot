from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def 이름():
  return '표주시게'