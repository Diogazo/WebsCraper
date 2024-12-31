from fastapi import FastAPI, Request, Response, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from controller.user import User
from lib.check_passw import check_user

app = FastAPI()

template = Jinja2Templates(directory="./view")

@app.get("/", response_class=HTMLResponse)
def root(req: Request):
    return template.TemplateResponse("index.html", {"request": req})

@app.post("/", response_class=HTMLResponse)
def root(req: Request):
    return template.TemplateResponse("index.html", {"request": req})

@app.get("/signup", response_class=HTMLResponse)
def signup(req: Request):
    return template.TemplateResponse("signup.html", {"request": req})

@app.get("/user", response_class=HTMLResponse)
def user(req: Request):
    return RedirectResponse("/")
    #return template.TemplateResponse("user.html", {"request": req})

@app.post("/user", response_class=HTMLResponse)
def user(req: Request, email: str = Form(), password_user: str = Form()):
    verify = check_user(email, password_user)
    if verify:
        return template.TemplateResponse("user.html", {"request": req, "data_user": verify})
    return RedirectResponse("/")

@app.post("/data-processing")
def data_processing(
    firstname: str = Form(),
    email: str = Form(),
    phone_number: str = Form(),
    province: str = Form(),
    city: str = Form(),
    password_user: str = Form()
    ):
    data_user = {
        "firstname": firstname,
        "email": email,
        "phone_number": phone_number,
        "province": province,
        "city": city,
        "password_user": password_user
    }
    db = User(data_user)
    db.create_user()

    return RedirectResponse("/")