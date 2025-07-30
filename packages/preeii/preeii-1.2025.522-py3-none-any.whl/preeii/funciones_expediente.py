from typing import Dict, Tuple
from xlsxwriter.format import Format
from xlsxwriter.workbook import Workbook
from xlsxwriter.worksheet import Worksheet

from .expediente import Expediente
from .funciones_semestre import escribir_semestre_listado, escribir_semestre


def escribir_encabezado_expediente(expediente: Expediente, cuaderno: Workbook, hoja: Worksheet, fila: int, columna: int,
                                   formatos: Dict[str, Format]) -> Tuple[int, int]:
    row = fila
    col = columna
    formato_celda_wrap = formatos['formato_celda_wrap']
    hoja.merge_range(row, col, row, col + 1, 'CARNET:', formato_celda_wrap)
    hoja.merge_range(row, col + 2, row, col + 7, expediente.get_carne(), formato_celda_wrap)
    row += 1
    hoja.merge_range(row, col, row, col + 1, 'NOMBRE:', formato_celda_wrap)
    hoja.merge_range(row, col + 2, row, col + 7, expediente.get_nombre(), formato_celda_wrap)
    row += 2
    return row, col


def escribir_expediente_listado(expediente: Expediente, cuaderno: Workbook, hoja: Worksheet, fila: int, columna: int,
                                formatos: Dict[str, Format]):
    # print('Escribir expediente')
    row = fila
    col = columna

    lista_semestres = expediente.obtener_semestres().keys()
    for id_semestre in lista_semestres:
        row, col = escribir_semestre_listado(expediente.obtener_semestres()[id_semestre], cuaderno, hoja, row, col,
                                             formatos)
        # print('rc-', row, col)
        # print(expediente.obtener_semestres()[id_semestre].obtener_cursos_aprobados())


def escribir_expediente(expediente: Expediente, cuaderno: Workbook, hoja: Worksheet, fila: int, columna: int,
                        formatos: Dict[str, Format]):
    # print('Escribir expediente')
    row = fila
    col = columna

    lista_semestres = expediente.obtener_semestres().keys()
    for id_semestre in lista_semestres:
        row, col = escribir_semestre(expediente.obtener_semestres()[id_semestre], cuaderno, hoja, row, col, formatos)
        # print('rc-', row, col)
        # print(expediente.obtener_semestres()[id_semestre].obtener_cursos_aprobados())
