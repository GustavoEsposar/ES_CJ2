import re

class Endereco:
    def __init__(self, cep, rua, numero, cidade, estado):
        self.cep = cep
        self.rua = rua
        self.numero = numero
        self.cidade = cidade
        self.estado = estado

    def to_dict(self):
        """Converte o endereço para um dicionário."""
        return {
            "cep": self.cep,
            "rua": self.rua,
            "numero": self.numero,
            "cidade": self.cidade,
            "estado": self.estado
        }
    
    def verificarEndereco(self):
        # Verificação de campos preenchidos
        if not self.rua:
            return False, "Rua não pode estar vazia."
        if not self.numero or not isinstance(self.numero, int) or self.numero <= 0:
            return False, "Número deve ser um valor inteiro positivo."
        if not self.cidade:
            return False, "Cidade não pode estar vazia."
        if not self.estado or not isinstance(self.estado, str) or len(self.estado) != 2:
            return False, "Estado deve ter exatamente 2 caracteres."
        # Verifica se o CEP está no formato correto (5 dígitos + hífen + 3 dígitos)
        cep_pattern = re.compile(r"^\d{5}-\d{3}$")
        if not cep_pattern.match(self.cep):
            return False, "CEP deve estar no formato 12345-678."
        
        # Todos os testes foram aprovados
        return True, "Endereço válido."
