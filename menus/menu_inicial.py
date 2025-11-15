import bcrypt
from menus.menu_cliente import menu_cliente
from services.cliente_services import buscar_cliente_por_email
import os
from services.cliente_services import inserir_cliente
from menus.menu_adm import menu_adm

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    input("\nPressione Enter para continuar...")

def menu_inicial():
    while True:
        limpar_tela()       
        print("=== 🎬 CINEMA SYSTEM ===")
        print("1. Criar novo cliente")
        print("2. Login cliente")
        print("3. Menu administrador")
        print("0. Sair")
        op = input("Escolha: ")

        if op == '1':
            criar_cliente()
        elif op == '2':
            cliente_login()
        elif op == '3':
            menu_adm()
        elif op == '0':
            print("Saindo...")
            break
        else:
            print("Opção inválida.")
            pause()

def criar_cliente():
    limpar_tela()
    print("=== NOVO CLIENTE ===")
    nome = input("Nome: ")
    cpf = input("CPF (apenas números): ")
    email = input("Email: ")
    senha = input("Senha: ")

    try:
        inserir_cliente(nome, cpf, email, senha)
        print("✅ Cliente criado com sucesso!")
    except Exception as e:
        print("Erro ao criar cliente:", e)
    pause()

def cliente_login():
    limpar_tela()
    print("=== LOGIN CLIENTE ===")
    email = input("Email: ")
    senha = input("Senha: ")

    user = buscar_cliente_por_email(email)
    if not user:
        print("Cliente não encontrado.")
        pause()
        return

    # Verifica a senha com bcrypt
    senha_correta = bcrypt.checkpw(senha.encode('utf-8'), user['password'].encode('utf-8'))

    if not senha_correta:
        print("Senha incorreta.")
        pause()
        return

    print(f"\nBem-vindo(a), {user['nome']}!")
    pause()
    menu_cliente(user)

