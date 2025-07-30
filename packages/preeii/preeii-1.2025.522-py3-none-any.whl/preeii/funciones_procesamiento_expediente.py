import os
import xlsxwriter

from datetime import timedelta
from typing import List, Dict, Tuple
from termcolor import cprint
from xlsxwriter.format import Format
from xlsxwriter.workbook import Workbook
from xlsxwriter.worksheet import Worksheet

from .config import *
from .semestre import Semestre
from .curso_carrera import CursoCarrera
from .expediente import Expediente
from .funciones_io import leer_historial
from .funciones_xlsxwriter import generar_formatos
from .funciones_expediente import escribir_encabezado_expediente, escribir_expediente


def cargar_cursos_carrera(listado_cursos: List) -> Tuple[Dict[str, CursoCarrera], Dict[int, Semestre], Expediente]:
    sigla_cursos: Dict[str, CursoCarrera] = {}
    semestre_cursos: Dict[int, Semestre] = {}
    expediente = Expediente()
    for detalle_curso in listado_cursos:
        sigla = detalle_curso['sigla']
        nombre = detalle_curso['curso.py']
        semestre = detalle_curso['semestre']
        creditos = detalle_curso['creditos']
        curso = CursoCarrera(sigla, nombre, creditos, semestre=semestre)

        if 'requisitos' in detalle_curso:
            requisitos = detalle_curso['requisitos']
            for requisito in requisitos:
                curso.agregar_requisito(requisito)

        if 'correquisitos' in detalle_curso:
            correquisitos = detalle_curso['correquisitos']
            for correquisito in correquisitos:
                curso.agregar_correquisito(correquisito)

        sigla_cursos[sigla] = curso
        if semestre not in semestre_cursos:
            semestre_cursos[semestre] = Semestre(semestre)
        semestre_cursos[semestre].agregar_curso(curso)

    for sem in semestre_cursos.values():
        expediente.agregar_semestre(sem)

    return sigla_cursos, semestre_cursos, expediente


def procesar_archivos_expedientes() -> None:
    lista_archivos = os.listdir('./expediente')
    impar: bool = True
    tiempo_total = timedelta(seconds=0)
    texto = '{:9} {:69} {:>9} {:>10}'.format('CARNE', 'NOMBRE', 'LINEAS', 'TIEMPO')
    cprint(texto, 'magenta', 'on_yellow')
    for archivo in lista_archivos:
        if archivo.endswith('.edf'):
            with open(os.path.join('./expediente', '{}'.format(archivo))) as f:
                lineas = f.readlines()
                lineas = [linea if not linea.endswith('\n') else linea[:-1] for linea in lineas]
                carne = lineas[0]
                nombre = lineas[1]

                # with open(os.path.join('./expediente', '{}.sdf'.format(carne))) as f:

                sigla_cursos, semestre_cursos, expediente = cargar_cursos_carrera(detalle_cursos)
                expediente.set_carne(carne)
                expediente.set_nombre(nombre)

                lineas = leer_historial(carne)
                for linea in lineas:
                    expediente.agregar_curso(linea)

                # MZ
                # print('MZ', expediente.obtener_semestres_completos())
                tiempo = timedelta(minutes=1) + len(lineas) * timedelta(seconds=20)
                tiempo_total += tiempo
                impar = not impar

                texto = '{:9} {:69} {:9} {:>10}'.format(carne, nombre, len(lineas), str(tiempo))
                if impar:
                    cprint(texto, 'blue', 'on_white')
                else:
                    cprint(texto, 'blue', 'on_cyan')

                existe_directorio: bool = os.path.isdir('./salida')
                if not existe_directorio:
                    os.mkdir('./salida')
                workbook: Workbook = xlsxwriter.Workbook(
                    os.path.join('./salida', '{}-{}.xlsx'.format(carne, nombre.upper())))

                worksheet: Worksheet = workbook.add_worksheet('malla')
                worksheet.hide_gridlines(2)

                formatos: Dict[str, Format] = generar_formatos(workbook)
                r, c = escribir_encabezado_expediente(expediente, workbook, worksheet, 0, 0, formatos)
                expediente.procesar_requisitos_correquisitos()
                escribir_expediente(expediente, workbook, worksheet, r, c, formatos)
                workbook.close()

    texto = 'TIEMPO TOTAL ESTIMADO QUE USTED SE AHORRO SOLO EN ESTA ETAPA: {}'.format(tiempo_total)
    texto = '{:^100}'.format(texto)
    cprint(texto, 'cyan', 'on_red', attrs=['bold', 'blink'])
