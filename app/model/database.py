import mysql.connector

class Database:
    def __init__(self):
        try:
            self._con = mysql.connector.connect(
                host="localhost",      
                user="root",    
                password="Diogazo045.",  
                database="webscrapper",
                port=3307  
            )
            self._cur = self._con.cursor(dictionary=True)  
        except mysql.connector.Error as e:
            print(f"Error al conectar a MySQL: {e}")
            self._con = None

    def get_all(self):
        if self._con:
            self._cur.execute("SELECT * FROM users")
            return self._cur.fetchall()
        return []

    def get_only(self, email):
        if self._con:
            self._cur.execute("SELECT * FROM users WHERE email = %s", (email,))
            return self._cur.fetchone()
        return None

    def insert(self, data_user):
        if self._con:
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
        if self._con:
            self._cur.execute("SELECT * FROM users WHERE token = %s", (token,))
            return self._cur.fetchone()
        return None
    
    def add_favorite(self, user_email: str, product_id: str):
        if self._con:
            try:
                sql = "INSERT INTO favorites (user_email, product_id) VALUES (%s, %s)"
                values = (user_email, product_id)
                self._cur.execute(sql, values)
                self._con.commit()
            except mysql.connector.Error as e:
                print(f"Error al agregar favorito: {e}")

    def update_profile(self, user_email: str, name: str, email: str, password: str):
        if self._con:
            try:
                sql = "UPDATE users SET firstname = %s, email = %s, password_user = %s WHERE email = %s"
                values = (name, email, password, user_email)
                self._cur.execute(sql, values)
                self._con.commit()
            except mysql.connector.Error as e:
                print(f"Error al actualizar el perfil: {e}")

    def get_products_by_category(self, category_name: str):
        if self._con:
            self._cur.execute("SELECT * FROM products WHERE category = %s", (category_name,))
            return self._cur.fetchall()
        return []

    def __del__(self):  
        if self._con and self._con.is_connected():
            self._cur.close()
            self._con.close()

db = Database()