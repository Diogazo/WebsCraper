from fastapi import FastAPI, Request, Response, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.controller.user import User
from app.lib.check_passw import check_user
from app.lib.scraper import scrape_prices

app = FastAPI()

# Directorio para las plantillas HTML
template = Jinja2Templates(directory="app/view")


@app.get("/", response_class=HTMLResponse)
def root(req: Request):
    return template.TemplateResponse("index.html", {"request": req})


@app.get("/signup", response_class=HTMLResponse)
def signup(req: Request):
    return template.TemplateResponse("signup.html", {"request": req})


@app.get("/login", response_class=HTMLResponse)
def login(req: Request):
    return template.TemplateResponse("login.html", {"request": req})


@app.post("/login", response_class=HTMLResponse)
def login_post(req: Request, email: str = Form(), password_user: str = Form()):
    verify = check_user(email, password_user)
    if isinstance(verify, dict):  # Si es un diccionario, la autenticación es correcta
        response = RedirectResponse(url="/user", status_code=303)
        response.set_cookie(key="user_email", value=email)  # Guardar el email en cookies
        return response
    return template.TemplateResponse("login.html", {"request": req, "error": "Credenciales incorrectas"})


@app.get("/user", response_class=HTMLResponse)
def user(req: Request):
    user_email = req.cookies.get("user_email")  # Obtener email desde cookies

    if not user_email:  # Si no hay sesión, redirigir a login
        return RedirectResponse("/login")

    user_data = check_user(user_email)  # Obtener datos del usuario autenticado
    if not user_data:  # Si no hay datos del usuario
        return RedirectResponse("/login")

    return template.TemplateResponse("user.html", {"request": req, "data_user": user_data})


@app.post("/user", response_class=HTMLResponse)
def user_post(req: Request, email: str = Form(), password_user: str = Form()):
    verify = check_user(email, password_user)
    if isinstance(verify, dict):  # Si es un diccionario, autenticación correcta
        return template.TemplateResponse("user.html", {"request": req, "data_user": verify})
    return template.TemplateResponse("login.html", {"request": req, "error": "Credenciales incorrectas"})



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

    # Redirigir a la página principal con una cookie de confirmación
    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie(key="registration_success", value="true", max_age=5)  # La cookie expira en 5 segundos
    return response

# Nuevo endpoint: Web scraping
@app.get("/scrape-prices", response_class=HTMLResponse)
def scrape_prices_endpoint(req: Request, search: str):
    results = scrape_prices(search)
    return template.TemplateResponse(
        "scrape_results.html", {"request": req, "products": results, "search": search}
    )
