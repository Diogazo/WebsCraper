from werkzeug.security import check_password_hash
from app.model.database import Database  # Se corrige la importación

def check_user(email, passw=None):
    db = Database()  # Crea una instancia de la base de datos
    filter_user = db.get_only(email)  # Busca el usuario por email

    if not filter_user:  # Si el usuario no existe, retorna False
        return False

    if passw is None:  # Si no se envió una contraseña, solo devuelve los datos del usuario
        return filter_user

    # Verifica la contraseña
    if check_password_hash(filter_user["password_user"], passw):
        return filter_user  # Devuelve los datos del usuario si la contraseña es válida
    return False  # Devuelve False si la contraseña no coincide