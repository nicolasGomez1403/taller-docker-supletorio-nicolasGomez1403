from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from sqlmodel import Session, select

from reservas.db import crear_tablas, engine, get_session
from reservas.modelos import Reserva


@asynccontextmanager
async def lifespan(app: FastAPI):
    crear_tablas()
    yield


app = FastAPI(title="Reservas de salas de estudio", lifespan=lifespan)


@app.get("/estado")
def estado():
    return {"estado": "listo"}


@app.get("/motor")
def motor():
    return {"motor": engine.dialect.name}


@app.get("/reservas")
def listar_reservas(session: Session = Depends(get_session)):
    return session.exec(select(Reserva)).all()


@app.post("/reservas")
def crear_reserva(reserva: Reserva, session: Session = Depends(get_session)):
    session.add(reserva)
    session.commit()
    session.refresh(reserva)
    return reserva
