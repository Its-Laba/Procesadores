""" ----------- Clase Analizador Léxico -------------"""


def main():
    archivo = open("Test/prueba.py", "r")
    if not archivo.readable():
        return "Mensaje de error numero 1: Archivo no se puede leer"
    lineas = archivo.readlines()
    archivo.close()

