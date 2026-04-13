"""
database.py — Conexão e configuração do banco de dados SQLite
"""

import sqlite3
from contextlib import contextmanager

DATABASE = "banco.db"


@contextmanager
def get_conn():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def criar_tabela():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                nome        TEXT    NOT NULL,
                email       TEXT    UNIQUE NOT NULL,
                telefone    TEXT,
                cidade      TEXT,
                empresa     TEXT,
                cpf_cnpj    TEXT    UNIQUE,
                criado      TEXT    DEFAULT (datetime('now', 'localtime'))
            )
        """)