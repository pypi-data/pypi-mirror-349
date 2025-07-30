class Historial:
    def __init__(self, sigla: str, sigla_normalizada: str, nombre: str, grupo: int, periodo: int, anno: int,
                 estado: str,
                 nota: str):
        self.__sigla: str = sigla
        self.__sigla_normalizada: str = sigla_normalizada
        self.__nombre: str = nombre
        self.__grupo: int = grupo
        self.__periodo: int = periodo
        self.__anno: int = anno
        self.__estado: str = estado
        self.__nota: str = nota

    def get_sigla(self) -> str:
        return self.__sigla

    def set_sigla(self, sigla: str) -> None:
        self.__sigla = sigla

    def get_sigla_normalizada(self) -> str:
        return self.__sigla_normalizada

    def set_sigla_normalizada(self, sigla_normalizada: str) -> None:
        self.__sigla_normalizada = sigla_normalizada

    def get_nombre(self) -> str:
        return self.__nombre

    def set_nombre(self, nombre: str) -> None:
        self.__nombre = nombre

    def get_grupo(self) -> int:
        return self.__grupo

    def set_grupo(self, grupo: int) -> None:
        self.__grupo = grupo

    def get_periodo(self) -> int:
        return self.__periodo

    def set_periodo(self, periodo: int) -> None:
        self.__periodo = periodo

    def get_anno(self) -> int:
        return self.__anno

    def set_anno(self, anno: int) -> None:
        self.__anno = anno

    def get_estado(self) -> str:
        return self.__estado

    def set_estado(self, estado: int) -> None:
        self.__estado = estado

    def get_nota(self) -> str:
        return self.__nota

    def set_nota(self, nota: str) -> None:
        self.__nota = nota

    def __str__(self):
        if self.get_nota() is None:
            nota = ''
        else:
            nota = self.get_nota()

        return '{:8} {:8} {:75} {:3} {:4} {:4} {:15}'.format(self.get_sigla(), self.get_sigla_normalizada(),
                                                             self.get_nombre(), self.get_periodo(), self.get_anno(),
                                                             nota, self.get_estado())
