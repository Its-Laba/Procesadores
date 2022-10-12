""" ----------- Clase Analizador Léxico -------------"""
import Tokens.Token
import Tabla.Tabla_Simbolos
class AL:
    puntero = 0
    linea = 0
    cad = ""
    num = 0
    palres = ["if", "else", "function", "input", "return", "let", "print", "int", "string", "boolean"]
    file = "../Test/prueba.txt"
    tokens = []
    ids = []
def get_palres():
    return AL.palres
def main():
    """ Main funcion del programa """
    archivo = open(AL.file, "r")
    if not archivo.readable():
        return "Mensaje de error numero 1: Archivo no se puede leer"
    lineas = archivo.readlines()
    archivo.close()
    procesar_lineas(lineas)
    ts = Tabla.Tabla_Simbolos.TS()
    ts.setTokens(AL.tokens)
    ts.setIds(AL.ids)
    ts.process()
    ts.printTabla()

    print("FIN")

    pass

def procesar_lineas(lineas):
    token = 0
    sigo = True
    while sigo:
        #print(f"{len(lineas)}: {AL.linea} | {len(lineas[AL.linea])}: {AL.puntero} ")
        # String
        if len(lineas[AL.linea]) == AL.puntero:
            AL.puntero = 0
            AL.linea += 1
        elif lineas[AL.linea][AL.puntero] == '\"':
            AL.puntero += 1
            cadena(lineas[AL.linea])
            token = Tokens.Token.T("CAD", '\"'+AL.cad+'\"')
            AL.cad = ""
        # Producto y Producto Asignado
        elif lineas[AL.linea][AL.puntero] == '*':
            AL.puntero += 1
            if lineas[AL.linea][AL.puntero] == '=':
                AL.puntero += 1
                token = Tokens.Token.T("PrAsig")
            else:
                AL.puntero += 1
                token = Tokens.Token.T("Mult")

        # Asignaccion
        elif lineas[AL.linea][AL.puntero] == '=':
            AL.puntero += 1
            token = Tokens.Token.T("Asig")

        # AND
        elif lineas[AL.linea][AL.puntero] == '&':
            AL.puntero += 1
            if lineas[AL.linea][AL.puntero] == '&':
                AL.puntero += 1
                token = Tokens.Token.T("And")
            else:
                print("Error linea: {lineas[linea]}, se esperaba &")
                err()
        # Coma
        elif lineas[AL.linea][AL.puntero] == ',':
            AL.puntero += 1
            token = Tokens.Token.T("Coma")
        # Semicolon
        elif lineas[AL.linea][AL.puntero] == ';':
            AL.puntero += 1
            token = Tokens.Token.T("SEMICOL")
        # Parentesis Open
        elif lineas[AL.linea][AL.puntero] == '(':
            AL.puntero += 1
            token = Tokens.Token.T("OpenPar")
        # Parentesis Close
        elif lineas[AL.linea][AL.puntero] == ')':
            AL.puntero += 1
            token = Tokens.Token.T("ClosePar")
        # Llaves Open
        elif lineas[AL.linea][AL.puntero] == '{':
            AL.puntero += 1
            token = Tokens.Token.T("OpenLlav")
        # Llaves Close
        elif lineas[AL.linea][AL.puntero] == '}':
            AL.puntero += 1
            token = Tokens.Token.T("CloseLlav")
        # MayorQue
        elif lineas[AL.linea][AL.puntero] == '>':
            AL.puntero += 1
            token = Tokens.Token.T("MayorQue")
        # Init
        elif digit(lineas[AL.linea][AL.puntero]):
            AL.num = int(lineas[AL.linea][AL.puntero])
            AL.puntero += 1
            numeros(lineas[AL.linea])
            if AL.num < 32768:
                token = Tokens.Token.T("Entero", AL.num.__str__())
            else:
                print(f"Error en linea: {lineas[AL.linea]} el numero {AL.num} sobrepasas el limite")
                err()
            AL.num = 0
        elif letra(lineas[AL.linea][AL.puntero]):
            AL.cad = lineas[AL.linea][AL.puntero]
            AL.puntero += 1
            palabra(lineas[AL.linea])
            if AL.cad.__eq__("true"):
                token = Tokens.Token.T("Bool", AL.cad)
            elif AL.cad.__eq__("false"):
                token = Tokens.Token.T("Bool", AL.cad)
            elif AL.cad in AL.palres:
                token = Tokens.Token.T("Res", AL.cad)
            else:
                if AL.cad in AL.ids:
                    token = Tokens.Token.T("ID", AL.ids.index(AL.cad))
                else:
                    AL.ids.append(AL.cad)
                    token = Tokens.Token.T("ID", AL.ids.index(AL.cad))
            AL.cad = ""

        # Salto de linea
        elif lineas[AL.linea][AL.puntero] == '\n' or lineas[AL.linea][AL.puntero] == '\r':
            AL.linea += 1
            #EOF
            if AL.linea == len(lineas):
                sigo = False
                token = Tokens.Token.T("EOF")
            AL.puntero = 0
        else:
            AL.puntero += 1
        if token != 0:
            AL.tokens.append(token)
            escribir(token)
            token = 0

    pass

def digit (num):
    return num.isnumeric()

def numeros(linea):
    if digit(linea[AL.puntero]):
        AL.num = AL.num * 10 + int(linea[AL.puntero])
        AL.puntero += 1
        numeros(linea)
def letra (letra):
    return letra.isalpha()

def palabra (linea):
    if digit(linea[AL.puntero]) or letra(linea[AL.puntero]) or linea[AL.puntero] == '_':
        AL.cad += linea[AL.puntero]
        AL.puntero += 1
        palabra(linea)
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

