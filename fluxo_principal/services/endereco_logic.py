enderecos_usuarios = {
    1: [{"rua": "Rua A", "cidade": "Cidade X", "cep": "12345-000"}],
    2: [{"rua": "Rua C", "cidade": "Cidade Z", "cep": "67890-000"}]
}

def buscar_endereco_usuario(user_id):
    if user_id not in enderecos_usuarios:
        raise ValueError(f"Usuário com ID {user_id} não encontrado")
    
    # Retorna apenas o primeiro endereço (principal)
    return enderecos_usuarios[user_id][0]
