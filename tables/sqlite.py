import sqlite3


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        # connection.set_trace_callback(logger)  # Bu xatolikka sabab bo'lishi mumkin
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE Users (
            id int NOT NULL ,
            Name varchar(255) NOT NULL,
            language varchar(3),
            phone  varchar(30) NULL,
            kirim int NULL,
            chiqim int NULL,
            PRIMARY KEY (id)
            );
        """
        self.execute(sql, commit=True)

    def create_table_kirim(self):
        sql = """
        CREATE TABLE Kirim (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            summa varchar(255) NOT NULL,
            izoh varchar(255) NULL,
            kategoriya varchar(255),
            user_id int NOT NULL
            
            );
        """
        self.execute(sql, commit=True)
    def create_table_chiqim(self):
        sql = """
        CREATE TABLE Chiqim (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            summa varchar(255) NOT NULL,
            izoh varchar(3) NULL,
            kategoriya varchar(255),
            user_id int NOT NULL
            
            );
        """
        self.execute(sql, commit=True)
    
    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_user(self, id: int, name: str, language: str = 'uz', phone: str = None, kirim: int = None, chiqim: int = None): # pyright: ignore[reportArgumentType]
        # SQL_EXAMPLE = "INSERT INTO Users(id, Name, email) VALUES(1, 'John', 'John@gmail.com')"
        
        sql = """
        INSERT INTO Users(id, Name, language, phone, kirim, chiqim) VALUES(?, ?, ?, ?, ?, ?)
        """
        self.execute(sql, parameters=(id, name, language, phone, kirim, chiqim), commit=True)

    def add_chiqim(self,  summa: str, izoh: str, kategoriya: str, user_id: int ): # pyright: ignore[reportArgumentType]
            # SQL_EXAMPLE = "INSERT INTO Users(id, Name, email) VALUES(1, 'John', 'John@gmail.com')"
            
            sql = """
            INSERT INTO Chiqim(summa, izoh, kategoriya, user_id) VALUES(?, ?, ?, ?)
            """
            self.execute(sql, parameters=(summa, izoh, kategoriya, user_id), commit=True)

    def add_kirim(self, summa: str, izoh: str, kategoriya: str, user_id: int): # pyright: ignore[reportArgumentType]
        sql = """
        INSERT INTO Kirim(summa, izoh, kategoriya, user_id) VALUES(?, ?, ?, ?)
        """
        self.execute(sql, parameters=(summa, izoh, kategoriya, user_id), commit=True)

    def select_all_users(self):
        sql = """
        SELECT * FROM Users
        """
        return self.execute(sql, fetchall=True)

    def select_user(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    def update_user_phone(self, phone, id):
        # SQL_EXAMPLE = "UPDATE Users SET email=mail@gmail.com WHERE id=12345"

        sql = f"""
        UPDATE Users SET phone=? WHERE id=?
        """
        return self.execute(sql, parameters=(phone, id), commit=True)

    def delete_users(self):
        self.execute("DELETE FROM Users WHERE TRUE", commit=True)

    def get_user_chiqimlar(self, user_id: int):
        """Foydalanuvchining chiqimlarini olish"""
        sql = "SELECT * FROM Chiqim WHERE user_id = ? ORDER BY id DESC"
        return self.execute(sql, parameters=(user_id,), fetchall=True)

    def get_user_kirimlar(self, user_id: int):
        """Foydalanuvchining kirimlarini olish"""
        sql = "SELECT * FROM Kirim WHERE user_id = ? ORDER BY id DESC"
        return self.execute(sql, parameters=(user_id,), fetchall=True)

    def get_user_total_chiqim(self, user_id: int):
        """Foydalanuvchining jami chiqimini hisoblash"""
        sql = "SELECT SUM(CAST(summa AS INTEGER)) FROM Chiqim WHERE user_id = ?"
        result = self.execute(sql, parameters=(user_id,), fetchone=True)
        return result[0] if result[0] else 0

    def get_user_total_kirim(self, user_id: int):
        """Foydalanuvchining jami kirimini hisoblash"""
        sql = "SELECT SUM(CAST(summa AS INTEGER)) FROM Kirim WHERE user_id = ?"
        result = self.execute(sql, parameters=(user_id,), fetchone=True)
        return result[0] if result[0] else 0


def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")