import requests

BASE_URL = "http://localhost:5000"

def ver_carrinho(user_id):
    response = requests.get(f"{BASE_URL}/checkout/carrinho", params={"user_id": user_id})
    if response.status_code == 200:
        print("Carrinho:", response.json())
    else:
        print("Erro ao visualizar o carrinho.")

def modificar_quantidade(user_id, item_id, quantidade):
    data = {
        "user_id": user_id,
        "item_id": item_id,
        "quantidade": quantidade
    }
    response = requests.post(f"{BASE_URL}/checkout/modificar-quantidade", json=data)
    if response.status_code == 200:
        print("Quantidade modificada:", response.json())
    else:
        print("Erro ao modificar quantidade:", response.json().get("mensagem"))

def fechar_pedido(user_id):
    response = requests.post(f"{BASE_URL}/checkout/fechar-pedido", json={"user_id": user_id})
    if response.status_code == 200:
        print("Pedido fechado com sucesso:", response.json())
    else:
        print("Erro ao fechar pedido.")

# Exemplo de uso
if __name__ == '__main__':
    user_id = 1
    ver_carrinho(user_id)
    modificar_quantidade(user_id, 101, 3)
    ver_carrinho(user_id)
    fechar_pedido(user_id)
