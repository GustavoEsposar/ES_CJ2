# main.py
from database.db_connection import get_collection
from model.comprador import Comprador
from model.endereco import Endereco
from model.payment_method import MetodoPagamento

import requests








'''
url = "http://localhost:5003/checkout/detalhes-da-compra"
data = {
    "order_id": "12345",
    "payment_method": "PIX",  # Substitua pelo método de pagamento adequado
    "amount": 150.0
}

response = requests.post(url, json=data)

print("Status Code:", response.status_code)
print("Response JSON:", response.json())
'''


'''
# Obtendo a coleção de compradores
compradores_collection = get_collection("compradores")

# Criando instâncias de Endereco e Comprador
endereco1 = Endereco(cep="12345-678", rua="Rua das Flores", numero="123", cidade="São Paulo", estado="SP")
endereco2 = Endereco(cep="98765-432", rua="Rua das Palmeiras", numero="456", cidade="Rio de Janeiro", estado="RJ")

comprador = Comprador(
    nome="Ana",
    email="ana@example.com",
    senha="senha123",
    enderecos=[endereco1.to_dict(), endereco2.to_dict()]
)

# Inserindo o comprador na coleção
compradores_collection.insert_one(comprador.to_dict())

payment_method = MetodoPagamento('PIX')

print("Novo comprador inserido com sucesso!")
'''