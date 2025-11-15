from config.db import criar_conexao

def inserir_usuario(nome: str, cpf: str, email: str, password: str):

    try:
        conn = criar_conexao()
        cursor = conn.cursor()

        sql = "INSERT INTO cliente (nome, cpf, email, password) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (nome, cpf, email, password))
        conn.commit()
        print("Usuário inserido com sucesso!")
    except Exception as e:
        print(f"Erro ao inserir usuário: {e}")
    finally:
        cursor.close()
        conn.close()
