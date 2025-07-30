import os
import pyperclip
import xlsxwriter
import getpass
import urllib3
import ssl

from datetime import datetime
from typing import Dict
from termcolor import cprint
from xlsxwriter.format import Format
from xlsxwriter.workbook import Workbook
from xlsxwriter.worksheet import Worksheet

from .config import *
from .funciones_procesamiento_expediente import cargar_cursos_carrera
from .funciones_memory_reader import identificar_tipo, procesar_cursos_solicitados, procesar_expediente
from .funciones_io import leer_historial
from .funciones_xlsxwriter import generar_formatos
from .funciones_expediente import escribir_encabezado_expediente, escribir_expediente
from .funciones_web_scraping import iniciar_proceso_descarga
from .funciones_procesamiento_expediente import procesar_archivos_expedientes
from .funciones_consola import clear, leer_rango_numeros_enteros
from .custom_http_adapter import CustomHttpAdapter, get_legacy_session


def imprimir_finalizado() -> None:
    print("FINALIZADO")
    print("SI LA APLICACIÓN FUE DE UTILIDAD PUEDE DONAR")
    print("EL EQUIVALENTE A UN CAFECITO AL SINPE MOVIL 50123456 (SI ES UN NUMERO DE VERDAD)")
    print("SI REALMENTE LE GUSTO CONSIDERE DONAR UN WHOPPER")
    print("SI TIENE DUDAS, NO LLAME, NO WHATSAPP SOLO RESPONDO TELEGRAM")
    print("SIGA EL CANAL DE YT https://www.youtube.com/mauricioz7")


def imprimir_sin_datos_expediente() -> None:
    print("EXPEDIENTE SIN DATOS")


def imprimir_no_hay_datos() -> None:
    print("NO HAY DATOS PARA PROCESAR")


def imprimir_procesando_expediente() -> None:
    print("EXPEDIENTE PROCESADO")


def imprimir_procesando_cursos_solicitados() -> None:
    print("SOLICITUD PROCESADO")


def imprimir_generador_prematriculas() -> None:
    # https://patorjk.com/software/taag/#p=display&f=Graffiti&t=Type%20Something%20
    print("PROCESADOR DE PREMATRICULAS")
    print("Desarrollado por Mauricio Andrés Zamora Hernández")
    print("Versión 2022 ALFA")


def opcion_menu_procesar_memoria() -> None:
    imprimir_generador_prematriculas()
    sigla_cursos, semestre_cursos, expediente = cargar_cursos_carrera(detalle_cursos)

    texto: str = pyperclip.paste()
    procesar: bool = False

    tipo: str = identificar_tipo(texto)
    if tipo == 'pre':
        imprimir_procesando_cursos_solicitados()
        carne, nombre = procesar_cursos_solicitados(texto)
        imprimir_finalizado()
        procesar = True
    elif tipo == 'exp':
        imprimir_procesando_expediente()
        carne, nombre = procesar_expediente(texto)
        imprimir_finalizado()
        procesar = True
    else:
        imprimir_no_hay_datos()

    if procesar:
        procesar_archivos_expedientes()

    input('Presione enter para continuar')


def opcion_menu_pruebas() -> None:
    print('modo excel')
    carne = 'C03370'
    print('carne', carne)

    sigla_cursos, semestre_cursos, expediente = cargar_cursos_carrera(detalle_cursos)
    expediente.set_carne(carne)

    lineas = leer_historial(carne)
    for linea in lineas:
        expediente.agregar_curso(linea)

    existe_directorio: bool = os.path.isdir('./salida')
    if not existe_directorio:
        os.mkdir('./salida')
    workbook: Workbook = xlsxwriter.Workbook(
        os.path.join('./salida', '{}.xlsx'.format(carne)))

    worksheet: Worksheet = workbook.add_worksheet('malla')
    worksheet.hide_gridlines(2)

    formatos: Dict[str, Format] = generar_formatos(workbook)
    r, c = escribir_encabezado_expediente(expediente, workbook, worksheet, 0, 0, formatos)
    expediente.procesar_requisitos_correquisitos()
    escribir_expediente(expediente, workbook, worksheet, r, c, formatos)
    workbook.close()

    input('Presione enter para continuar')


def opcion_menu_informacion() -> None:
    ancho = 60
    print('{:{align}{width}}'.format('ESTA ES UNA VERSIÓN DE PRUEBA', align='^', width=ancho))
    print('{:{align}{width}}'.format('EN CADA PREMATRICULA ALGO SE AGREGA O CORRIJE', align='^', width=ancho))
    print()
    print('{:{align}{width}}'.format('ESTE SOFTWARE ES DE TIPO "AS IS"', align='^', width=ancho))
    print('{:{align}{width}}'.format('https://en.wikipedia.org/wiki/As_is', align='^', width=ancho))
    print()
    print('{:{align}{width}}'.format('Este script fue hecho en mi tiempo libre,', align='^', width=ancho))
    print('{:{align}{width}}'.format('si quieren invitar a un combo de BK por', align='^', width=ancho))
    print('{:{align}{width}}'.format('semestre que lo usen se les agradece.', align='^', width=ancho))
    print()
    print('{:{align}{width}}'.format('por Mauricio Zamora', align='^', width=ancho))
    print('{:{align}{width}}'.format('mauricio@zamora.cr', align='^', width=ancho))
    input('Presione enter para continuar')


def opcion_menu_descargar() -> None:
    print('POR FAVOR ESCRIBA SUS CREDENCIALES DE LA UCR')
    print('Usuario: (como el correo, pero sin el @ucr.ac.cr')
    data['user'] = input('')
    print('Usuario: ', data['user'])
    try:
        data['password'] = getpass.getpass()
    except Exception as error:
        print('ERROR', error)

    if iniciar_proceso_descarga():
        procesar_archivos_expedientes()
    input('Presione enter para continuar')


def opcion_menu_salir() -> None:
    print(':)')


def menu(ancho: int = 60) -> None:
    ahora = datetime.now()
    fecha_final = datetime(year=2026, month=2, day=28)
    duracion = fecha_final - ahora
    dias = duracion.days
    opcion: int = -1
    if dias >= 0:
        while opcion != 0:
            clear()
            texto = '{:{align}{width}}'.format('MENU PRINCIPAL', align='^', width=ancho)
            cprint(texto, 'blue', 'on_white')
            # opcion = '{:2d} > {:55}'.format(1, 'PROCESAR MEMORIA')
            # print('{:{align}{width}}'.format(opcion, align='^', width=ancho))

            opcion = '{:2d} > {:55}'.format(1, 'DESCARGAR EXPEDIENTES')
            print('{:{align}{width}}'.format(opcion, align='^', width=ancho))

            opcion = '{:2d} > {:55}'.format(2, 'INFORMACIÓN')
            print('{:{align}{width}}'.format(opcion, align='^', width=ancho))

            opcion = '{:2d} > {:55}'.format(3, 'PROCESAR EXPIDIENTE EN MEMORIA RAM')
            print('{:{align}{width}}'.format(opcion, align='^', width=ancho))

            opcion = '{:2d} > {:55}'.format(0, 'SALIR')
            print('{:{align}{width}}'.format(opcion, align='^', width=ancho))
            print(
                '{:{align}{width}}'.format('DESARROLLADO POR MAURICIO ANDRES ZAMORA HERNÁNDEZ', align='^', width=ancho))

            opcion = '{:3} DIAS PARA QUE DEJE FUNCIONAR ESTA VERSION DE PRUEBA'.format(dias)
            texto = '{:{align}{width}}'.format(opcion, align='^', width=ancho)
            cprint(texto, 'yellow', 'on_red')
            opcion = leer_rango_numeros_enteros('Digite la opción del menú:', 0, 4)
            if opcion == 0:
                opcion_menu_salir()
            elif opcion == 3:
                opcion_menu_procesar_memoria()
            # elif opcion == 4:
            #     opcion_menu_pruebas()
            elif opcion == 2:
                opcion_menu_informacion()
            elif opcion == 1:
                opcion_menu_descargar()

    else:
        print('{:{align}{width}}'.format('SE HA VENCIDO LA VERSION DE PRUEBAS', align='^', width=ancho))
        print('{:{align}{width}}'.format('POR FAVOR CONSULTAR POR LA VERSIÓN ACTUAL', align='^', width=ancho))
        print('{:{align}{width}}'.format('mauricio.zamora@gmail.com', align='^', width=ancho))
