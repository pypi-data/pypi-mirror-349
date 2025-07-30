from typing import Dict
from xlsxwriter.format import Format
from xlsxwriter.workbook import Workbook


def generar_formatos(cuaderno: Workbook) -> Dict[str, Format]:
    formatos: Dict[str, Format] = {}

    formato_celda_wrap = cuaderno.add_format()
    formatos['formato_celda_wrap'] = formato_celda_wrap
    formato_celda_wrap.set_align('center')
    formato_celda_wrap.set_align('vcenter')
    formato_celda_wrap.set_text_wrap()
    formato_celda_wrap.set_border(1)

    formato_celda_wrap_verde = cuaderno.add_format()
    formatos['formato_celda_wrap_verde'] = formato_celda_wrap_verde
    formato_celda_wrap_verde.set_align('center')
    formato_celda_wrap_verde.set_align('vcenter')
    formato_celda_wrap_verde.set_text_wrap()
    formato_celda_wrap_verde.set_bg_color('green')
    formato_celda_wrap_verde.set_border(1)

    formato_celda_wrap_rojo = cuaderno.add_format()
    formatos['formato_celda_wrap_rojo'] = formato_celda_wrap_rojo
    formato_celda_wrap_rojo.set_align('center')
    formato_celda_wrap_rojo.set_align('vcenter')
    formato_celda_wrap_rojo.set_text_wrap()
    formato_celda_wrap_rojo.set_bg_color('red')
    formato_celda_wrap_rojo.set_border(1)

    formato_celda_wrap_amarillo = cuaderno.add_format()
    formatos['formato_celda_wrap_amarillo'] = formato_celda_wrap_amarillo
    formato_celda_wrap_amarillo.set_align('center')
    formato_celda_wrap_amarillo.set_align('vcenter')
    formato_celda_wrap_amarillo.set_text_wrap()
    formato_celda_wrap_amarillo.set_bg_color('yellow')
    formato_celda_wrap_amarillo.set_border(1)

    formato_celda_centrado = cuaderno.add_format()
    formatos['formato_celda_centrado'] = formato_celda_centrado
    formato_celda_centrado.set_align('center')
    formato_celda_centrado.set_align('vcenter')
    formato_celda_centrado.set_border(1)

    formato_celda_centrado_verde = cuaderno.add_format()
    formatos['formato_celda_centrado_verde'] = formato_celda_centrado_verde
    formato_celda_centrado_verde.set_align('center')
    formato_celda_centrado_verde.set_align('vcenter')
    formato_celda_centrado_verde.set_border(1)
    formato_celda_centrado_verde.set_bg_color('green')

    formato_celda_centrado_amarillo = cuaderno.add_format()
    formatos['formato_celda_centrado_amarillo'] = formato_celda_centrado_amarillo
    formato_celda_centrado_amarillo.set_align('center')
    formato_celda_centrado_amarillo.set_align('vcenter')
    formato_celda_centrado_amarillo.set_border(1)
    formato_celda_centrado_amarillo.set_bg_color('yellow')

    formato_celda_centrado_rojo = cuaderno.add_format()
    formatos['formato_celda_centrado_rojo'] = formato_celda_centrado_rojo
    formato_celda_centrado_rojo.set_align('center')
    formato_celda_centrado_rojo.set_align('vcenter')
    formato_celda_centrado_rojo.set_border(1)
    formato_celda_centrado_rojo.set_bg_color('red')

    return formatos
