from fastapi import FastAPI, Request, Response, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles
from app.controller.user import User
from app.lib.check_passw import check_user
from app.lib.scraper import scrape_prices
from app.model.database import Database as db

app = FastAPI()
templates = Jinja2Templates(directory="app/view")

# Montar la carpeta 'static' para servir archivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    user = db.get_user_by_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no autenticado",
        )
    return user

@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/signup", response_class=HTMLResponse)
def signup(req: Request):
    return templates.TemplateResponse("signup.html", {"request": req})

@app.get("/login", response_class=HTMLResponse)
def login(req: Request):
    return templates.TemplateResponse("login.html", {"request": req})

@app.post("/login", response_class=HTMLResponse)
def login_post(req: Request, email: str = Form(), password_user: str = Form()):
    verify = check_user(email, password_user)
    if isinstance(verify, dict):  # Si es un diccionario, la autenticación es correcta
        response = RedirectResponse(url="/user", status_code=303)
        response.set_cookie(key="user_email", value=email)  # Guardar el email en una cookie
        return response
    return templates.TemplateResponse("login.html", {"request": req, "error": "Credenciales incorrectas"})

@app.get("/user", response_class=HTMLResponse)
def user(req: Request):
    user_email = req.cookies.get("user_email")  # Obtener el email desde la cookie

    if not user_email:  # Si no hay sesión, redirigir a login
        return RedirectResponse("/login")

    user_data = check_user(user_email)  # Obtener datos del usuario autenticado
    if not user_data:  # Si no hay datos del usuario
        return RedirectResponse("/login")

    is_logged_in = True  # El usuario ha iniciado sesión
    return templates.TemplateResponse("user.html", {"request": req, "data_user": user_data, "is_logged_in": is_logged_in})

@app.post("/user", response_class=HTMLResponse)
def user_post(req: Request, email: str = Form(), password_user: str = Form()):
    verify = check_user(email, password_user)
    if isinstance(verify, dict):  # Si es un diccionario, autenticación correcta
        return templates.TemplateResponse("user.html", {"request": req, "data_user": verify})
    return templates.TemplateResponse("login.html", {"request": req, "error": "Credenciales incorrectas"})

@app.post("/update-profile")
def update_profile(
    name: str = Form(),
    email: str = Form(),
    password: str = Form(),
    user_email: str = Depends(get_current_user)
):
    db.update_profile(user_email, name, email, password)
    return {"message": "Perfil actualizado"}

@app.get("/category/{category_name}")
def category_page(req: Request, category_name: str):
    products = db.get_products_by_category(category_name)
    return templates.TemplateResponse(
        "category.html", {"request": req, "category": category_name, "products": products}
    )

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

@app.get("/scrape-prices", response_class=HTMLResponse)
def scrape_prices_endpoint(req: Request, search: str):
    results = scrape_prices(search)[:4]  # Limitar a 4 resultados
    return templates.TemplateResponse(
        "scrape_results.html", {"request": req, "products": results, "search": search}
    )

@app.post("/favorite/{product_id}")
def add_favorite(product_id: str, user_email: str = Depends(get_current_user)):
    add_favorite(user_email, product_id)
    return {"message": "Producto agregado a favoritos"}

@app.get("/product/{product_id}", response_class=HTMLResponse)
async def read_product(request: Request, product_id: int):
    # Aquí deberías obtener los detalles del producto desde la base de datos
    product_details = {
        1: {
            "product_name": "Alexa Echo Dot",
            "product_image": "/static/images/imagen1.jpg",
            "product_price": "$45.99",
            "product_availability": "In Stock",
            "product_description": "Descripción del Alexa Echo Dot."
        },
        2: {
            "product_name": "Pc Gaming",
            "product_image": "/static/images/imagen2.jpg",
            "product_price": "$899.99",
            "product_availability": "In Stock",
            "product_description": "Descripción del Pc Gaming."
        },
        3: {
            "product_name": "Iphone 16 Blue Sky",
            "product_image": "/static/images/imagen3.jpg",
            "product_price": "$1200",
            "product_availability": "In Stock",
            "product_description": "Descripción del Iphone 16 Blue Sky."
        }
    }
    product = product_details.get(product_id, None)
    if product:
        return templates.TemplateResponse("product_detail.html", {"request": request, **product})
    else:
        return HTMLResponse(content="Producto no encontrado", status_code=404)

@app.get("/logout", response_class=RedirectResponse)
def logout():
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie(key="user_email")  # Eliminar la cookie
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")