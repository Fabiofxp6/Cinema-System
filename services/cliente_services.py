import bcrypt
from config.db import criar_conexao

def inserir_cliente(nome, cpf, email, password):
    """
    Insere um cliente com senha criptografada usando bcrypt.
    """
    con = criar_conexao()
    try:
        with con.cursor() as cur:
            # Gera o hash da senha com salt
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            cur.execute(
                "INSERT INTO cliente (nome, cpf, email, password) VALUES (%s, %s, %s, %s)",
                (nome, cpf, email, hashed.decode('utf-8'))
            )
        con.commit()
    finally:
        con.close()


def buscar_cliente_por_email(email: str):
    """
    Retorna um cliente com base no e-mail, incluindo o campo 'password'.
    """
    con = criar_conexao()
    try:
        with con.cursor() as cur:
            cur.execute(
                "SELECT id_cliente, nome, email, cpf, password FROM cliente WHERE email = %s",
                (email,)
            )
            row = cur.fetchone()
            if not row:
                return None
            cols = [d[0] for d in cur.description]
            return dict(zip(cols, row))
    finally:
        con.close()
