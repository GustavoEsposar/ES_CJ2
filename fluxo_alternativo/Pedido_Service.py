from flask import Flask, jsonify, request, render_template
from flask import Flask, jsonify, request
from database.db_connection import get_collection, get_comprador_id, atualizar_quantidade
from model.payment_method import MetodoPagamento 

app = Flask(__name__)

@app.route("/checkout/carrinho_painel", methods=["GET"])
def obter_formulario_endereco():
    # Renderiza o formulário HTML para o novo endereço
    return render_template("index2.html")

def calcularResumoDoCarrinho(carrinho):
    total = sum(item['preco'] * item['quantidade'] for item in carrinho)
    return {"itens": carrinho, "total": total}

@app.route('/checkout/carrinho', methods=['GET'])
def ver_carrinho():
    comprador_id = get_comprador_id("profe@palito.com")
    
    if not comprador_id:
        return jsonify({"mensagem": "Comprador não encontrado"}), 404

    carrinho_collection = get_collection("carrinho")
    carrinho = carrinho_collection['itens']

    carrinho_detalhado = [{"id": str(item["_id"]), "nome": item["nome"], "preco": item["preco"], "quantidade": item["quantidade"]} for item in carrinho]
    resumo = calcularResumoDoCarrinho(carrinho_detalhado)
    
    return jsonify(resumo), 200

@app.route('/checkout/modificar-quantidade', methods=['POST'])
def modificar_quantidade():
    data = request.json
    item_id = data["item_id"]
    nova_quantidade = data["quantidade"]

    comprador_id = get_comprador_id("profe@palito.com")
    if not comprador_id:
        return jsonify({"mensagem": "Comprador não encontrado"}), 404

    atualizar_quantidade(item_id, nova_quantidade)

    carrinho_collection = get_collection("carrinho")
    carrinho = carrinho_collection['itens']
    carrinho_detalhado = [{"id": str(item["_id"]), "nome": item["nome"], "preco": item["preco"], "quantidade": item["quantidade"]} for item in carrinho]
    resumo = calcularResumoDoCarrinho(carrinho_detalhado)
    
    return jsonify(resumo), 200

@app.route('/checkout/fechar-pedido', methods=['POST'])
def fechar_pedido():
    data = request.json

    comprador_id = get_comprador_id("profe@palito.com")
    if not comprador_id:
        return jsonify({"mensagem": "Comprador não encontrado"}), 404

    # Aqui você pode incluir a lógica para iniciar o processo de pagamento e finalizar o pedido
    return jsonify({"status": "Pedido finalizado com sucesso"}), 200

def debitarPagamento(payment_method: MetodoPagamento):
    print("Pagamento OK")
    return 200

def confirmarReducaoNoEstoque():
    print("Retirada do estoque OK")
    return 200

@app.route('/checkout/detalhes-da-compra', methods=['POST'])
def checkout_compra():
    data = request.json
    order_id = data["order_id"]
    payment_method = data["payment_method"]
    amount = data["amount"]

    paymentMethod = MetodoPagamento(payment_method)

    if paymentMethod.verificar() == True:
        response = debitarPagamento(order_id, paymentMethod, amount)

        if response == 200:
            confirmarReducaoNoEstoque()
            return jsonify({"status": 200, "mensagem": "Compra realizada com sucesso"}), 200
        
    else: return jsonify({"status": 503, "mensagem": "Metodo de pagamento indisponível"}), 503

if __name__ == '__main__':
    app.run(port=5000)
