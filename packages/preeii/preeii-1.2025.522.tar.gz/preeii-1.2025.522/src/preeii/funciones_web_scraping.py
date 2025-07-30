import requests
from .config import *
from .student_parser import StudentParser
from .main_listing_parser import MainListingParser
from .funciones_io import escribir_historial, escribir_informacion_estudiante
from .custom_http_adapter import CustomHttpAdapter, get_legacy_session
import re
from termcolor import cprint
import urllib3
import ssl

def procesar_expediente_estudiante(texto):
    student_parser = StudentParser()
    student_parser.feed(texto)
    return student_parser.get_lista()


def descargar_expediente_estudiante(carne, nombre, clave, sess):
    r = sess.get(url_notas.format(clave))
    return r.text


def iniciar_proceso_descarga() -> bool:
    se_puedo_descargar = False
    # s = requests.Session()
    # s.post(url_login, data=data)
    s = get_legacy_session(data, url_login)
    r = s.get(url_listado)
    contenido = r.text
    match = re.findall(r'Listado de estudiantes asignados al profesor', contenido)

    if match:
        se_puedo_descargar = True
        main_listing_parser = MainListingParser()
        main_listing_parser.feed(contenido)
        estudiantes = main_listing_parser.get_lista()
        textos = []
        for estudiante in estudiantes:
            clave = estudiante[0]
            carne = estudiante[1:2][0]
            nombre = estudiante[2:3][0]
            correo = estudiante[-1]
            texto = descargar_expediente_estudiante(carne, nombre, clave, s)
            textos.append(texto)
            lineas = procesar_expediente_estudiante(texto)
            escribir_historial(carne, ['SIGLA', 'CURSO', 'CREDITOS', 'GRUPO', 'SEM', 'AÑO', 'ESTADO', 'NOTA'], lineas)
            escribir_informacion_estudiante(carne, carne, nombre)


    else:
        cprint('NO SE HA PODIDO OBTENER LA INFORMACIÓN, FAVOR VERIFIQUE SUS CREDENCIALES (USUARIO Y CLAVE)', 'white',
               'on_red', attrs=['bold'])

    return se_puedo_descargar
