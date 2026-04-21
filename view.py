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
        statement= select(Conta).where(Conta.id==id) #Busca a conta pelo ID
        conta = session.exec(statement).first() #Retorna a primeira conta encontrada
        if conta.valor >0:
            raise ValueError("Não ha como desativar uma que tem saldo positivo") #Validação para impedir desativar contas com saldo positivo
        conta.status = "Inativo" #Altera o status da conta para "Inativo
        session.commit() #Salva as alterações no banco de dados

def transferir_saldo(id_conta_saida, id_conta_entrada, valor):
    with Session(engine) as session:
        statement = select(Conta).where(Conta.id == id_conta_saida) #Busca a conta de saída pelo ID
        conta_saida = session.exec(statement).first() #Retorna a primeira conta encontrada
        if conta_saida.valor < valor:
            raise ValueError("Saldo insuficiente para transferência") #Validação para impedir transferências com saldo insuficiente
        statement = select(Conta).where(Conta.id == id_conta_entrada) #Busca a conta de entrada pelo ID
        conta_entrada = session.exec(statement).first() #Retorna a primeira conta encontrada

        conta_saida.valor -= valor #Deduz o valor da conta de saída
        conta_entrada.valor += valor #Adiciona o valor à conta de entrada
        session.commit() 

def movimentar_dinheiro(historico: Historico):
    with Session(engine) as session:
        statement = select(Conta).where(Conta.id == historico.conta_id) 
        conta = session.exec(statement).first()
        if historico.tipo == Tipos.ENTRADA:
            conta.valor += historico.valor #Adiciona o valor à conta se for uma entrada
        elif historico.tipo == Tipos.SAIDA:
            if conta.valor < historico.valor:
                raise ValueError("Saldo insuficiente para saída") #Validação para impedir saídas com saldo insuficiente
            conta.valor -= historico.valor #Reduz o valor da conta se for uma saída
        
        session.add(historico) #Adiciona o histórico da transação ao banco de dados
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
    with Session(engine) as session:
        statement = select(Historico).where(
            Historico.data >= data_inicio,
            Historico.data <= data_fim
        )
        resultados = session.exec(statement).all() #Busca o histórico de transações entre as datas especificadas
        return resultados


def criar_grafico_por_conta():
    with Session(engine) as session:
        statement = select(Conta).where(Conta.status==Status.Ativo)
        contas = session.exec(statement).all()
        bancos = [i.banco.value for i in contas]#Cria uma lista com os nomes dos bancos para cada conta ativa
        total = [i.valor for i in contas]#Cria uma lista com os valores de cada conta ativa
        import matplotlib.pyplot as plt
        plt.bar(bancos, total) #Cria um gráfico de barras usando os nomes dos bancos e os valores das contas ativas
        plt.show
