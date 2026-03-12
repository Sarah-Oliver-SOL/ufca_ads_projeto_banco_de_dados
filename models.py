from datetime import date
from sqlalchemy import Integer, String, Date, DECIMAL, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


SCHEMA = "etapa3"

# ==========================================================
# PARTE 2: MAPEAMENTO ORM
# ==========================================================
class Usuario(Base):
    __tablename__ = "usuario"
    __table_args__ = {"schema": SCHEMA}

    id_usuario: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)

    listas: Mapped[list["ListaPersonalizada"]] = relationship(back_populates="usuario")
    historico_midias: Mapped[list["UsuarioMidia"]] = relationship(back_populates="usuario")

    def __repr__(self):
        return f"Usuario(id_usuario={self.id_usuario}, nome={self.nome!r})"


class Midia(Base):
    __tablename__ = "midia"
    __table_args__ = {"schema": SCHEMA}

    id_midia: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    titulo: Mapped[str] = mapped_column(String(150), nullable=False)
    genero: Mapped[str] = mapped_column(String(50), nullable=False)
    ano: Mapped[int] = mapped_column(Integer, nullable=False)
    duracao: Mapped[int | None] = mapped_column(Integer, nullable=True)
    class_indicativa: Mapped[str | None] = mapped_column(String(10), nullable=True)
    elenco: Mapped[str | None] = mapped_column(String(250), nullable=True)
    nota_media: Mapped[float | None] = mapped_column(DECIMAL, nullable=True)

    serie: Mapped["Serie | None"] = relationship(back_populates="midia", uselist=False)
    listas_assoc: Mapped[list["ListaMidia"]] = relationship(back_populates="midia")
    usuarios_assoc: Mapped[list["UsuarioMidia"]] = relationship(back_populates="midia")

    def __repr__(self):
        return (
            f"Midia(id_midia={self.id_midia}, titulo={self.titulo!r}, "
            f"ano={self.ano}, nota_media={self.nota_media})"
        )


class Serie(Base):
    __tablename__ = "serie"
    __table_args__ = {"schema": SCHEMA}

    id_midia: Mapped[int] = mapped_column(
        ForeignKey(f"{SCHEMA}.midia.id_midia", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )

    midia: Mapped["Midia"] = relationship(back_populates="serie")
    temporadas: Mapped[list["Temporada"]] = relationship(back_populates="serie")

    def __repr__(self):
        return f"Serie(id_midia={self.id_midia})"


class Temporada(Base):
    __tablename__ = "temporada"
    __table_args__ = {"schema": SCHEMA}

    id_temporada: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_serie: Mapped[int] = mapped_column(
        ForeignKey(f"{SCHEMA}.serie.id_midia", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False
    )
    numero_temporada: Mapped[int] = mapped_column(Integer, nullable=False)

    serie: Mapped["Serie"] = relationship(back_populates="temporadas")
    episodios: Mapped[list["Episodio"]] = relationship(back_populates="temporada")

    def __repr__(self):
        return (
            f"Temporada(id_temporada={self.id_temporada}, "
            f"numero_temporada={self.numero_temporada})"
        )


class Episodio(Base):
    __tablename__ = "episodio"
    __table_args__ = {"schema": SCHEMA}

    id_episodio: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_temporada: Mapped[int] = mapped_column(
        ForeignKey(f"{SCHEMA}.temporada.id_temporada", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False
    )
    numero_episodio: Mapped[int] = mapped_column(Integer, nullable=False)
    titulo: Mapped[str | None] = mapped_column(String(150), nullable=True)
    duracao_minutos: Mapped[int | None] = mapped_column(Integer, nullable=True)
    data_lancamento: Mapped[date | None] = mapped_column(Date, nullable=True)
    status: Mapped[str | None] = mapped_column(String(20), nullable=True)
    nota: Mapped[float | None] = mapped_column(DECIMAL, nullable=True)

    temporada: Mapped["Temporada"] = relationship(back_populates="episodios")

    def __repr__(self):
        return f"Episodio(id_episodio={self.id_episodio}, titulo={self.titulo!r})"


class ListaPersonalizada(Base):
    __tablename__ = "lista_personalizada"
    __table_args__ = {"schema": SCHEMA}

    id_lista: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_usuario: Mapped[int] = mapped_column(
        ForeignKey(f"{SCHEMA}.usuario.id_usuario", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False
    )
    nome_lista: Mapped[str | None] = mapped_column(String(50), nullable=True)

    usuario: Mapped["Usuario"] = relationship(back_populates="listas")
    midias_assoc: Mapped[list["ListaMidia"]] = relationship(back_populates="lista")

    def __repr__(self):
        return (
            f"ListaPersonalizada(id_lista={self.id_lista}, "
            f"id_usuario={self.id_usuario}, nome_lista={self.nome_lista!r})"
        )


class ListaMidia(Base):
    __tablename__ = "lista_midia"
    __table_args__ = {"schema": SCHEMA}

    id_lista: Mapped[int] = mapped_column(
        ForeignKey(f"{SCHEMA}.lista_personalizada.id_lista", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )
    id_midia: Mapped[int] = mapped_column(
        ForeignKey(f"{SCHEMA}.midia.id_midia", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )

    lista: Mapped["ListaPersonalizada"] = relationship(back_populates="midias_assoc")
    midia: Mapped["Midia"] = relationship(back_populates="listas_assoc")

    def __repr__(self):
        return f"ListaMidia(id_lista={self.id_lista}, id_midia={self.id_midia})"


class UsuarioMidia(Base):
    __tablename__ = "usuario_midia"
    __table_args__ = {"schema": SCHEMA}

    id_usuario: Mapped[int] = mapped_column(
        ForeignKey(f"{SCHEMA}.usuario.id_usuario", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )
    id_midia: Mapped[int] = mapped_column(
        ForeignKey(f"{SCHEMA}.midia.id_midia", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )
    status: Mapped[str | None] = mapped_column(String(20), nullable=True)
    nota: Mapped[float | None] = mapped_column(DECIMAL, nullable=True)
    data_conclusao: Mapped[date | None] = mapped_column(Date, nullable=True)

    usuario: Mapped["Usuario"] = relationship(back_populates="historico_midias")
    midia: Mapped["Midia"] = relationship(back_populates="usuarios_assoc")

    def __repr__(self):
        return (
            f"UsuarioMidia(id_usuario={self.id_usuario}, id_midia={self.id_midia}, "
            f"status={self.status!r}, nota={self.nota})"
        )