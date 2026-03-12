from sqlalchemy import select, desc, func, text
from database import engine, SessionLocal
from models import (
    Usuario,
    Midia,
    ListaPersonalizada,
    ListaMidia,
    UsuarioMidia,
    Serie,
    Temporada,
)

# ==========================================================
# TESTE DE CONEXaO
# ==========================================================
with engine.connect() as conn:
    versao = conn.execute(text("SELECT version();")).fetchone()
    print("Conexão com PostgreSQL realizada com sucesso.")
    print(versao[0])


# PARTE 3: OPERAÇÕES CRUD VIA ORM
# ==========================================================
# FUNcoES AUXILIARES
# ==========================================================
def criar_usuario(session, nome: str) -> Usuario:
    usuario = Usuario(nome=nome)
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario


def criar_lista(session, id_usuario: int, nome_lista: str) -> ListaPersonalizada:
    lista = ListaPersonalizada(id_usuario=id_usuario, nome_lista=nome_lista)
    session.add(lista)
    session.commit()
    session.refresh(lista)
    return lista


# ==========================================================
# CREATE
# ==========================================================
with SessionLocal() as session:
    print("\n=== CREATE ===")

    u1 = criar_usuario(session, "Mariana Costa")
    u2 = criar_usuario(session, "Felipe Rocha")
    u3 = criar_usuario(session, "Camila Souza")

    print("Usuários inseridos com sucesso:")
    print(u1)
    print(u2)
    print(u3)

    lista = criar_lista(session, u1.id_usuario, "Maratonar depois")
    print("Lista criada:")
    print(lista)


# ==========================================================
# READ - listagem com ordenacao
# ==========================================================
with SessionLocal() as session:
    print("\n=== READ COM ORDENAÇÃO ===")

    midias = session.execute(
        select(Midia)
        .order_by(desc(Midia.nota_media), Midia.titulo.asc())
        .limit(10)
    ).scalars().all()

    for m in midias:
        print(m)


# ==========================================================
# UPDATE
# ==========================================================
with SessionLocal() as session:
    print("\n=== UPDATE ===")

    lista = session.execute(
        select(ListaPersonalizada)
        .where(ListaPersonalizada.nome_lista == "Para assistir")
    ).scalars().first()

    if lista:
        print("Antes:", lista)
        lista.nome_lista = "Assistir em breve"
        session.commit()
        session.refresh(lista)
        print("Depois:", lista)
    else:
        print("Lista não encontrada.")


# ==========================================================
# DELETE
# ==========================================================
with SessionLocal() as session:
    print("\n=== DELETE ===")

    registro = session.execute(
        select(ListaMidia)
        .where(ListaMidia.id_lista == 4, ListaMidia.id_midia == 1)
    ).scalars().first()

    if registro:
        print("Excluindo:", registro)
        session.delete(registro)
        session.commit()
        print("Registro removido com sucesso.")
    else:
        print("Registro não encontrado para exclusão.")

# PARTE 4: CONSULTAS COM RELACIONAMENTO
# ==========================================================
# CONSULTA 1
# listas e usuários
# ==========================================================
with SessionLocal() as session:
    print("\n=== CONSULTA 1: LISTAS E USUÁRIOS ===")

    resultados = session.execute(
        select(ListaPersonalizada, Usuario)
        .join(ListaPersonalizada.usuario)
        .order_by(Usuario.nome.asc(), ListaPersonalizada.nome_lista.asc())
    ).all()

    for lista, usuario in resultados:
        print(f"Lista: {lista.nome_lista} | Usuário: {usuario.nome}")


# ==========================================================
# CONSULTA 2
# histórico do usuário 1
# ==========================================================
with SessionLocal() as session:
    print("\n=== CONSULTA 2: HISTÓRICO DO USUÁRIO 1 ===")

    historico = session.execute(
        select(UsuarioMidia, Midia, Usuario)
        .join(UsuarioMidia.midia)
        .join(UsuarioMidia.usuario)
        .where(Usuario.id_usuario == 1)
        .order_by(Midia.titulo.asc())
    ).all()

    for reg, midia, usuario in historico:
        print(
            f"Usuário: {usuario.nome} | Mídia: {midia.titulo} "
            f"| Status: {reg.status} | Nota: {reg.nota}"
        )


# ==========================================================
# CONSULTA 3
# filtro + ordenação
# ==========================================================
with SessionLocal() as session:
    print("\n=== CONSULTA 3: FILTRO + ORDENAÇÃO ===")

    midias = session.execute(
        select(Midia)
        .where(Midia.ano >= 2010)
        .order_by(desc(Midia.nota_media), Midia.titulo.asc())
    ).scalars().all()

    for m in midias:
        print(f"{m.titulo} | Ano: {m.ano} | Nota: {m.nota_media}")


# ==========================================================
# CONSULTA 4
# agregação por relacionamento
# ==========================================================
with SessionLocal() as session:
    print("\n=== CONSULTA EXTRA: QUANTIDADE DE TEMPORADAS POR SÉRIE ===")

    resultados = session.execute(
        select(
            Midia.titulo,
            func.count(Temporada.id_temporada).label("qtd_temporadas")
        )
        .join(Serie, Serie.id_midia == Midia.id_midia)
        .join(Temporada, Temporada.id_serie == Serie.id_midia)
        .group_by(Midia.titulo)
        .order_by(desc("qtd_temporadas"), Midia.titulo.asc())
    ).all()

    for titulo, qtd in resultados:
        print(f"Série: {titulo} | Quantidade de temporadas: {qtd}")


print("\nExecução finalizada com sucesso.")