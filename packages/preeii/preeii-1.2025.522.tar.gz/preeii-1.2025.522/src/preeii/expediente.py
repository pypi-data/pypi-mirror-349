from typing import List, Dict, Tuple
from .semestre import Semestre
from .curso_carrera import CursoCarrera
from .historial import Historial


class Expediente:
    def __init__(self) -> None:
        self.__semestres: Dict[int, Semestre] = {}
        self.__siglas: List[str] = []
        self.__optativos: List = []
        self.__otros_cursos: List = []
        self.__carne: str = ''
        self.__nombre: str = ''

    def get_carne(self) -> str:
        return self.__carne

    def set_carne(self, carne: str):
        if carne is not None:
            self.__carne = carne

    def get_nombre(self) -> str:
        return self.__nombre

    def set_nombre(self, nombre: str):
        if nombre is not None:
            self.__nombre = nombre

    def get_siglas(self) -> List[str]:
        return self.__siglas

    def get_optativos(self) -> List[str]:
        return self.__optativos

    def get_otros_cursos(self) -> List[str]:
        return self.__otros_cursos

    def obtener_semestres(self) -> Dict[int, Semestre]:
        return self.__semestres

    def agregar_semestre(self, semestre: Semestre) -> None:
        self.obtener_semestres()[semestre.get_numero()] = semestre
        self.get_siglas().extend(semestre.get_siglas())

    def obtener_semestres_completos(self) -> List[Tuple[int, bool]]:
        salida: List[Tuple[int, bool]] = []
        for i, c in self.obtener_semestres().items():
            salida.append((i, c.esta_completo()))
        return salida

    def agregar_curso(self, dicc: Dict[str, str]) -> None:
        sigla = dicc['SIGLA']
        sigla_normalizada = self.convertir_sigla_normalizada(sigla)
        nombre = dicc['CURSO']
        try:
            grupo = int(dicc['GRUPO'])
        except (ValueError, TypeError):
            grupo = int(0)

        if dicc['SEM'] == 'I':
            periodo = 1
        elif dicc['SEM'] == 'II':
            periodo = 2
        else:
            periodo = 3
        try:
            anno = int(dicc['AÑO'])
        except (ValueError, TypeError):
            anno = int(0)

        estado = dicc['ESTADO']
        nota = dicc['NOTA']
        try:
            nota = str(float(nota))
        except (ValueError, TypeError):
            if nota is None:
                nota = ''
        # print(dicc)
        encontro: bool = False
        for semestre in self.obtener_semestres().values():
            if semestre.tiene_curso(sigla_normalizada):
                encontro = True
                curso: CursoCarrera = semestre.get_cursos_por_siglas()[
                    sigla_normalizada]
                historial = Historial(
                    sigla, sigla_normalizada, nombre, grupo, periodo, anno, estado, nota)
                curso.agregar_historial(historial)
                # print(sigla, sigla_normalizada, ' en ', semestre)

        if not encontro:
            if sigla.startswith('II'):
                self.get_optativos().append(dicc)
            else:
                self.get_otros_cursos().append(dicc)
            # print(sigla, sigla_normalizada, ' no se encontro')

    def obtener_cursos_aprobados(self) -> List[str]:
        lista: List[str] = []
        for semestre in self.obtener_semestres().values():
            lista.extend(semestre.obtener_cursos_aprobados())

        lista.sort()
        return lista

    def obtener_cursos_matriculados(self) -> List[str]:
        lista: List[str] = []
        for semestre in self.obtener_semestres().values():
            lista.extend(semestre.obtener_cursos_matriculados())

        lista.sort()
        return lista

    def obtener_cursos_retirados(self) -> List[str]:
        lista: List[str] = []
        for semestre in self.obtener_semestres().values():
            lista.extend(semestre.obtener_cursos_retirados())

        lista.sort()
        return lista

    def obtener_cursos_reprobados(self) -> List[str]:
        lista: List[str] = []
        for semestre in self.obtener_semestres().values():
            lista.extend(semestre.obtener_cursos_reprobados())

        lista.sort()
        return lista

    def procesar_requisitos_correquisitos(self):
        # print('procesar_requisitos_correquisitos(self):')
        lista = self.obtener_cursos_aprobados()
        for semestre in self.obtener_semestres().values():
            for c in semestre.get_cursos():
                c.verificar_requisitos_correquisitos_aprobados(lista)

        lista = self.obtener_cursos_matriculados()
        for semestre in self.obtener_semestres().values():
            for c in semestre.get_cursos():
                c.verificar_requisitos_correquisitos_matriculados(lista)

        lista = self.obtener_cursos_reprobados()
        for semestre in self.obtener_semestres().values():
            for c in semestre.get_cursos():
                c.verificar_requisitos_correquisitos_reprobados(lista)

        lista = self.obtener_cursos_retirados()
        for semestre in self.obtener_semestres().values():
            for c in semestre.get_cursos():
                c.verificar_requisitos_correquisitos_retirados(lista)

    @staticmethod
    def convertir_sigla_normalizada(sigla: str) -> str:
        sigla_normalizada: str = sigla

        if sigla.startswith('EF'):
            sigla_normalizada = 'EF-D'
        elif sigla.startswith('RP'):
            sigla_normalizada = 'RP-1'
        elif sigla.startswith('EG03'):
            sigla_normalizada = 'EG-CA'
        elif sigla.startswith('EG0124'):
            sigla_normalizada = 'EG-I'
        elif sigla.startswith('EG0126'):
            sigla_normalizada = 'EG-I'
        elif sigla.startswith('EG0125'):
            sigla_normalizada = 'EG-II'
        elif sigla.startswith('EG0127'):
            sigla_normalizada = 'EG-II'
        elif sigla.startswith('SR0001'):
            sigla_normalizada = 'SR-I'
        elif sigla.startswith('SR0002'):
            sigla_normalizada = 'SR-I'
        elif sigla.startswith('SR0003'):
            sigla_normalizada = 'SR-I'
        elif sigla.startswith('SR0004'):
            sigla_normalizada = 'SR-I'
        elif sigla.startswith('SR0005'):
            sigla_normalizada = 'SR-I'
        elif sigla.startswith('SR0006'):
            sigla_normalizada = 'SR-I'
        elif sigla.startswith('SR0007'):
            sigla_normalizada = 'SR-I'
        elif sigla.startswith('SR0008'):
            sigla_normalizada = 'SR-I'
        elif sigla.startswith('SR0010'):
            sigla_normalizada = 'SR-I'
        elif sigla.startswith('SR0011'):
            sigla_normalizada = 'SR-II'
        elif sigla.startswith('SR0022'):
            sigla_normalizada = 'SR-II'
        elif sigla.startswith('SR0033'):
            sigla_normalizada = 'SR-II'
        elif sigla.startswith('SR0044'):
            sigla_normalizada = 'SR-II'
        elif sigla.startswith('SR0055'):
            sigla_normalizada = 'SR-II'
        elif sigla.startswith('SR0066'):
            sigla_normalizada = 'SR-II'
        elif sigla.startswith('SR0077'):
            sigla_normalizada = 'SR-II'
        elif sigla.startswith('SR0088'):
            sigla_normalizada = 'SR-II'
        elif sigla.startswith('SR0110'):
            sigla_normalizada = 'SR-II'
        return sigla_normalizada
