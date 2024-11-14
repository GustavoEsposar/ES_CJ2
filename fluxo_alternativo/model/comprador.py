from endereco import EnderecoSchema

class Comprador:
    def __init__(self, nome, email, senha, enderecos=[]):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.enderecos = [EnderecoSchema(endereco).to_dict() for endereco in enderecos]

    def to_dict(self):
        """Converte o comprador para um dicionário."""
        return {
            "nome": self.nome,
            "email": self.email,
            "senha": self.senha,
            "enderecos": self.enderecos
        }
