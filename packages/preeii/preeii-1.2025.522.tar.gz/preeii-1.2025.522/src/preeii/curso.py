class Curso:
    def __init__(self, sigla: str, nombre: str, creditos: int, nota: str = None, anno: int = None, periodo: int = None,
                 semestre: int = None, estado: str = '', sigla_normalizada: str = None):
        self.__sigla: str = sigla
        self.__sigla_normalizada: str = sigla_normalizada
        self.__nombre: str = nombre
        self.__creditos: int = creditos
        self.__semestre: int = semestre
        self.__estado: str = estado
        self.__nota: str = nota
        self.__anno: int = anno
        self.__periodo: int = periodo

    def get_sigla(self) -> str:
        return self.__sigla

    def set_sigla(self, sigla: str) -> None:
        self.__sigla = sigla

    def get_sigla_normalizada(self) -> str:
        if self.__sigla_normalizada is None:
            return self.get_sigla()
        else:
            return self.__sigla_normalizada

    def set_sigla_normalizada(self, sigla_normalizada: str) -> None:
        self.__sigla_normalizada = sigla_normalizada

    def get_nombre(self) -> str:
        return self.__nombre

    def set_nombre(self, nombre: str) -> None:
        self.__nombre = nombre

    def get_creditos(self) -> int:
        return self.__creditos

    def set_creditos(self, creditos: int) -> None:
        self.__creditos = creditos

    def get_semestre(self) -> int:
        return self.__semestre

    def set_semestre(self, semestre: int) -> None:
        self.__semestre = semestre

    def get_estado(self) -> str:
        return self.__estado

    def set_estado(self, estado: str) -> None:
        self.__estado = estado

    def __str__(self):
        return '{:8} {:8} {:75} {:2d} {:15}'.format(self.get_sigla(), self.get_sigla_normalizada(), self.get_nombre(),
                                                    self.__creditos, self.get_estado())

    def get_nota(self) -> str:
        return self.__nota

    def set_nota(self, nota: str) -> None:
        self.__nota = nota

    def get_anno(self) -> int:
        return self.__anno

    def set_anno(self, anno: int) -> None:
        self.__anno = anno

    def get_periodo(self) -> int:
        return self.__periodo

    def set_periodo(self, periodo: int) -> None:
        self.__periodo = periodo
