from flask import Flask, request, jsonify
from services.estoque_logic import calcular_disponibilidade

app = Flask(__name__)

# Simula um estoque como um banco de dados sintético
estoque = {
    "001": {"quantidade": 10},
    "002": {"quantidade": 5},
    "003": {"quantidade": 15}
}

@app.route('/verificar_estoque', methods=['POST'])
def verificar_estoque():
    resumo = request.json

    produtos_disponiveis = calcular_disponibilidade(estoque, resumo["itens"])
    if produtos_disponiveis:
        return jsonify({"status": "disponível"}), 200
    else:
        return jsonify({"status": "indisponível"}), 200
    

@app.route('/reduzir_estoque', methods=['POST'])
def reduzir_estoque():
    resumo = request.json

    itens = resumo["itens"]
    for item in itens:
        item_id = item["produto_id"]
        quantidade = item["quantidade"]

        if item_id not in estoque:
            return jsonify({"erro": "item não encontrado"}), 404

        if estoque[item_id]["quantidade"] < quantidade:
            return jsonify({"erro": "quantidade insuficiente"}), 400

        estoque[item_id]["quantidade"] -= quantidade

    return jsonify({"status": "estoque atualizado"}), 200


if __name__ == '__main__':
    app.run(port=5001, debug=True)
