import os
from pathlib import Path

from sqlalchemy import URL
from sqlmodel import Session, SQLModel, create_engine

RESERVAS_DB_HOST = os.environ.get("RESERVAS_DB_HOST")

if RESERVAS_DB_HOST:
    url = URL.create(
        "mariadb+pymysql",
        username=os.environ.get("RESERVAS_DB_USUARIO"),
        password=os.environ.get("RESERVAS_DB_CLAVE"),
        host=RESERVAS_DB_HOST,
        port=int(os.environ.get("RESERVAS_DB_PUERTO", "3306")),
        database=os.environ.get("RESERVAS_DB_NOMBRE"),
    )
    engine = create_engine(url, pool_pre_ping=True)
else:
    engine = create_engine("sqlite:///./instancia/reservas.db", connect_args={"check_same_thread": False})


def crear_tablas() -> None:
    if engine.dialect.name == "sqlite":
        Path(engine.url.database).parent.mkdir(exist_ok=True)
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
