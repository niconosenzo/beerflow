
from datetime import time

lista_horarios = [time(x, y) for x in range(0, 24) for y in range(0, 60, 5)]

HORA = tuple([(x, x.isoformat()) for x in lista_horarios])

DEVOLUCION = (
    ("Lleno", "Lleno"),
    ("Mitad", "Mitad"),
    ("Vacio", "Vacio"),
)
