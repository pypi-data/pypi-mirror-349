from typing import List


def imprimir_cursos_solicitados(cursos_solicitados: List) -> None:
    print('{:6} {:70} {:8} {:14} {:^3}'.format(
        'SIGLA', 'CURSO', 'CREDITOS', 'AUTORIZACION', 'DEC'))
    for cs in cursos_solicitados:
        sigla, curso, creditos, autorizacion, dec = cs
        print('{:6} {:70} {:^8d} {:^14} {:^3}'.format(
            sigla, curso, creditos, autorizacion, dec))


def imprimir_historial(historial: List) -> None:
    print('{:6} {:70} {:8} {:5} {:3} {:>4} {:>12} {:>4}'.format(
        'SIGLA', 'CURSO', 'CREDITOS', 'GRUPO', 'SEM', 'anno', 'ESTADO', 'NOTA'))
    for h in historial:
        sigla, curso, creditos, grupo, semestre, anno, estado, nota = h
        print('{:6} {:70} {:^8d} {:5d} {:>3} {:4d} {:12} {:>4}'.format(
            sigla, curso, creditos, grupo, semestre, anno, estado, nota))
