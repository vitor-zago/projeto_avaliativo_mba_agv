class TicketAcesso:
    """
    Classe para gerenciar tickets de tempo de acesso.
    """
    
    # Dicionário de tickets de acesso válidos
    ticket_acesso = {"TICKET_10": 10, "TICKET_5": 5, "TICKET_2": 2}

    def __init__(self, codigo: str):
        self.codigo = codigo
        self.is_valid = codigo in self.ticket_acesso
        self.fator_acrescimo = self.ticket_acesso.get(codigo, 0)  # Usar get() para evitar KeyError

    def aplicar_acrescimo(self, tempo_restante: int) -> int:
        """
        Retorna o tempo restante de acesso acrescido do bonus do ticket.
        """
        return tempo_restante + self.fator_acrescimo

    def get_fator_acrescimo(self) -> int:
        """
        Retorna o valor do fator de acrescimo do ticket.
        """
        return self.fator_acrescimo