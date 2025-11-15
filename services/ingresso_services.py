from config.db import criar_conexao

def vender_ingresso(id_sessao, id_cliente, assento, valor_pago, tipo):
    con = criar_conexao()
    cur = con.cursor()
    try:
        cur.execute("""
            INSERT INTO ingresso (id_sessao, id_cliente, assento, valor_pago, tipo)
            VALUES (%s, %s, %s, %s, %s)
        """, (id_sessao, id_cliente, assento, valor_pago, tipo))
        con.commit()
    except Exception as e:
        con.rollback()
        raise e
    finally:
        cur.close()
        con.close()

def listar_ingressos():
    con = criar_conexao()
    cur = con.cursor()
    try:
        cur.execute("""
            SELECT i.id_ingresso, c.nome AS cliente, f.titulo AS filme, s.data_hora, i.assento, i.valor_pago, i.tipo
            FROM ingresso i
            JOIN cliente c ON i.id_cliente = c.id_cliente
            JOIN sessao s ON i.id_sessao = s.id_sessao
            JOIN filme f ON s.id_filme = f.id_filme
            ORDER BY s.data_hora
        """)
        return cur.fetchall()
    finally:
        cur.close()
        con.close()

def listar_ingressos_por_cliente(id_cliente):
    con = criar_conexao()
    cur = con.cursor()
    try:
        cur.execute("""
            SELECT i.id_ingresso, f.titulo, s.data_hora, i.assento, i.valor_pago, i.tipo
            FROM ingresso i
            JOIN sessao s ON i.id_sessao = s.id_sessao
            JOIN filme f ON s.id_filme = f.id_filme
            WHERE i.id_cliente = %s
            ORDER BY s.data_hora
        """, (id_cliente,))
        rows = cur.fetchall()

        resultado = []
        for r in rows:
            resultado.append({
                "id_ingresso": r[0],
                "titulo": r[1],
                "data_hora": r[2],
                "assento": r[3],
                "valor_pago": float(r[4]),
                "tipo": r[5]
            })
        return resultado
    finally:
        cur.close()
        con.close()
