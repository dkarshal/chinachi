import requests
import school_api
from typing import Optional
from fastapi import FastAPI, Request, Header, Depends
from fastapi.responses import HTMLResponse
from fastapi.exceptions import HTTPException
from fastapi.templating import Jinja2Templates
from database import SessionLocal, engine
import models
from sqlalchemy.orm import Session


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

@app.on_event("startup")
async def load():
    db=SessionLocal()
    db.query(models.Student).delete()
    db.commit()
    actual_data = await school_api.fetch_data()
    for student in actual_data:
        insert = models.Student(
            ID = int(student["ID"]),
            DisplayNameAll = student["DisplayNameAll"],
            PostName = student["PostName"],
            DivisionName = student["DivisionName"],
            # MinIn = student["MinIn"],
            # MaxIn = student["MaxIn"],
            # MaxOut = student["MaxOut"],
            Status = bool(int(student["Status"])),  
            # DayOut = student["DayOut"],
            DaysNoInScool = student["DaysNoInScool"],
            DaysNoOutScool = student["DaysNoOutScool"],
            Manager = student["Manager"],
        )
        db.add(insert)
    db.commit()



@app.get("/index/", response_class=HTMLResponse)
async def movielist(request: Request, hx_request: Optional[str] = Header(None), db: Session = Depends(get_db)):
    films = db.query(models.Film).all()
    print(films)
    context = {"request": request, 'films': films}
    if hx_request:
        return templates.TemplateResponse("partials/table.html", context)
    return templates.TemplateResponse("index.html", context)

@app.get("/")
def read_root():
    return {"msg": "hi, route to /docs"}

@app.get("/login")
def login(request: Request):
    return templates.TemplateResponse("login.html", context={"request": request})

@app.post("/redirect")
async def redirect(username: str, password: str, request: Request):
    if username == "admin" and password == "1":
        return templates.TemplateResponse("admin.html", context={"request": request})
    elif username == "curator" and password == "1":
        return templates.TemplateResponse("curator.html", context={"request": request})
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")

@app.get("/curator/{username}", response_class=HTMLResponse)
async def curator(username: str, request: Request, db: Session = Depends(get_db)):
    students = db.query(models.Student).filter(models.Student.Manager==username).all()
    for student in students:
        if student.Status is True:
            student.color = "bg-green-700"
            student.marked = "marked"
        else:
            student.color = "bg-red-700"
            student.marked = ""
    return templates.TemplateResponse("curator.html", context={"request": request, "students": students, "classes": await users_class(username, db)})

async def users_class(username, db):
    classes = db.query(models.Student.DivisionName).filter(models.Student.Manager==username).all()
    classes = list(map(lambda x: x[0],list({*classes})))
    return classes

@app.post("/update_database/{student_id}")
async def update_database(student_id: str, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.ID == student_id).first()
    if student:
        student.Status = not (student.Status)  # Update the 'Status' field with the new value

        # Step 3: Commit the Changes
        db.commit()
        db.refresh(student)
        return {"message": "Student record updated successfully"}
    else:
        return {"message": "Student record wasn't updated successfully"}


@app.get("/admin/", response_class=HTMLResponse)
async def admin(request: Request, hx_request: Optional[str] = Header(None), db: Session = Depends(get_db)):
    classes = db.query(models.Student.DivisionName, models.Student.Manager).all()
    # Assuming classes is a list of tuples like [(division_name1, manager1, status1), ...]
    #classes = sorted(list({(Division, Manager, Status) for Division, Manager, Status in classes}), key=lambda x: x[0])
    print(classes)
    classes = sorted(list({*classes}))
    if hx_request:
        return templates.TemplateResponse("partials/classes_card.html", context={"request": request, "classes": classes})
    return templates.TemplateResponse("admin.html", context={"request": request, "classes": classes})

@app.get("/inschool-class-students/{division_name}")
def get_class_students(division_name: str, db: Session = Depends(get_db)):
    inclass_students = db.query(models.Student.DivisionName, models.Student.Status).filter(models.Student.DivisionName == division_name, models.Student.Status==True).count()
    return inclass_students

@app.get("/outschool-class-students/{division_name}")
def get_class_students(division_name: str, db: Session = Depends(get_db)):
    outclass_students = db.query(models.Student.DivisionName, models.Student.Status).filter(models.Student.DivisionName+"2" == division_name, models.Student.Status==False).count()
    return outclass_students