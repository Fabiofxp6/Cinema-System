import os
from services.filme_services import inserir_filme, listar_filmes, atualizar_filme
from services.sala_services import inserir_sala, listar_salas
from services.sessao_services import criar_sessao, listar_sessoes
from services.ingresso_services import listar_ingressos
from services.verificar_clientes import verificar_clientes, apagar_cliente  # <-- NOVO

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    input("\nPressione Enter para continuar...")

def menu_adm():
    limpar_tela()
    senha = input("Senha do administrador: ")
    if senha != "admin123":
        print("Acesso negado.")
        pause()
        return

    while True:
        limpar_tela()
        print("=== MENU ADMINISTRADOR ===")
        print("1. Adicionar filme")
        print("2. Adicionar sala")
        print("3. Criar sessão")
        print("4. Listar filmes")
        print("5. Listar salas")
        print("6. Listar sessões")
        print("7. Ver ingressos vendidos")
        print("8. Verificar clientes")
        print("9. Apagar cliente")
        print("10. Editar Filme")
        print("0. Voltar")
        op = input("Escolha: ")

        if op == '1':
            titulo = input("Título: ")
            duracao = int(input("Duração (min): "))
            classificacao = input("Classificação: ")
            genero = input("Gênero: ")
            inserir_filme(titulo, duracao, classificacao, genero)
            print("Filme adicionado.")
            pause()

        elif op == '2':
            numero = int(input("Número da sala: "))
            capacidade = int(input("Capacidade: "))
            inserir_sala(numero, capacidade)
            print("Sala criada.")
            pause()

        elif op == '3':
            print("Escolha o filme para a sessão:")
            for f in listar_filmes():
                print(f)
            print("Escolha a sala para a sessão:")
            for s in listar_salas():
                print(s)
            id_filme = int(input("ID do filme: "))
            id_sala = int(input("ID da sala: "))
            data_hora = input("Data e hora (DD-MM-YYYY HH:MM:SS): ")
            criar_sessao(id_filme, id_sala, data_hora)
            print("Sessão criada.")
            pause()

        elif op == '4':
            for f in listar_filmes():
                print(f)
            pause()

        elif op == '5':
            for s in listar_salas():
                print(s)
            pause()

        elif op == '6':
            for s in listar_sessoes():
                print(s)
            pause()

        elif op == '7':
            for i in listar_ingressos():
                print(i)
            pause()

        elif op == '8':
            verificar_clientes()
            pause()

        elif op == '9':
            print("Clientes cadastrados:")
            verificar_clientes()
            id_c = int(input("Digite o ID do cliente a ser removido: "))
            apagar_cliente(id_c)
            pause()

        elif op == '10':
            print("Filmes cadastrados:")
            for f in listar_filmes():
                print(f)

            try:
                id_f = int(input("ID do filme que deseja editar: "))
            except ValueError:
                print("ID inválido.")
                pause()
                continue

            print("\nDeixe em branco para NÃO alterar o campo.")
            novo_titulo = input("Novo título: ")
            nova_duracao = input("Nova duração: ")
            nova_classificacao = input("Nova classificação: ")
            novo_genero = input("Novo gênero: ")

            try:
                duracao_param = int(nova_duracao) if nova_duracao else None
            except ValueError:
                print("Duração inválida.")
                pause()
                continue

            sucesso = atualizar_filme(
                id_f,
                titulo=novo_titulo if novo_titulo else None,
                duracao=duracao_param,
                classificacao_indicativa=nova_classificacao if nova_classificacao else None,
                genero=novo_genero if novo_genero else None
            )

            if sucesso:
                print("Filme atualizado com sucesso!")
            else:
                print("Nenhuma alteração realizada ou ID não encontrado.")

            pause()

        elif op == '0':
            break

        else:
            print("Opção inválida.")
            pause()
