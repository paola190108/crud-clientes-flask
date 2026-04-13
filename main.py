from crud import (
    criar_tabela,
    criar_usuario,
    listar_usuarios,
    buscar_por_id,
    buscar_por_nome,
    buscar_por_email,
    atualizar_usuario,
    deletar_usuario,
)


def separador(titulo: str):
    print(f"\n{'═' * 50}")
    print(f"  {titulo}")
    print(f"{'═' * 50}")


if __name__ == "__main__":

    # ── Setup ──────────────────────────────────────
    separador("1. CRIANDO A TABELA")
    criar_tabela()

    # ── CREATE ─────────────────────────────────────
    separador("2. CREATE — Inserindo usuários")
    criar_usuario("Ana Silva",    "ana@email.com",    28)
    criar_usuario("Bruno Lima",   "bruno@email.com",  34)
    criar_usuario("Carla Dias",   "carla@email.com",  22)
    criar_usuario("Daniel Souza", "daniel@email.com", 41)
    criar_usuario("Ana Costa",    "anacosta@email.com", 30)

    # ── READ — listar todos ────────────────────────
    separador("3. READ — Listando todos")
    listar_usuarios()

    # ── READ — buscar por ID ───────────────────────
    separador("4. READ — Buscar por ID")
    buscar_por_id(1)
    buscar_por_id(99)  # inexistente

    # ── READ — buscar por nome ─────────────────────
    separador("5. READ — Buscar por nome (parcial)")
    buscar_por_nome("ana")    # encontra "Ana Silva" e "Ana Costa"
    buscar_por_nome("Lima")   # encontra "Bruno Lima"

    # ── READ — buscar por e-mail ───────────────────
    separador("6. READ — Buscar por e-mail (exato)")
    buscar_por_email("carla@email.com")
    buscar_por_email("naoexiste@email.com")

    # ── UPDATE ─────────────────────────────────────
    separador("7. UPDATE — Atualizando usuário ID 2")
    atualizar_usuario(2, nome="Bruno Santos", idade=35)

    separador("8. READ — Verificando atualização")
    buscar_por_id(2)

    # ── DELETE ─────────────────────────────────────
    separador("9. DELETE — Deletando usuário ID 4")
    deletar_usuario(4)
    deletar_usuario(99)  # inexistente

    # ── Estado final ───────────────────────────────
    separador("10. READ — Estado final da tabela")
    listar_usuarios()

    print("\nDemo concluída com sucesso!\n")