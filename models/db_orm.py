from config.database import Database
from flask import jsonify

class DBORM:
    def __init__(self):
        self.connection = Database.get_connection()
        
    def execute_query(self, query: str, fetch=True, values=None):
        if not self.connection:
            return jsonify({"error": "Erro na conexão com o banco"}), 500
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, values or ())
            
            if fetch:
                result = cursor.fetchall()
            else:
                self.connection.commit()
                result = cursor.lastrowid
            cursor.close()
            return result
        
        except mysql.connector.Error as e:
            return jsonify({"error" : f"Erro ao executar a query: {e}"}), 500
        