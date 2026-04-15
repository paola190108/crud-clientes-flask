import psycopg2
import os

def get_connection():
    # O Railway fornece a DATABASE_URL automaticamente
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise ValueError("A variável DATABASE_URL não foi encontrada. Verifique as configurações do Railway.")
    return psycopg2.connect(url)

def criar_tabela():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id SERIAL PRIMARY KEY,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            telefone TEXT,
            cidade TEXT,
            empresa TEXT,
            cpf_cnpj TEXT UNIQUE
        );
    """)
    conn.commit()
    cursor.close()
    conn.close()
    print("Tabela verificada/criada com sucesso.")