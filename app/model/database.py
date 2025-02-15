import mysql.connector

class Database():
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

    def __del__(self):  
        if self._con and self._con.is_connected():
            self._cur.close()
            self._con.close()
