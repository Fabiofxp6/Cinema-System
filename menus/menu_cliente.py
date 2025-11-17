import os
from services.filme_services import listar_filmes
from services.sessao_services import listar_sessoes
from services.ingresso_services import vender_ingresso, listar_ingressos_por_cliente

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    input("\nPressione Enter para continuar...")

def menu_cliente(cliente):
    while True:
        limpar_tela()
        print(f"=== MENU CLIENTE ({cliente['nome']}) ===")
        print("1. Listar filmes")
        print("2. Listar sessões")
        print("3. Comprar ingresso")
        print("4. Meus ingressos")
        print("0. Logout")
        op = input("Escolha: ")

        if op == '1':
            for f in listar_filmes():
                print(f)
            pause()

        elif op == '2':
            for s in listar_sessoes():
                print(s)
            pause()

        elif op == '3':
            try:
                print("Escolha a sessão para comprar o ingresso:")
                for s in listar_sessoes():
                    print(s)
                id_sessao = int(input("ID da sessão: "))
                assento = input("Assento (ex: A1): ")
                valor = float(input("Inteira: R$44.00 / Meia: R$22.00\nValor do ingresso: R$"))
                if valor == 44.00:
                    tipo = "inteira"
                elif valor == 22.00:
                    tipo = "meia"
                else:
                    raise ValueError("Valor inválido para ingresso.")
                vender_ingresso(id_sessao, cliente['id_cliente'], assento, valor, tipo)
                print("🎟️ Ingresso comprado com sucesso!")
            except Exception as e:
                print("Erro:", e)
            pause()

        elif op == '4':
            ingressos = listar_ingressos_por_cliente(cliente['id_cliente'])
            if not ingressos:
                print("Nenhum ingresso encontrado.")
            else:
               for i in ingressos:
                print("INGRESSO")
                print("ID:", i['id_ingresso'])
                print("Título:", i['titulo'])
                print("Data/Hora:", i['data_hora'])
                print("Assento:", i['assento'])
                print("Valor Pago:", i['valor_pago'])
                print("Tipo:", i['tipo'])
                print()


            pause()

        elif op == '0':
            print("Saindo da conta...")
            pause()
            break
        else:
            print("Opção inválida.")
            pause()
