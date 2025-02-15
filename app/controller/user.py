from app.model.database import Database
from werkzeug.security import generate_password_hash

class User():
    def __init__(self, data_user):
        self.db = Database()  # Se cambia HandleDB por Database
        self.data_user = data_user

    def create_user(self):
        self._add_id()  # Agrega un ID único
        self._passw_encrypt()  # Encripta la contraseña
        self.db.insert(self.data_user)  # Guarda el usuario en la BD

    def _add_id(self):
        users = self.db.get_all()  # Obtiene todos los usuarios
        if users:  # Si hay usuarios en la base de datos
            last_id = max(int(user["id"]) for user in users)  # Encuentra el ID más alto
        else:
            last_id = 0  # Si no hay usuarios, empieza desde 1

        self.data_user["id"] = str(last_id + 1)  # Se asegura de que sea una cadena

    def _passw_encrypt(self):
        self.data_user["password_user"] = generate_password_hash(
            self.data_user["password_user"], method="pbkdf2:sha256", salt_length=16
        )  # Configuración más estándar
