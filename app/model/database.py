import os
import mysql.connector

class Database:
    def __init__(self):
        try:
            self._con = mysql.connector.connect(
                host=os.getenv("DB_HOST", "localhost"),
                user=os.getenv("DB_USER", "root"),
                password=os.getenv("DB_PASS", "Diogazo045."),
                database=os.getenv("DB_NAME", "webscrapper"),
                port=int(os.getenv("DB_PORT", 3306))
            )
            self._cur = self._con.cursor(dictionary=True)
        except mysql.connector.Error as e:
            print(f"Error al conectar a MySQL: {e}")
            self._con = None

    def get_all(self):
        if not self._con:
            return []
        try:
            self._cur.execute("SELECT * FROM users")
            return self._cur.fetchall()
        except mysql.connector.Error as e:
            print(f"Error al obtener datos: {e}")
            return []

    def get_only(self, email):
        if not self._con:
            return None
        try:
            self._cur.execute("SELECT * FROM users WHERE email = %s", (email,))
            return self._cur.fetchone()
        except mysql.connector.Error as e:
            print(f"Error al obtener usuario: {e}")
            return None

    def insert(self, data_user):
        if not self._con:
            return
        try:
            sql = """
                INSERT INTO users (firstname, email, phone_number, province, city, password_user) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (
                data_user["firstname"],
                data_user["email"],
                data_user["phone_number"],
                data_user["province"],
                data_user["city"],
                data_user["password_user"]
            )
            self._cur.execute(sql, values)
            self._con.commit()
        except mysql.connector.Error as e:
            print(f"Error en la inserción: {e}")

    def get_user_by_token(self, token: str):
        if not self._con:
            return None
        try:
            self._cur.execute("SELECT * FROM users WHERE token = %s", (token,))
            return self._cur.fetchone()
        except mysql.connector.Error as e:
            print(f"Error al obtener usuario por token: {e}")
            return None

    def add_favorite(self, user_email: str, product_id: str):
        if not self._con:
            return
        try:
            sql = "INSERT INTO favorites (user_email, product_id) VALUES (%s, %s)"
            self._cur.execute(sql, (user_email, product_id))
            self._con.commit()
        except mysql.connector.Error as e:
            print(f"Error al agregar favorito: {e}")

    def update_profile(self, user_email: str, name: str, email: str, password: str):
        if not self._con:
            return
        try:
            sql = "UPDATE users SET firstname = %s, email = %s, password_user = %s WHERE email = %s"
            self._cur.execute(sql, (name, email, password, user_email))
            self._con.commit()
        except mysql.connector.Error as e:
            print(f"Error al actualizar el perfil: {e}")

    def get_products_by_category(self, category_name: str):
        if not self._con:
            return []
        try:
            self._cur.execute("SELECT * FROM products WHERE category = %s", (category_name,))
            return self._cur.fetchall()
        except mysql.connector.Error as e:
            print(f"Error al obtener productos: {e}")
            return []

    def close(self):
        if self._con and self._con.is_connected():
            self._cur.close()
            self._con.close()

from app.model.database import Database

# Crear una instancia de la clase Database
db = Database()
