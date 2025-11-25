from typing import Optional, List, Dict, Any
from config.db import criar_conexao

def inserir_filme(titulo: str, duracao: int, classificacao_indicativa: str, genero: str) -> int:
    con = criar_conexao()
    try:
        with con.cursor() as cur:
            cur.execute(
                """
                INSERT INTO filme (titulo, duracao, classificacao_indicativa, genero)
                VALUES (%s, %s, %s, %s)
                RETURNING id_filme
                """,
                (titulo, duracao, classificacao_indicativa, genero)
            )
            fid = cur.fetchone()[0]
        con.commit()
        return fid
    finally:
        con.close()

def listar_filmes() -> List[Dict[str, Any]]:
    con = criar_conexao()
    try:
        with con.cursor() as cur:
            cur.execute("SELECT id_filme, titulo, duracao, classificacao_indicativa, genero FROM filme ORDER BY id_filme")
            rows = cur.fetchall()
            cols = [d[0] for d in cur.description]
            return [dict(zip(cols, r)) for r in rows]
    finally:
        con.close()

def buscar_filme_por_id(id_filme: int) -> Optional[Dict[str, Any]]:
    con = criar_conexao()
    try:
        with con.cursor() as cur:
            cur.execute("SELECT id_filme, titulo, duracao, classificacao_indicativa, genero FROM filme WHERE id_filme = %s", (id_filme,))
            row = cur.fetchone()
            if not row:
                return None
            cols = [d[0] for d in cur.description]
            return dict(zip(cols, row))
    finally:
        con.close()

def deletar_filme(id_filme: int) -> bool:
    con = criar_conexao()
    try:
        with con.cursor() as cur:
            cur.execute("DELETE FROM filme WHERE id_filme = %s RETURNING id_filme", (id_filme,))
            removed = cur.fetchone()
        con.commit()
        return removed is not None
    finally:
        con.close()

def atualizar_filme(id_filme: int, titulo: Optional[str] = None, duracao: Optional[int] = None,
    classificacao_indicativa: Optional[str] = None, genero: Optional[str] = None) -> bool:
    con = criar_conexao()
    try:
        campos = []
        valores = []

        if titulo:
            campos.append("titulo = %s")
            valores.append(titulo)

        if duracao:
            campos.append("duracao = %s")
            valores.append(duracao)

        if classificacao_indicativa:
            campos.append("classificacao_indicativa = %s")
            valores.append(classificacao_indicativa)

        if genero:
            campos.append("genero = %s")
            valores.append(genero)

        # Nada para atualizar
        if not campos:
            return False

        valores.append(id_filme)

        sql = f"UPDATE filme SET {', '.join(campos)} WHERE id_filme = %s RETURNING id_filme"

        with con.cursor() as cur:
            cur.execute(sql, valores)
            atualizado = cur.fetchone()

        con.commit()
        return atualizado is not None

    finally:
        con.close()

