import mysql.connector
from flask import jsonify
from dotenv import load_dotenv
import os

load_dotenv()

class DB_ORM:
    def __init__(self):
        self.connection = None

    def get_connection(self):
        if self.connection is None or self.connection.is_connected():
            try:
                self.connection = mysql.connector.connect(
                    host=os.getenv("DB_HOST"),
                    user=os.getenv("DB_USER"),
                    password=os.getenv("DB_PASSWORD"),
                    database=os.getenv("DB_NAME")
                )
            except mysql.connector.Error as e:
                print(f"Erro ao conectar ao banco de dados: {e}")
                return None
        return self.connection

    def get_tables(self):
        conn = self.get_connection()

        if not conn:
            return jsonify({"error": "Erro na conexão com o banco"}), 500

        try:
            cursor = conn.cursor()
            
            cursor.execute("SHOW TABLES")
            tables = [table[0] for table in cursor.fetchall()]

            cursor.close
            return ", ".join(tables)
        except mysql.connector.Error as e:
            return jsonify({"error" : "Erro ao obter tabelas"})        

    def get_table_schema(self, table_name):
        conn = self.get_connection()
        if not conn:
            return jsonify({"error" : "Erro na conexão com o banco"}), 500
        
        try:
            cursor = conn.cursor()
            
            cursor.execute(f"SHOW COLUMNS FROM {table_name}")
            table_schema = [title for title in cursor.fetchall()]
            
            cursor.close()
            
            table_dict = {}
            for column in table_schema:
                column_name, column_type, is_nullable, key, default, extra = column
                table_dict[column_name] = {
                    "Tipo": column_type,
                    "Null": is_nullable,
                    "Key": key,
                    "Default": default,
                    "Extra": extra
                }
            
            return table_dict
        except mysql.connector.Error as e:
            return jsonify({"error" : "Erro na conexão com o banco"}), 500