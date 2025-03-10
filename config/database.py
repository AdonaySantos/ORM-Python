import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    _connection = None
    
    @staticmethod
    def get_connection():
        if Database._connection is None or Database._connection.is_connected():
            try:
                Database._connection = mysql.connector.connect(
                    host=os.getenv("DB_HOST"),
                    user=os.getenv("DB_USER"),
                    password=os.getenv("DB_PASSWORD"),
                    database=os.getenv("DB_NAME")
                )
            except mysql.connector.Error as e:
                print(f"Erro ao conectar ao banco de dados: {e}")
                return None
        return Database._connection