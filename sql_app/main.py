import requests
import school_api
from typing import Optional
from fastapi import FastAPI, Request, Header, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from database import SessionLocal, engine
import models
from sqlalchemy.orm import Session
import models


# headers = {'Accept': 'application/json'}
# actual_data = requests.get('https://api.nisproject.kz/users/', headers=headers)
#print(f"Response: {actual_data.json()}")

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


templates = Jinja2Templates(directory="templates")

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# @app.on_event("startup")
# async def load():
#     actual_data = await school_api.fetch_data()
#     for student in actual_data:
#         db=SessionLocal()
#         print(student)
#         insert = models.Student(
#             ID = int(student["ID"]),
#             DisplayNameAll = student["DisplayNameAll"],
#             PostName = student["PostName"],
#             DivisionName = student["DivisionName"],
#             # MinIn = student["MinIn"],
#             # MaxIn = student["MaxIn"],
#             # MaxOut = student["MaxOut"],
#             Status = bool(int(student["Status"])),  
#             # DayOut = student["DayOut"],
#             DaysNoInScool = student["DaysNoInScool"],
#             DaysNoOutScool = student["DaysNoOutScool"],
#             Manager = student["Manager"],
#         )
#         db.add(insert)
#         db.commit()


@app.get("/index/", response_class=HTMLResponse)
async def movielist(request: Request, hx_request: Optional[str] = Header(None), db: Session = Depends(get_db)):
    films = db.query(models.Film).all()
    print(films)
    context = {"request": request, 'films': films}
    if hx_request:
        return templates.TemplateResponse("partials/table.html", context)
    return templates.TemplateResponse("index.html", context)

@app.get("/login/", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", context={"request": request})

@app.get("/curator/", response_class=HTMLResponse)
async def curator(request: Request, db: Session = Depends(get_db)):
    students = db.query(models.Student).filter(models.Student.Manager=="Уалиева Сауле Абзаловна").all()
    return templates.TemplateResponse("curator.html", context={"request": request, "students": students})

@app.get("/admin/", response_class=HTMLResponse)
async def admin(request: Request):
    return templates.TemplateResponse("admin.html", context={"request": request})