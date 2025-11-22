# Health test obrigatório para o endpoint da API

def test_health_endpoint(client):
    response = client.get("/health")
    
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "healthy"
    assert "verson" in data
    assert "api_iniciada_em" in data
    assert "tempo_operacao_minutos" in data
    
    
    