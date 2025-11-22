# Testa a api de tickets
 # Garante que um ticket válido (ex: TICKET_5) aumente o tempo restante do cliente exatamente pelo fator do ticket.

import pytest

def test_ticket_valido_api(client):
    client_id = 1
    
    response = client.post(
        f"/clients/{client_id}/calcular_tempo", 
        json={"ticket": "TICKET_5"},
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert "tempo_restante_anterior" in data
    assert "novo_tempo_restante" in data
    assert "acrescimo_aplicado" in data
    assert data["acrescimo_aplicado"] == 5
    assert data["novo_tempo_restante"] == pytest.approx(
        data["tempo_restante_anterior"] + 5,
        rel=1e-2,
    )