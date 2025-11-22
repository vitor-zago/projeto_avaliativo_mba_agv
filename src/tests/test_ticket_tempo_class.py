# Testa a classe TicketTempo

from api.ticket_tempo import TicketAcesso

def test_ticket_valido_add_acrescimo():
    ticket = TicketAcesso("TICKET_10")
    
    assert ticket.is_valid is True
    assert ticket.get_fator_acrescimo() == 10
    
    tempo_novo = ticket.aplicar_acrescimo(tempo_atual=30)
    assert tempo_novo == 40      # 30 + 10   
    
def test_ticket_invalido_nao_add_tempo():
    ticket = TicketAcesso("TICKET_INVALIDO")
        
    assert ticket.is_valid is False
    assert ticket.get_fator_acrescimo() == 0
    
    tempo_novo = ticket.aplicar_acrescimo(tempo_atual=30)
    assert tempo_novo == 30      # Sem alteração no tempo
