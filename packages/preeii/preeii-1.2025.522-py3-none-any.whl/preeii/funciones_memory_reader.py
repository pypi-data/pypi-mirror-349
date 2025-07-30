import re
from typing import Optional, Tuple
from .funciones_io import *
from .funciones_imprimir import imprimir_cursos_solicitados


def identificar_tipo(texto: str) -> Optional[str]:
    re_expediente = re.compile('(Expediente académico)')
    expediente = re_expediente.search(texto)
    re_prematricula = re.compile('(Cursos solicitados en prematrícula)')
    prematricula = re_prematricula.search(texto)
    if prematricula:
        return 'pre'
    elif expediente:
        return 'exp'
    else:
        return None


def procesar_cursos_solicitados(texto: str) -> Tuple[str, str]:
    re_carne = re.compile(
        r"Carné:\s+([A-Z]?\d{5})\s*\r\n")
    se_carne = re_carne.search(texto)
    carne = se_carne.group(1)

    re_nombre = re.compile(
        r"Nombre:\s+([\w\s]+)\s*\r\n")
    se_nombre = re_nombre.search(texto)
    nombre = se_nombre.group(1)

    re_comentario_estudiante = re.compile(
        r"Comentario del estudiante\r\n(.*)\r\n", re.IGNORECASE)
    se_comentario_estudiante = re_comentario_estudiante.search(texto)
    comentario_estudiante = se_comentario_estudiante.group(1)
    if comentario_estudiante.startswith('Cantidad de créditos solicitados'):
        comentario_estudiante = ''

    # print('Comentario estudiante:', comentario_estudiante)

    re_comentario_profesor = re.compile(
        r"Comentario hacia el Estudiante\s*\r\n(.*)\r\n", re.IGNORECASE)
    se_comentario_profesor = re_comentario_profesor.search(texto)
    comentario_profesor = se_comentario_profesor.group(1)
    if comentario_profesor.startswith('* Cursos con Declaración Jurada'):
        comentario_profesor = ''
    # print('Comentario profesor:', comentario_profesor)

    # print(carne, nombre)

    re_solicitudes = re.compile(
        r"(\*?)[ ]?([A-Z]{2}\d{4}|[A-Z]{2}-[A-Z]|[A-Z]{2}-[I]{1,3})\s*([\.:\dA-Z\(\) ÁÉÍÓÚÑ]+)\s+(\d{1,2}).*\r\n(.*)\r\n")

    solicitudes = []

    for match in re_solicitudes.finditer(texto):
        declaracion = match.group(1)
        sigla = match.group(2)
        curso = match.group(3)
        creditos = int(match.group(4))
        otros = match.group(5).strip()
        solicitudes.append(
            (sigla, curso, creditos, otros, 'SI' if declaracion == '*' else 'NO'))

    solicitudes = sorted(solicitudes, key=lambda x: (x[0]))
    escribir_cursos_solicitados(carne, [
        'SIGLA', 'CURSO', 'CREDITOS', 'AUTORIZACION', 'DEC'], solicitudes)
    escribir_comentarios(carne, comentario_estudiante, comentario_profesor)
    imprimir_cursos_solicitados(solicitudes)

    return carne, nombre


def procesar_expediente(texto: str) -> Tuple[str, str]:
    re_estudiante = re.compile(
        r"Carné:\s+([A-Z]?\d{5})\s+([\w\s]+)\r\n", re.VERBOSE)
    estudiante = re_estudiante.search(texto)
    carne = estudiante.group(1)
    nombre = estudiante.group(2)
    # print(carne, nombre)

    re_historial = re.compile(
        r"([A-Z]{2}\d{4})\s+([\.:\dA-Z\(\) ÁÉÍÓÚÑ]+)\s+(\d{1,2})\s+(\d{1,3})\s+([I]{1,3})\s+(\d{4})\s+([A-Z ]+)\s+(.+)\r\n")

    historial = []

    for match in re_historial.finditer(texto):
        sigla = match.group(1)
        curso = match.group(2)
        creditos = int(match.group(3))
        grupo = int(match.group(4))
        semestre = match.group(5)
        anno = int(match.group(6))
        estado = match.group(7)
        nota = match.group(8)
        historial.append((sigla, curso, creditos, grupo,
                          semestre, anno, estado, nota))

    historial = sorted(historial, key=lambda x: (x[5], x[4], x[0]))

    escribir_informacion_estudiante('{}'.format(carne), carne, nombre)
    escribir_historial(carne, [
        'SIGLA', 'CURSO', 'CREDITOS', 'GRUPO', 'SEM', 'AÑO', 'ESTADO', 'NOTA'], historial)
    # imprimir_historial(historial)
    return carne, nombre
