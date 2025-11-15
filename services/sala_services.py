from typing import Optional, List, Dict, Any
from config.db import criar_conexao

def inserir_sala(sala_num: int, capacidade: int) -> int:
    con = criar_conexao()
    try:
        with con.cursor() as cur:
            cur.execute(
                "INSERT INTO sala (sala, capacidade) VALUES (%s, %s) RETURNING id_sala",
                (sala_num, capacidade)
            )
            sid = cur.fetchone()[0]
        con.commit()
        return sid
    finally:
        con.close()

def listar_salas() -> List[Dict[str, Any]]:
    con = criar_conexao()
    try:
        with con.cursor() as cur:
            cur.execute("SELECT id_sala, sala, capacidade FROM sala ORDER BY id_sala")
            rows = cur.fetchall()
            cols = [d[0] for d in cur.description]
            return [dict(zip(cols, r)) for r in rows]
    finally:
        con.close()

def buscar_sala_por_numero(sala_num: int) -> Optional[Dict[str, Any]]:
    con = criar_conexao()
    try:
        with con.cursor() as cur:
            cur.execute("SELECT id_sala, sala, capacidade FROM sala WHERE sala = %s", (sala_num,))
            row = cur.fetchone()
            if not row:
                return None
            cols = [d[0] for d in cur.description]
            return dict(zip(cols, row))
    finally:
        con.close()

def deletar_sala(id_sala: int) -> bool:
    con = criar_conexao()
    try:
        with con.cursor() as cur:
            cur.execute("DELETE FROM sala WHERE id_sala = %s RETURNING id_sala", (id_sala,))
            removed = cur.fetchone()
        con.commit()
        return removed is not None
    finally:
        con.close()
