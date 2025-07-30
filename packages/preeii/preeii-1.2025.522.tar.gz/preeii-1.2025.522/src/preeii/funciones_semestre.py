from typing import Dict, Tuple
from xlsxwriter.format import Format
from xlsxwriter.workbook import Workbook
from xlsxwriter.worksheet import Worksheet

from .semestre import Semestre
from .funciones_curso import escribir_curso


def escribir_semestre_listado(semestre: Semestre, cuaderno: Workbook, hoja: Worksheet, fila: int, columna: int,
                              formatos: Dict[str, Format]) -> Tuple[int, int]:
    # print('Escribir semestre', semestre.get_numero())
    profundidad = semestre.obtener_maximo_historial()
    lista_siglas = semestre.get_siglas()
    # print('Max. historial : ' + str(profundidad))

    for id_sigla, sigla in enumerate(lista_siglas):
        # print(id_sigla, sigla)
        escribir_curso(semestre.get_cursos_por_siglas()[sigla], cuaderno, hoja, fila, id_sigla * 9, formatos,
                       profundidad)

    # print(profundidad + fila, columna)
    return profundidad + fila + 5, columna


def escribir_semestre(semestre: Semestre, cuaderno: Workbook, hoja: Worksheet, fila: int, columna: int,
                      formatos: Dict[str, Format]) -> Tuple[int, int]:
    # print('Escribir semestre', semestre.get_numero())
    profundidad = semestre.obtener_maximo_historial()
    lista_siglas = semestre.get_siglas()
    # print('Max. historial : ' + str(profundidad))

    for id_sigla, sigla in enumerate(lista_siglas):
        # print(id_sigla, sigla)
        escribir_curso(semestre.get_cursos_por_siglas()[sigla], cuaderno, hoja, fila, id_sigla * 9, formatos,
                       profundidad)

    # print(profundidad + fila, columna)
    return profundidad + fila + 5, columna
