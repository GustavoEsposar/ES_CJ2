def calcular_disponibilidade(estoque, itens):
    for item in itens:
        produto_id = item["produto_id"]
        quantidade_requerida = item["quantidade"]
        if produto_id not in estoque or estoque[produto_id]["quantidade"] < quantidade_requerida:
            return False
    return True
