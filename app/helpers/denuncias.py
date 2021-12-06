
import enum


class EstadoDenuncias(enum.IntEnum):
    SinConfirmar: int = 1
    EnCurso: int = 2
    Resuelta: int = 3
    Cerrada: int = 4
class CategoriaDenuncias(enum.IntEnum):
    AlcantarillaTapada = 1
    Basural = 2
    Otro = 3

