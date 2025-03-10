from flask import Flask, jsonify, request
from services.table_service import TableService

app = Flask(__name__)
table_service = TableService()

@app.route("/tables", methods=['GET'])
def get_tables():
    return jsonify({"tables" : table_service.get_tables()})

@app.route("/schema/<string:table_name>", methods=['GET'])
def get_table_schema(table_name):
    return jsonify(table_service.get_table_schema(table_name))

@app.route("/data/<string:table_name>", methods=['POST'])
def get_data(table_name):
    if not request.is_json:
        return jsonify({"error": "A requisição deve ser em formato JSON"}), 400
    
    data = request.json.get("columns")
    
    if not data:
        return jsonify({"error": "Nenhuma coluna especificada"}), 400
    return table_service.get_data(table_name, data)

if __name__ == "__main__":
    app.run(debug=True)