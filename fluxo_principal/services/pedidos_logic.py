def calcular_resumo_do_carrinho(carrinho):
    if not isinstance(carrinho, dict) or 'itens' not in carrinho:
        raise ValueError("Formato do carrinho inválido")
    
    total = round(sum(item["preco_unitario"] * item["quantidade"] for item in carrinho["itens"]), 2)
    return {"itens": carrinho["itens"], "total": total}
