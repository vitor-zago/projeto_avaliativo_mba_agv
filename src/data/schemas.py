"""
Schemas Pydantic para validação de dados
"""
from pydantic import BaseModel, Field
from typing import List

# Modelo de Clientes
class ClientesInput(BaseModel):
    """
    Schema para representaros dados de entrada de um produto
    """    
    nome: str = Field(..., min_length=1, max_length=256, description="Nome do cliente")
    tempo: int = Field(..., ge=1, le=1000, description="Tempo de acesso remanescente do cliente")


class MessageInput(BaseModel):
    """
    Schema para entrada de mensagem
    """
    text: str = Field(...,
                      min_length=1,
                      max_length=500,
                      description="Texto da mensagem"
                      )
    priority: int = Field(
        default=1,
        ge=1, #ge= greater equal
        le=5, #le= less equal
        description="Prioridade da mensagem (1-5)")
    
    class Config:
        json_schema_extra  = {
            "example": {
                "text": "Esta é uma mensagem de teste.",
                "priority": 3
            }
        }

class ClienteOutput(BaseModel):
    """
    Schema para representar os dados de saída de um cliente
    """
    id: int
    nome: str 
    tempo: int 

class TicketInput(BaseModel):
    ticket: str = Field(..., min_length=1, max_length=50, description="Código do ticket de acesso")
