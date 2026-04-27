
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi import FastAPI,HTTPException
import uvicorn
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client,Client
from message_api import api
SECRET_KEY = "sb_secret_AZM7ADduXmdR_nqsTp920Q_-4TsVLuE"
PROJECT_URL = "https://ajjbldcfukrjzivigcfq.supabase.co"
app = FastAPI()
current_dir = os.path.dirname(os.path.realpath(__file__))
frontend_path = os.path.join(current_dir, "..", "frontend")

frontend_path = os.path.join(BASE_DIR, "frontend")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)
supabase: Client = create_client(PROJECT_URL,SECRET_KEY)
class Register(BaseModel):
    email: str
    password: str
class Message(BaseModel):
    message: str
@app.get("/")
async def read_index():
    return FileResponse(os.path.join(frontend_path, 'register.html'))
@app.post("/register")
async def regist(user: Register):
    print(f"получены данные,{user.email},{user.password}")
    data_from_table = supabase.table('users').select('email').eq('email',user.email).execute()
    if data_from_table.data:
        raise HTTPException(status_code=400, detail="email already exists")
    supabase.table('users').insert({'email':user.email,"password": user.password }).execute()
    return {"message": "ok"}
@app.post("/enter")
async def enter(user: Register):
    print(f"логин попытка: {user.email}, {user.password}")
    user_email = supabase.table('users').select('email, password').eq('email',user.email).execute()
    if user_email.data and user_email.data[0]["password"] == user.password:
        return {"message": "login success","success": True,"email": user.email}
    raise HTTPException(status_code=400,detail="Email or password is not correct")
@app.post("/chat")
async def chat(data: Message):
    print("Получено:", data.message)
    response = api.chat_api.send_message(data.message)
    if response == []:
        return {
        "reply": 'More words please'
    }
    translate = response[1]
    response = response[0]
    return {
        "reply": response + f"\nTranslate: {translate}"
    }
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")

