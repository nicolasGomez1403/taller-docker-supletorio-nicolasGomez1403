from fastapi.testclient import TestClient

from reservas.api import app


def test_estado():
    with TestClient(app) as cliente:
        respuesta = cliente.get("/estado")
    assert respuesta.status_code == 200
    assert respuesta.json() == {"estado": "listo"}


def test_motor_sin_variables_usa_sqlite():
    with TestClient(app) as cliente:
        respuesta = cliente.get("/motor")
    assert respuesta.json() == {"motor": "sqlite"}


def test_crear_y_listar_reserva():
    reserva = {"sala": "sala 3", "responsable": "ana", "franja": "10:00-12:00"}
    with TestClient(app) as cliente:
        creada = cliente.post("/reservas", json=reserva)
        listado = cliente.get("/reservas")
    assert creada.status_code == 200
    assert creada.json()["id"] is not None
    assert reserva.items() <= listado.json()[-1].items()
