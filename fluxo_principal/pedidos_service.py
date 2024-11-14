from flask import Flask, request, jsonify
import requests
from services.pedidos_logic import calcular_resumo_do_carrinho
from API_transporte import ApiTranporte

app = Flask(__name__)

carteira_usuario = {
    "1": {"metodos": [
        'cartao_credito', 'cartao_debito', 'boleto'
    ]},
    "2": {"metodos": [
        'cartao_credito', 'cartao_debito'
    ]},
    "3": {"metodos": [
        'cartao_credito'
    ]}
}


resumo_pedido = {
    "user_id": "1",
    "itens": [
      {
        "nome": "item1",
        "preco_unitario": 10.99,
        "produto_id": "001",
        "quantidade": 2
      },
      {
        "nome": "item2",
        "preco_unitario": 25.5,
        "produto_id": "002",
        "quantidade": 1
      }
    ],
    "total": 47.48,
    "valor_frete": 14
  }


def obterCarteira(user_id):

    if user_id not in carteira_usuario:
        return None

    carteira = carteira_usuario.get(user_id)

    return carteira

def debitarPagamento(metodo_pagamento):

    if metodo_pagamento is None:
        return None

    if metodo_pagamento not in ['cartao_credito', 'cartao_debito', 'boleto']:
        return None
    
    return True

def confirmarReducaoNoEstoque(reduzir_estoque):
    try:
        response = requests.post('http://localhost:5001/reduzir_estoque', json=reduzir_estoque)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException:
        return None


@app.route('/checkout/carrinho', methods=['POST'])
def checkout_carrinho():
    try:
        # Obtém o corpo da requisição JSON (carrinho)
        carrinho = request.json

        # Envia apenas a lista de itens para o serviço de estoque
        itens_para_verificar = {"itens": carrinho["itens"]}
        response = requests.post('http://localhost:5001/verificar_estoque', json=itens_para_verificar)
        response.raise_for_status()

        # Busca o endereço do usuário com base no user_id fornecido
        user_id = carrinho.get("user_id")
        if user_id is None:
            return jsonify({"erro": "user_id não fornecido no carrinho"}), 400

        response_endereco = requests.get(f'http://localhost:5002/enderecos?user_id={user_id}')
        if response_endereco.status_code != 200:
            return jsonify({"erro": "Erro ao consultar o serviço de endereços"}), 500
        
        cep_user = response_endereco.json().get("cep")
        if not cep_user:
            return jsonify({"erro": "CEP não encontrado para o usuário"}), 404

        # Calcula o valor do frete
        cep_loja = "12345-000"
        api_transporte = ApiTranporte()
        valor_frete = api_transporte.calcular_frete(cep_user, cep_loja)

        # Calcula o resumo do carrinho
        resumo = calcular_resumo_do_carrinho(carrinho)

        # Detalhes da compra
        return jsonify({"resumo_pedido": resumo, "valor_frete": valor_frete}), 200
    


    except requests.exceptions.RequestException:
        return jsonify({"erro": "Erro ao consultar o serviço de estoque"}), 500

    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    

@app.route('/checkout/pagamento', methods=['POST'])
def checkout_pagamento():
    try:
        # Obtém o corpo da requisição JSON (carrinho)
        resposta = resumo_pedido

        user_id = resposta.get("user_id")
        if user_id is None:
            return jsonify({"erro": "user_id não fornecido no pagamento"}), 400
        

        carteira = obterCarteira(user_id)
        if carteira is None:
            return jsonify({"erro": "Carteira não encontrada para o usuário"}), 404
        
        return jsonify(carteira), 200

    except requests.exceptions.RequestException:
        return jsonify({"erro": "Erro ao consultar o serviço de estoque"}), 500

    except ValueError as e:
        return jsonify({"erro": str(e)}), 400


@app.route('/checkout/detalhes-da-compra', methods=['POST'])
def checkout_detalhes_compra():
    try:
        # Obtém o corpo da requisição JSON (carrinho)
        resposta = request.json

        user_id = resposta.get("user_id")
        if user_id is None:
            return jsonify({"erro": "user_id não fornecido no pagamento"}), 400
                           
        metodo_pagamento = resposta.get("metodo")
        if metodo_pagamento is None:
            return jsonify({"erro": "método de pagamento não fornecido"}), 400
        
        # Debita o pagamento
        response_debito = debitarPagamento(metodo_pagamento)
        if response_debito is None:
            return jsonify({"erro": "Erro ao debitar o pagamento"}), 500
        
        # Confirma a redução no estoque
        response_confirmacao = confirmarReducaoNoEstoque(resumo_pedido)
        if response_confirmacao is None:
            return jsonify({"erro": "Erro ao confirmar a redução no estoque"}), 500
        
        resumo_pedido["metodo_pagamento"] = metodo_pagamento

        return jsonify(resumo_pedido), 200

    except requests.exceptions.RequestException:
        return jsonify({"erro": "Erro ao consultar o serviço de estoque"}), 500

    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    
if __name__ == '__main__':
    app.run(port=5000, debug=True)