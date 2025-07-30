from typing import Dict
from xlsxwriter.format import Format
from xlsxwriter.workbook import Workbook
from xlsxwriter.worksheet import Worksheet

from .curso_carrera import CursoCarrera


def escribir_curso(curso: CursoCarrera, cuaderno: Workbook, hoja: Worksheet, fila: int, columna: int,
                   formatos: Dict[str, Format], relleno_historial: int = 0):
    row: int = fila
    col: int = columna

    formato_celda_centrado = formatos['formato_celda_centrado']
    formato_celda_wrap = formatos['formato_celda_wrap']
    formato_celda_wrap_verde = formatos['formato_celda_wrap_verde']
    formato_celda_wrap_rojo = formatos['formato_celda_wrap_rojo']
    formato_celda_wrap_amarillo = formatos['formato_celda_wrap_amarillo']
    formato_celda_centrado_verde = formatos['formato_celda_centrado_verde']
    # formato_celda_centrado_rojo = formatos['formato_celda_centrado_rojo']
    formato_celda_centrado_amarillo = formatos['formato_celda_centrado_amarillo']
    # Bloque 1
    hoja.write(row, col, curso.get_sigla(), formato_celda_centrado)
    row += 1
    hoja.write(row, col, curso.get_creditos(), formato_celda_centrado)
    row += 1
    try:
        nota: float = float(curso.get_nota())
        hoja.merge_range(row, col, row + 1, col, nota, formato_celda_centrado)
    except (ValueError, TypeError):
        hoja.merge_range(row, col, row + 1, col, curso.get_nota(), formato_celda_centrado)

    # Bloque 2
    row = fila
    col += 1

    if curso.get_estado() in ['APROBADO', 'EQUIVALENTE', 'CONVALIDADO']:
        hoja.merge_range(row, col, row + 2, col + 4, curso.get_nombre(), formato_celda_wrap_verde)
    elif curso.get_estado() in ['MATRICULADO']:
        hoja.merge_range(row, col, row + 2, col + 4, curso.get_nombre(), formato_celda_wrap_amarillo)
    elif curso.get_estado() in ['RETIRO DE MA']:
        hoja.merge_range(row, col, row + 2, col + 4, curso.get_nombre(), formato_celda_wrap_rojo)
    elif curso.get_estado() in ['REPROBADO']:
        hoja.merge_range(row, col, row + 2, col + 4, curso.get_nombre(), formato_celda_wrap_rojo)
    else:
        hoja.merge_range(row, col, row + 2, col + 4, curso.get_nombre(), formato_celda_wrap)
    row += 3
    hoja.merge_range(row, col, row, col + 4, curso.get_estado(), formato_celda_wrap)

    # Bloque 3 y 4
    temp_row = fila
    temp_col = col + 5
    for r in range(temp_row, temp_row + 4):
        hoja.write_blank(r, temp_col, None, formato_celda_centrado)
        hoja.write_blank(r, temp_col + 1, None, formato_celda_centrado)

    req_correq: Dict[str, int] = {}
    req_correq.update(curso.get_requisitos())
    req_correq.update(curso.get_correquisitos())
    siglas_rc = list(req_correq.keys())
    siglas_rc.sort()
    if len(siglas_rc) > 4:
        bloque_3 = siglas_rc[:4]
        bloque_4 = siglas_rc[4:]
    else:
        bloque_3 = siglas_rc
        bloque_4 = []

    # Bloque 3
    for r, rcq in enumerate(bloque_3, temp_row):
        if rcq in curso.get_requisitos():
            if curso.get_requisitos()[rcq] == 4:
                f = formato_celda_centrado_verde
            elif curso.get_requisitos()[rcq] == 0:
                f = formato_celda_centrado
            elif curso.get_requisitos()[rcq] == 1:
                f = formato_celda_centrado_amarillo
            else:
                f = formato_celda_centrado
        else:
            if curso.get_correquisitos()[rcq] == 4:
                f = formato_celda_centrado_verde
            elif curso.get_correquisitos()[rcq] == 0:
                f = formato_celda_centrado
            elif curso.get_correquisitos()[rcq] == 1:
                f = formato_celda_centrado_amarillo
            else:
                f = formato_celda_centrado
        hoja.write(r, temp_col, rcq, f)

    # Bloque 4
    for r, rcq in enumerate(bloque_4, temp_row):
        if rcq in curso.get_requisitos():
            # print('req/cor', rcq, curso.py.get_requisitos()[rcq])
            if curso.get_requisitos()[rcq] == 4:
                f = formato_celda_centrado_verde
            elif curso.get_requisitos()[rcq] == 0:
                f = formato_celda_centrado
            elif curso.get_requisitos()[rcq] == 1:
                f = formato_celda_centrado_amarillo
            else:
                f = formato_celda_centrado
        else:
            if curso.get_correquisitos()[rcq] == 4:
                f = formato_celda_centrado_verde
            elif curso.get_correquisitos()[rcq] == 0:
                f = formato_celda_centrado
            elif curso.get_correquisitos()[rcq] == 1:
                f = formato_celda_centrado_amarillo
            else:
                f = formato_celda_centrado
        hoja.write(r, temp_col + 1, rcq, f)

    # Bloque 5
    row += 1
    col -= 1
    for r, h in enumerate(curso.get_historial(), row):
        row += 1
        hoja.write(r, col, h.get_sigla(), formato_celda_centrado)
        hoja.merge_range(r, col + 1, r, col + 5, h.get_nombre(), formato_celda_wrap)
        hoja.write(r, col + 6, '{:1}-{:4}'.format(h.get_periodo(), h.get_anno()), formato_celda_centrado)
        try:
            nota = float(h.get_nota())
            hoja.write_number(r, col + 7, nota, formato_celda_centrado)
        except (ValueError, TypeError):
            hoja.write(r, col + 7, h.get_nota(), formato_celda_centrado)
    lineas_blancas = relleno_historial - len(curso.get_historial())
    for lb in range(lineas_blancas):
        hoja.merge_range(row, col, row, col + 7, '', formato_celda_wrap)
        row += 1
