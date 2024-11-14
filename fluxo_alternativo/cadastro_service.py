from flask import Flask, jsonify, request, render_template
from model.endereco import Endereco
from database.db_connection import get_comprador_id, add_endereco_to_comprador

app = Flask(__name__)

@app.route("/novo-endereco", methods=["GET"])
def obter_formulario_endereco():
    # Renderiza o formulário HTML para o novo endereço
    return render_template("index.html")

@app.route("/novo-endereco", methods=["POST"])
def cadastrar_endereco():
    # Obtém o JSON da requisição
    endereco_dados = request.get_json()
    print("Dados recebidos:", endereco_dados)  # Log para depuração

    # Verifica se todos os campos necessários estão presentes
    if not endereco_dados:
        return jsonify({"status": 400, "mensagem": "Erro de Validação: Estrutura de dados inválida"}), 400
    
    # Busca o comprador_id com base no email fornecido
    comprador_id = get_comprador_id("profe@palito.com")
    
    if not comprador_id:
        return jsonify({"status": 404, "mensagem": "Erro: Comprador não encontrado"}), 404

    try:
        numero = int(endereco_dados.get("numero", 0))  # Converte o número para inteiro
        novo_endereco = Endereco(
            rua=endereco_dados.get("rua"),
            numero=numero,
            cidade=endereco_dados.get("cidade"),
            estado=endereco_dados.get("estado"),
            cep=endereco_dados.get("cep")
        )
    except ValueError:
        return jsonify({"status": 400, "mensagem": "Erro de Validação: Número inválido"}), 400
    
    # Valida o endereço com mensagens específicas
    verificado, mensagem = novo_endereco.verificarEndereco()
    if verificado:
        # Se o endereço for válido, adicione o novo endereço ao comprador no MongoDB
        sucesso = add_endereco_to_comprador(comprador_id, novo_endereco)
        if sucesso:
            response = jsonify({"status": 200, "mensagem": f"Endereço cadastrado com sucesso para o comprador ID {comprador_id}"})
            return response, 200
        else:
            return jsonify({"status": 500, "mensagem": "Erro ao atualizar o endereço no banco de dados"}), 500
    else:
        # Retorna mensagem específica de erro
        return jsonify({"status": 400, "mensagem": mensagem}), 400

if __name__ == "__main__":
    app.run(host="localhost", port=5002)