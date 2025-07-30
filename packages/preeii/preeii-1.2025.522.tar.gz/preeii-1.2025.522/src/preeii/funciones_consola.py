from os import system, name


def clear() -> None:
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux
    else:
        _ = system('clear')


def leer_numero_entero(etiqueta: str = None) -> int:
    if etiqueta is not None:
        print(etiqueta)
    continuar: bool = True
    numero_entero: int = 0
    while continuar:
        numero = input()
        continuar = False
        try:
            numero_entero = int(numero)
        except (ValueError, TypeError):
            continuar = True
            print('El valor no es entero, por favor reintente: ')

    return numero_entero


def leer_rango_numeros_enteros(etiqueta: str = None, rango_inferior: int = 0, rango_superior: int = 99999999) -> int:
    numero_entero: int = leer_numero_entero(etiqueta)
    continuar: bool = True
    while continuar:
        if rango_inferior <= numero_entero <= rango_superior:
            continuar = False
        else:
            print('Debe digitar un número entre {} y {}'.format(rango_inferior, rango_superior))
            numero_entero: int = leer_numero_entero(etiqueta)

    return numero_entero
