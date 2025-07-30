import base64

from html.parser import HTMLParser
from typing import List


class MainListingParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.__lista: List[List[str]] = []
        self.__estudiante_detectado: bool = False
        self.__contador: int = 0
        self.__datos: List[str] = []

    def get_lista(self) -> List[List[str]]:
        return self.__lista

    def handle_starttag(self, tag, attrs):
        if tag == 'input':
            dic = dict(attrs)
            if 'name' in dic and dic['name'] == 'radio':
                clave = '!!'.join(dic['value'].split(','))
                clave = base64.b64encode(clave.encode("utf-8")).decode("utf-8")
                self.__estudiante_detectado = True
                self.__datos = []
                self.__datos.append(clave)
                self.__lista.append(self.__datos)

        if tag == 'td' and self.__estudiante_detectado:
            self.__contador += 1
            if self.__contador == 5:
                self.__contador = 0
                self.__estudiante_detectado = False
                # self.__lista.append(self.__datos)

    def handle_data(self, data):
        if self.__estudiante_detectado:
            if data.strip() != '':
                self.__datos.append(data.strip())
