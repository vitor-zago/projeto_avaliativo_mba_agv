from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import datetime
from typing import Dict, List

from data.schemas import TicketInput
from api.ticket_tempo import TicketAcesso

app = FastAPI()

# Variáveis globais para controle de tempo
api_start_time: datetime.datetime = None
clientes_tempo_inicial: Dict[int, int] = {}

# Modelo de dados
class Client(BaseModel):
    id: int
    nome: str
    tempo: int

# Banco de dados simulado
clientes_db = [
    {"id": 1, "nome": "Gisele", "tempo": 30},  # 30 minutos
    {"id": 2, "nome": "Ana", "tempo": 45},     # 45 minutos  
    {"id": 3, "nome": "Vitor", "tempo": 20},   # 20 minutos
]

def calcular_tempo_restante(cliente_id: int) -> int:
    """
    Calcula o tempo restante baseado no tempo inicial e tempo decorrido.
    """
    if api_start_time is None:
        return clientes_db[cliente_id - 1]["tempo"]
    
    tempo_decorrido = (datetime.datetime.now() - api_start_time).total_seconds() / 60  # Converter para minutos
    tempo_inicial = clientes_tempo_inicial.get(cliente_id, clientes_db[cliente_id - 1]["tempo"])
    
    tempo_restante = tempo_inicial - tempo_decorrido
    return max(0, tempo_restante)  # Não permite tempo negativo

@app.on_event("startup")
def startup_event():
    """
    Executado quando a API inicia.
    """
    global api_start_time, clientes_tempo_inicial
    api_start_time = datetime.datetime.now()
    
    # Inicializa o tempo inicial de cada cliente
    for cliente in clientes_db:
        clientes_tempo_inicial[cliente["id"]] = cliente["tempo"]
    
    print(f"API iniciada em: {api_start_time}")

# Endpoints
@app.get("/")
def home():
    return {"mensagem": "Bem-vindo à API de Validação de Tickets de Tempo de Acesso!"}

@app.get("/health")
def health_check():
    tempo_operacao = (datetime.datetime.now() - api_start_time).total_seconds() if api_start_time else 0
    return {
        "status": "healthy",
        "version": "1.0.0",
        "api_iniciada_em": api_start_time.isoformat() if api_start_time else "N/A",
        "tempo_operacao_minutos": round(tempo_operacao / 60, 2)
    }

@app.get("/clientes")
def listar_clientes():
    """
    Lista todos os clientes com tempo restante atualizado.
    """
    clientes_com_tempo_restante = []
    for cliente in clientes_db:
        tempo_restante = calcular_tempo_restante(cliente["id"])
        clientes_com_tempo_restante.append({
            "id": cliente["id"],
            "nome": cliente["nome"],
            "tempo_restante": round(tempo_restante, 2),
            "tempo_original": clientes_tempo_inicial.get(cliente["id"], cliente["tempo"])
        })
    
    return {"clientes": clientes_com_tempo_restante}

@app.get("/clientes/{cliente_id}")
def consultar_cliente(cliente_id: int):
    """
    Retorna um determinado cliente pelo ID com tempo restante atualizado.
    """
    cliente = next((p for p in clientes_db if p["id"] == cliente_id), None)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    tempo_restante = calcular_tempo_restante(cliente_id)
    
    return {
        "id": cliente["id"],
        "nome": cliente["nome"],
        "tempo_restante": round(tempo_restante, 2),
        "tempo_original": clientes_tempo_inicial.get(cliente_id, cliente["tempo"]),
        "api_iniciada_em": api_start_time.isoformat() if api_start_time else "N/A"
    }

@app.post("/clientes/{cliente_id}/calcular_tempo", response_model=dict)
def aplicar_acrescimo(cliente_id: int, ticket: TicketInput):
    """
    Aplica acréscimo de tempo ao tempo RESTANTE do cliente.
    """
    cliente = next((p for p in clientes_db if p["id"] == cliente_id), None)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    ticket_tempo = TicketAcesso(ticket.ticket)

    if not ticket_tempo.is_valid:
        raise HTTPException(status_code=400, detail="Ticket inválido")
    
    # Calcula tempo restante atual
    tempo_restante_atual = calcular_tempo_restante(cliente_id)
    
    # Aplica o acréscimo ao tempo restante
    novo_tempo_restante = ticket_tempo.aplicar_acrescimo(tempo_restante_atual)
    
    # Atualiza o tempo inicial para refletir o novo tempo total
    tempo_decorrido = (datetime.datetime.now() - api_start_time).total_seconds() / 60
    novo_tempo_inicial = novo_tempo_restante + tempo_decorrido
    
    clientes_tempo_inicial[cliente_id] = novo_tempo_inicial
    cliente["tempo"] = novo_tempo_inicial  # Atualiza também no "banco de dados"
    
    return {
        "id": cliente["id"],
        "nome": cliente["nome"],
        "tempo_restante_anterior": round(tempo_restante_atual, 2),
        "acrescimo_aplicado": ticket_tempo.fator_acrescimo,
        "novo_tempo_restante": round(novo_tempo_restante, 2),
        "novo_tempo_total": round(novo_tempo_inicial, 2),
        "tempo_decorrido": round(tempo_decorrido, 2)
    }

@app.post("/clientes/{cliente_id}/reset_tempo")
def resetar_tempo(cliente_id: int, novo_tempo: int):
    """
    Reseta o tempo do cliente (apenas para testes).
    """
    cliente = next((p for p in clientes_db if p["id"] == cliente_id), None)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    clientes_tempo_inicial[cliente_id] = novo_tempo
    cliente["tempo"] = novo_tempo
    
    return {
        "mensagem": f"Tempo do cliente {cliente['nome']} resetado para {novo_tempo} minutos",
        "tempo_restante_atual": calcular_tempo_restante(cliente_id)
    }

if __name__ == "__main__":
    uvicorn.run('main:app', host="127.0.0.1", port=8000, reload=True)