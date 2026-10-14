from sqlmodel import Field, SQLModel


class Reserva(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    sala: str = Field(max_length=60)
    responsable: str = Field(max_length=120)
    franja: str = Field(max_length=20)
