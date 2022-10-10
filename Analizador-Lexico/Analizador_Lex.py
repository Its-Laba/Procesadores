""" ----------- Clase Analizador Léxico -------------"""
import Tokens.Token
from Tokens import Token

class AL:
    puntero = 0
    linea = 0
    cad = ""
    file = "../Test/prueba.txt"

def main():
    """ Main funcion del programa """
    archivo = open(AL.file, "r")
    if not archivo.readable():
        return "Mensaje de error numero 1: Archivo no se puede leer"
    lineas = archivo.readlines()
    archivo.close()
    procesar_lineas(lineas)
    print("FIN")

    pass

def procesar_lineas(lineas):
    token = 0
    sigo = True
    while sigo:
        # String
        if lineas[AL.linea][AL.puntero] == '\"':
            AL.puntero += 1
            cadena(lineas[AL.linea])
            token = Tokens.Token.T("CAD", '\"'+AL.cad+'\"')
            AL.cad = ""
        # Salto de linea
        elif lineas[AL.linea][AL.puntero] == '\n' or lineas[AL.linea][AL.puntero] == '\r':
            AL.linea += 1
            #EOF
            if AL.linea == len(lineas):
                AL.puntero += 1
                sigo = False
                token = Tokens.Token.T("EOF")
            AL.puntero = 0
        if token != 0:
            escribir(token)
            token = 0

    pass


def escribir(token):
    f = open("../Test/Archivos/Token.txt","a")
    f.write(token.__str__()+'\n')
    f.close()
    pass

def cadena(linea):

    if linea[AL.puntero] != '\n' and linea[AL.puntero] != '\"':
        AL.cad += linea[AL.puntero]
        AL.puntero += 1
        cadena(linea)
    elif linea[AL.puntero] == '\"':
        AL.puntero += 1
        if len(AL.cad) > 64:
            print(f"Error linea: {linea} la cadena supera los 64 caracteres")
            err()
    else:
        print(f"Error linea: {linea} se espera \" ")
        err()


def err():
    exit()


if __name__ == "__main__" :
    main()

