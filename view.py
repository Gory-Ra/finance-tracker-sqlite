from models import Bancos, Conta, engine, Status, Historico, Tipos
from sqlmodel import Session, select
from datetime import date

def criar_conta(conta: Conta): # Lógica para criar uma nova conta 
    with Session(engine) as session: 
        statement = select(Conta).where(Conta.banco == conta.banco) #.where faz um filtro para verificação
        results = session.exec(statement).all() 
        if results:
            print("Conta já existe para este banco.") #validação para evitar criar contas duplicadas para o mesmo banco
            return
        session.add(conta)
        session.commit()
        return conta

def listar_contas(): # Lógica para listar todas as contas
    with Session(engine) as session:
        statement = select(Conta)                       # [] = -> false [1] = -> true
        results = session.exec(statement).all()
    return results  

def desativar_conta(id):
    with Session(engine) as session:
        statement = select(Conta).where(Conta.id == id)
        conta = session.exec(statement).first() 
        
        if not conta:
            raise ValueError("Conta não encontrada") #Validação para verificar se a conta existe antes de tentar desativá-la
        
        if conta.valor > 0:
            raise ValueError("Não ha como desativar uma conta com saldo positivo")
        
        conta.status = Status.INATIVO  # Altera o status da conta para inativo
        
        session.add(conta)
        session.commit()

def transferir_saldo(id_conta_saida, id_conta_entrada, valor):
    with Session(engine) as session:
        
        if valor <= 0:
            raise ValueError("O valor deve ser maior que zero")
        
        if id_conta_saida == id_conta_entrada:
            raise ValueError("Não é possível transferir para a mesma conta")
        
        conta_saida = session.exec(
            select(Conta).where(Conta.id == id_conta_saida)
        ).first()
        
        conta_entrada = session.exec(
            select(Conta).where(Conta.id == id_conta_entrada)
        ).first()
        
        if not conta_saida or not conta_entrada:
            raise ValueError("Conta não encontrada")
        
        if conta_saida.valor < valor:
            raise ValueError("Saldo insuficiente para transferência")
        
        conta_saida.valor -= valor
        conta_entrada.valor += valor
        
        session.add(conta_saida)
        session.add(conta_entrada)#Adiciona as contas atualizadas ao banco de dados
        
        session.commit()

def movimentar_dinheiro(historico: Historico):
    with Session(engine) as session:
        
        if historico.valor <= 0:
            raise ValueError("O valor deve ser maior que zero")
        
        conta = session.exec(
            select(Conta).where(Conta.id == historico.conta_id)
        ).first()
        
        if not conta:
            raise ValueError("Conta não encontrada")
        
        if historico.tipo == Tipos.ENTRADA:
            conta.valor += historico.valor
        
        elif historico.tipo == Tipos.SAIDA:
            if conta.valor < historico.valor:
                raise ValueError("Saldo insuficiente para saída")
            conta.valor -= historico.valor
        
        session.add(conta)
        session.add(historico)
        session.commit()
        
        return historico

def total_contas():
    with Session(engine) as session:
        statement = select(Conta)
        contas = session.exec(statement).all()
    
    total = 0
    for conta in contas:
        total += conta.valor
    
    return float(total)
        
def buscar_historico_entre_datas(data_inicio: date, data_fim: date):
    if data_inicio > data_fim:
        raise ValueError("Data inicial não pode ser maior que a final")
    
    with Session(engine) as session:
        statement = select(Historico).where(
            Historico.data >= data_inicio,
            Historico.data <= data_fim
        )
        return session.exec(statement).all()


import matplotlib.pyplot as plt

def criar_grafico_por_conta():
    with Session(engine) as session:
        statement = select(Conta).where(Conta.status == Status.ATIVO)
        contas = session.exec(statement).all()
        
        if not contas:
            print("Nenhuma conta ativa encontrada")
            return
        
        bancos = [i.banco.value for i in contas]
        total = [i.valor for i in contas]
        
        plt.bar(bancos, total)
        plt.show()
