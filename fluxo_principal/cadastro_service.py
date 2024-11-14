from flask import Flask, request, jsonify
from services.endereco_logic import buscar_endereco_usuario

app = Flask(__name__)

@app.route('/enderecos', methods=['GET'])
def cadastro_usuario():
    user_id = request.args.get('user_id')
    
    # Converter user_id para int
    try:
        user_id = int(user_id)
    except (ValueError, TypeError):
        return jsonify({"erro": "user_id inválido"}), 400

    try:
        endereco = buscar_endereco_usuario(user_id)
        return jsonify(endereco), 200
    except ValueError as e:
        return jsonify({"erro": str(e)}), 404

if __name__ == '__main__':
    app.run(port=5002, debug=True)
