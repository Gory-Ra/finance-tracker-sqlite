# Criar o banco de dados e a tabela

from sqlmodel import Field, Relationship, SQLModel, create_engine
from enum import Enum
from datetime import date

class Bancos(Enum): #Bancos disponíveis (pode ser expandido para incluir mais bancos no futuro)
    NUBANK = "Nubank"
    INTER = "Inter"
    C6 = "C6"

class Status(Enum): #Status da conta, se está ativa ou inativa
    ATIVO = "Ativo"
    INATIVO = "Inativo"

class Tipos(Enum): #Tipos de transações, se é uma entrada ou saída de dinheiro
    ENTRADA = "Entrada"
    SAIDA = "Saida"

class Conta(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    banco: Bancos = Field(default=Bancos.NUBANK)
    status: Status = Field(default=Status.ATIVO)
    valor: float = 0.0

class Historico(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    conta_id: int = Field(foreign_key="conta.id")
    conta: Conta = Relationship()
    tipo: Tipos = Field(default=Tipos.ENTRADA)
    valor: float = 0.0
    data: date = Field(default_factory=date.today)

sqlite_file_name = "database.db" #Nome do arquivo do banco de dados SQLite
sqlite_url = f"sqlite:///{sqlite_file_name}" #URL de conexão para o banco de dados SQLite

engine = create_engine(sqlite_url, echo=False) #Criar o mecanismo de conexão com o banco de dados

def create_db_and_tables(): #Função para criar o banco de dados e as tabelas
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__": #Executar a função para criar o banco de dados e as tabelas quando o script for executado diretamente
    create_db_and_tables()

