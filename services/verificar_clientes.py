from config.db import criar_conexao

def verificar_clientes():
    """
    Mostra todos os clientes cadastrados na tabela 'cliente' e retorna uma lista com os resultados.
    """
    con = criar_conexao()
    try:
        with con.cursor() as cursor:
            cursor.execute("SELECT id_cliente, nome, email, cpf FROM cliente ORDER BY id_cliente")
            clientes = cursor.fetchall()

            if not clientes:
                print("Nenhum cliente encontrado.")
                return []

            print("\n--- Clientes Cadastrados ---")
            for c in clientes:
                print(f"ID: {c[0]} | Nome: {c[1]} | Email: {c[2]} | CPF: {c[3]}")

            return clientes

    except Exception as e:
        print(f"Erro ao verificar clientes: {e}")
        return []
    finally:
        con.close()


def apagar_cliente(id_cliente: int):
    """
    Apaga um cliente pelo ID.
    """
    con = criar_conexao()
    try:
        with con.cursor() as cursor:
            cursor.execute("DELETE FROM cliente WHERE id_cliente = %s RETURNING id_cliente", (id_cliente,))
            removido = cursor.fetchone()
        con.commit()

        if removido:
            print(f"Cliente ID {id_cliente} removido com sucesso.")
        else:
            print("Cliente não encontrado.")
    except Exception as e:
        print(f"Erro ao apagar cliente: {e}")
    finally:
        con.close()
