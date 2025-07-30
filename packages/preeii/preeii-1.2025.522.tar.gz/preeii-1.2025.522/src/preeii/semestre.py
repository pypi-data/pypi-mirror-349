from typing import List, Dict
from .curso_carrera import CursoCarrera


class Semestre:
    def __init__(self, numero: int) -> None:
        self.__numero: int = numero
        self.__cursos: List[CursoCarrera] = []
        self.__cursos_por_sigla: Dict[str, CursoCarrera] = {}
        self.__siglas: List[str] = []

    def obtener_cursos_aprobados(self) -> List[str]:
        return list(map(lambda c: c.get_sigla(),
                        filter(lambda c: c.get_estado() in ['APROBADO', 'EQUIVALENTE', 'CONVALIDADO'],
                               self.get_cursos())))

    def obtener_cursos_matriculados(self) -> List[str]:
        return list(map(lambda c: c.get_sigla(),
                        filter(lambda c: c.get_estado() in ['MATRICULADO'],
                               self.get_cursos())))

    def obtener_cursos_retirados(self) -> List[str]:
        return list(map(lambda c: c.get_sigla(),
                        filter(lambda c: c.get_estado() in ['RETIRO DE MA'],
                               self.get_cursos())))

    def obtener_cursos_reprobados(self) -> List[str]:
        return list(map(lambda c: c.get_sigla(),
                        filter(lambda c: c.get_estado() in ['REPROBADO'],
                               self.get_cursos())))

    def get_numero(self) -> int:
        return self.__numero

    def get_cursos(self) -> List[CursoCarrera]:
        return self.__cursos

    def get_cursos_por_siglas(self) -> Dict[str, CursoCarrera]:
        return self.__cursos_por_sigla

    def get_siglas(self) -> List[str]:
        return self.__siglas

    def agregar_curso(self, curso: CursoCarrera) -> None:
        self.get_cursos().append(curso)
        self.get_siglas().append(curso.get_sigla())
        self.get_cursos_por_siglas()[curso.get_sigla()] = curso
        self.get_siglas().sort()

    def obtener_maximo_historial(self) -> int:
        return max(map(lambda c: len(c.get_historial()), self.get_cursos()))

    def obtener_total_creditos(self) -> int:
        return sum(map(lambda c: c.get_creditos(), self.get_cursos()))

    def obtener_total_creditos_aprobados(self) -> int:
        return sum(
            map(lambda c: c.get_creditos(),
                filter(lambda f: f.get_estado() in ['APROBADO', 'EQUIVALENTE', 'CONVALIDADO'], self.get_cursos())))

    def obtener_maximo_requisitos(self) -> int:
        reqs = list(map(lambda c: len(c.get_requisitos()), filter(lambda f: f.tiene_requisitos(), self.get_cursos())))
        if reqs:
            return max(reqs)
        else:
            return 0

    def obtener_maximo_correquisitos(self) -> int:
        reqs = list(
            map(lambda c: len(c.get_correquisitos()), filter(lambda f: f.tiene_correquisitos(), self.get_cursos())))
        if reqs:
            return max(reqs)
        else:
            return 0

    def esta_completo(self) -> bool:
        return all([c.esta_aprobado() for c in self.get_cursos()])

    def __str__(self) -> str:
        return 'Semestre {:2}'.format(self.get_numero())

    def tiene_curso(self, sigla: str) -> bool:
        return sigla in self.get_siglas()
