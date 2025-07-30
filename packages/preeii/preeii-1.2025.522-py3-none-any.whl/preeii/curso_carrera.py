from typing import List, Dict, Optional
from .curso import Curso
from .historial import Historial


class CursoCarrera(Curso):
    def __init__(self, sigla: str, nombre: str, creditos: int, nota: str = None, anno: int = None, periodo: int = None,
                 semestre: int = None, estado: str = ''):
        super().__init__(sigla, nombre, creditos, nota, anno, periodo, semestre, estado)
        self.__historial: List[Historial] = []
        self.__requisitos: Dict[str, int] = {}  # 0 Sin datos, 1 Matriculado 2 Reprobado 3 Retirado 4 Aprobado 5 Conv.
        self.__correquisitos: Dict[
            str, int] = {}  # 0 Sin datos, 1 Matriculado 2 Reprobado 3 Retirado 4 Aprobado 5 Conv.

    def get_historial(self) -> List[Historial]:
        return self.__historial

    def get_requisitos(self) -> Dict[str, int]:
        return self.__requisitos

    def tiene_requisitos(self) -> bool:
        return bool(self.get_requisitos())

    def agregar_requisito(self, sigla: str) -> None:
        self.get_requisitos()[sigla] = 0

    def cumple_requisitos(self) -> bool:
        requisitos: List[bool] = [x == 4 for x in self.get_requisitos().values()]
        return not requisitos or all(requisitos)

    def get_correquisitos(self) -> Dict[str, int]:
        return self.__correquisitos

    def tiene_correquisitos(self) -> bool:
        return bool(self.get_correquisitos())

    def agregar_correquisito(self, sigla: str) -> None:
        self.get_correquisitos()[sigla] = 0

    def cumple_correquisitos(self) -> bool:
        return not self.get_correquisitos().values() or all([x == 4 for x in self.get_correquisitos().values()])

    def verificar_requisitos_correquisitos_aprobados(self, siglas_cursos_aprobados: List[str]):
        if siglas_cursos_aprobados:
            for sigla in self.get_requisitos().keys():
                if sigla in siglas_cursos_aprobados:
                    self.get_requisitos()[sigla] = 4
            for sigla in self.get_correquisitos().keys():
                if sigla in siglas_cursos_aprobados:
                    self.get_correquisitos()[sigla] = 4

    def verificar_requisitos_correquisitos_matriculados(self, siglas_cursos_matriculados: List[str]):
        if siglas_cursos_matriculados:
            for sigla in self.get_requisitos().keys():
                if sigla in siglas_cursos_matriculados:
                    self.get_requisitos()[sigla] = 1
            for sigla in self.get_correquisitos().keys():
                if sigla in siglas_cursos_matriculados:
                    self.get_correquisitos()[sigla] = 1

    def verificar_requisitos_correquisitos_reprobados(self, siglas_cursos_reprobados: List[str]):
        if siglas_cursos_reprobados:
            for sigla in self.get_requisitos().keys():
                if sigla in siglas_cursos_reprobados:
                    self.get_requisitos()[sigla] = 2
            for sigla in self.get_correquisitos().keys():
                if sigla in siglas_cursos_reprobados:
                    self.get_correquisitos()[sigla] = 2

    def verificar_requisitos_correquisitos_retirados(self, siglas_cursos_retirados: List[str]):
        if siglas_cursos_retirados:
            for sigla in self.get_requisitos().keys():
                if sigla in siglas_cursos_retirados:
                    self.get_requisitos()[sigla] = 3
            for sigla in self.get_correquisitos().keys():
                if sigla in siglas_cursos_retirados:
                    self.get_correquisitos()[sigla] = 3

    def agregar_historial(self, historial: Historial):
        self.__historial.append(historial)
        self.__historial.sort(key=lambda h: (
            h.get_anno(), h.get_periodo()), reverse=True)

    def get_nota(self) -> str:
        if self.get_historial():
            return self.get_historial()[0].get_nota()
        else:
            return ''

    def get_estado(self) -> str:
        if self.get_historial():
            return self.get_historial()[0].get_estado()
        else:
            return ''

    def esta_aprobado(self) -> bool:
        return self.get_estado() in ['APROBADO', 'EQUIVALENTE', 'CONVALIDADO']

    def get_anno(self) -> Optional[int]:
        if self.get_historial():
            return self.get_historial()[0].get_anno()
        else:
            return None

    def get_periodo(self) -> Optional[int]:
        if self.get_historial():
            return self.get_historial()[0].get_periodo()
        else:
            return None

    def __str__(self):
        periodo = self.get_periodo() if not self.get_periodo() is None else ''
        anno = self.get_anno() if not self.get_anno() is None else ''
        salida: str = '\t' + '{} {:>3} {:4} {:4}'.format(super().__str__(), periodo, anno, self.get_nota())
        salida = salida + '\n'
        if self.get_historial():
            salida = salida + '\t\tHistorial:'
            for h in self.get_historial():
                salida = salida + '\n\t\t' + str(h)
        else:
            salida = salida + '\t\t' + 'Sin Historial'
        return salida
