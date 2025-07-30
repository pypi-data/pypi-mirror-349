import os
import csv
from typing import List


def escribir_cursos_solicitados(archivo: str, encabezado: List, cursos_solicitados: List) -> None:
    existe_directorio: bool = os.path.isdir('./solicitudes')
    if not existe_directorio:
        os.mkdir('./solicitudes')
    with open(os.path.join('./solicitudes', '{}.sdf'.format(archivo)), 'w', newline='') as file:
        writer = csv.writer(file, dialect='excel', delimiter='\t')
        writer.writerow(encabezado)
        for h in cursos_solicitados:
            writer.writerow(h)


def escribir_comentarios(archivo: str, estudiante: str, rev: str) -> None:
    existe_directorio: bool = os.path.isdir('./solicitudes')
    if not existe_directorio:
        os.mkdir('./solicitudes')
    f = open(os.path.join('./solicitudes', '{}.edf'.format(archivo)), "w")
    f.write('estudiante:')
    f.write(estudiante)
    f.write('\n')
    f.write('rev:')
    f.write(rev)
    f.close()


def escribir_historial(archivo: str, encabezado: List, historial: List) -> None:
    existe_directorio: bool = os.path.isdir('./expediente')
    if not existe_directorio:
        os.mkdir('./expediente')
    with open(os.path.join('./expediente', '{}.sdf'.format(archivo)), 'w', newline='') as file:
        writer = csv.writer(file, dialect='excel', delimiter='\t')
        writer.writerow(encabezado)
        for h in historial:
            writer.writerow(h)


def leer_historial(archivo: str) -> List:
    salida: List = []
    with open(os.path.join('./expediente', '{}.sdf'.format(archivo)), 'r', newline='') as file:
        reader = csv.DictReader(file, delimiter='\t', dialect='excel')
        # reader = csv.reader(file, delimiter='\t', dialect='excel')
        for linea in reader:
            salida.append(dict(linea))
    return salida


def escribir_informacion_estudiante(archivo: str, carne: str, nombre: str) -> None:
    existe_directorio: bool = os.path.isdir('./expediente')
    if not existe_directorio:
        os.mkdir('./expediente')
    f = open(os.path.join('./expediente', '{}.edf'.format(archivo)), "w")
    f.write(carne)
    f.write('\n')
    f.write(nombre)
    f.close()
