from html.parser import HTMLParser
from typing import List


class StudentParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.__lista: List[List[str]] = []
        self.__bandera_table: bool = False
        self.__bandera_tr_header: bool = False
        self.__bandera_tr: bool = False
        self.__bandera_lectura: bool = False
        self.__contador: int = 0
        self.__datos: List[str] = []

    def get_lista(self) -> List[List[str]]:
        self.__lista.sort(key=lambda x: (x[5], x[4], x[0]), reverse=True)
        return self.__lista

    def handle_starttag(self, tag, attrs):
        if tag == 'table':
            self.__bandera_table = True

        if tag == 'tr' and not self.__bandera_tr_header:
            self.__bandera_tr_header = True

        if tag == 'tr' and self.__bandera_tr_header:
            self.__bandera_tr = True
            self.__contador = 0

        if tag == 'td' and self.__bandera_tr:
            self.__bandera_lectura = True

    def handle_data(self, data):
        if self.__bandera_lectura:
            if self.__contador == 0:
                self.__datos = []

            t = data.strip()
            if self.__contador == 4:
                t = ' '.join(data.strip().split())
                t = t.split(' ')
                # if t[0] == 'I':
                #     t[0] = '1'
                # elif t[0] == 'II':
                #     t[0] = '2'
                # elif t[0] == 'III':
                #     t[0] = '3'
                self.__datos.extend(t)
            else:
                if self.__contador == 6:
                    try:
                        t = float(t)
                    except (ValueError, TypeError):
                        t = t.strip()

                self.__datos.append(t)

            if self.__contador == 6:
                self.__lista.append(self.__datos)
            self.__contador += 1

    def handle_endtag(self, tag):
        if tag == 'tr' and self.__bandera_tr_header:
            self.__bandera_tr = False

        if tag == 'td' and self.__bandera_tr_header:
            self.__bandera_lectura = False
