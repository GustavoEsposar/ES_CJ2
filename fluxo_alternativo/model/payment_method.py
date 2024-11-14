import re

class MetodoPagamento:
    def __init__(self, type):
        self.type = type
    
    def verificar(self):
        # Verificação de campos preenchidos
        if not self.type:
            return False
        if self.type == 'PIX':
            return True
        if self.type == 'DEBITO':
            return True
        if self.type == 'CREDITO':
            return True

        return False, "Metodo de pagamento inválido"