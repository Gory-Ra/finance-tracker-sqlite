from datetime import datetime, date

from models import Bancos, Tipos, Historico, Conta
from view import (
    criar_conta,
    listar_contas,
    desativar_conta,
    transferir_saldo,
    movimentar_dinheiro,
    total_contas,
    buscar_historico_entre_datas,
    criar_grafico_por_conta
)


class UI:
    def start(self):
        while True:
            print('''
            [1] -> Criar conta
            [2] -> Desativar conta
            [3] -> Transferir dinheiro
            [4] -> Movimentar dinheiro
            [5] -> Total contas
            [6] -> Filtrar histórico
            [7] -> Gráfico
            [0] -> Sair
            ''')

            try:
                choice = int(input('Escolha uma opção: '))
            except ValueError:
                print("Opção inválida.")
                continue

            if choice == 1:
                self._criar_conta()
            elif choice == 2:
                self._desativar_conta()
            elif choice == 3:
                self._transferir_saldo()
            elif choice == 4:
                self._movimentar_dinheiro()
            elif choice == 5:
                self._total_contas()
            elif choice == 6:
                self._filtrar_movimentacoes()
            elif choice == 7:
                self._criar_grafico()
            elif choice == 0:
                print("Saindo...")
                break
            else:
                print("Opção inválida.")

    def _criar_conta(self):
        print('Digite o nome de algum dos bancos abaixo:')
        for banco in Bancos:
            print(f'---{banco.value}---')

        try:
            banco = Bancos(input().title())
            valor = float(input('Digite o valor atual disponível na conta: '))
        except ValueError:
            print("Entrada inválida.")
            return

        conta = Conta(banco=banco, valor=valor)
        criar_conta(conta)
        print("Conta criada com sucesso.")

    def _desativar_conta(self):
        print('Escolha a conta que deseja desativar.')
        for i in listar_contas():
            if i.valor == 0:
                print(f'{i.id} -> {i.banco.value} -> R$ {i.valor}')

        try:
            id_conta = int(input())
            desativar_conta(id_conta)
            print('Conta desativada com sucesso.')
        except ValueError as e:
            print(f"Erro: {e}")

    def _transferir_saldo(self):
        try:
            print('Escolha a conta retirar o dinheiro.')
            for i in listar_contas():
                print(f'{i.id} -> {i.banco.value} -> R$ {i.valor}')

            conta_retirar_id = int(input())

            print('Escolha a conta para enviar dinheiro.')
            for i in listar_contas():
                if i.id != conta_retirar_id:
                    print(f'{i.id} -> {i.banco.value} -> R$ {i.valor}')

            conta_enviar_id = int(input())

            valor = float(input('Digite o valor para transferir: '))

            transferir_saldo(conta_retirar_id, conta_enviar_id, valor)
            print("Transferência realizada com sucesso.")

        except ValueError as e:
            print(f"Erro: {e}")

    def _movimentar_dinheiro(self):
        try:
            print('Escolha a conta.')
            for i in listar_contas():
                print(f'{i.id} -> {i.banco.value} -> R$ {i.valor}')

            conta_id = int(input())

            valor = float(input('Digite o valor movimentado: '))

            print('Selecione o tipo da movimentação')
            for tipo in Tipos:
                print(f'---{tipo.value}---')

            tipo = Tipos(input().title())

            historico = Historico(
                conta_id=conta_id,
                tipo=tipo,
                valor=valor,
                data=date.today()
            )

            movimentar_dinheiro(historico)
            print("Movimentação registrada com sucesso.")

        except ValueError as e:
            print(f"Erro: {e}")

    def _total_contas(self):
        print(f'Total: R$ {total_contas()}')

    def _filtrar_movimentacoes(self):
        try:
            data_inicio = datetime.strptime(
                input('Digite a data de início (DD/MM/AAAA): '),
                '%d/%m/%Y'
            ).date()

            data_fim = datetime.strptime(
                input('Digite a data final (DD/MM/AAAA): '),
                '%d/%m/%Y'
            ).date()

        except ValueError:
            print("Data inválida.")
            return

        resultados = buscar_historico_entre_datas(data_inicio, data_fim)

        for i in resultados:
            print(f'{i.valor} - {i.tipo.value}')

    def _criar_grafico(self):
        criar_grafico_por_conta()


UI().start()