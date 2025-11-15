from typing import Optional, List, Dict, Any
from config.db import criar_conexao

def criar_sessao(id_filme: int, id_sala: int, data_hora) -> int:
    """
    Insere uma sessão. data_hora deve ser um objeto datetime (ou string aceitável pelo DB).
    Retorna id_sessao.
    """
    con = criar_conexao()
    try:
        with con.cursor() as cur:
            # tentativa prévia de verificar conflito de sala+hora (opcional, porque há UNIQUE DB)
            cur.execute(
                "SELECT 1 FROM sessao WHERE id_sala = %s AND data_hora = %s LIMIT 1",
                (id_sala, data_hora)
            )
            conflict = cur.fetchone()
            if conflict:
                raise ValueError("Já existe uma sessão nessa sala e horário.")

            cur.execute(
                "INSERT INTO sessao (id_filme, id_sala, data_hora) VALUES (%s, %s, %s) RETURNING id_sessao",
                (id_filme, id_sala, data_hora)
            )
            sid = cur.fetchone()[0]
        con.commit()
        return sid
    finally:
        con.close()

def listar_sessoes() -> List[Dict[str, Any]]:
    con = criar_conexao()
    try:
        with con.cursor() as cur:
            cur.execute("""SELECT s.id_sessao, s.id_filme, f.titulo, s.id_sala, s.data_hora
                           FROM sessao s
                           LEFT JOIN filme f ON s.id_filme = f.id_filme
                           ORDER BY s.data_hora""")
            rows = cur.fetchall()
            cols = [d[0] for d in cur.description]
            return [dict(zip(cols, r)) for r in rows]
    finally:
        con.close()

def buscar_sessao_por_id(id_sessao: int) -> Optional[Dict[str, Any]]:
    con = criar_conexao()
    try:
        with con.cursor() as cur:
            cur.execute("SELECT id_sessao, id_filme, id_sala, data_hora FROM sessao WHERE id_sessao = %s", (id_sessao,))
            row = cur.fetchone()
            if not row:
                return None
            cols = [d[0] for d in cur.description]
            return dict(zip(cols, row))
    finally:
        con.close()

def deletar_sessao(id_sessao: int) -> bool:
    con = criar_conexao()
    try:
        with con.cursor() as cur:
            cur.execute("DELETE FROM sessao WHERE id_sessao = %s RETURNING id_sessao", (id_sessao,))
            removed = cur.fetchone()
        con.commit()
        return removed is not None
    finally:
        con.close()
