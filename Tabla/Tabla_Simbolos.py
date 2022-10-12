""" --------------- Clase de Tabla de Simbolos ---------------------------"""

import Tokens.Token
import Lexico.Analizador_Lex


class TS:
    def __init__(self):
        self.indice = 2
        self.registros = 0
        self.desp = 0
        self.palRes = Lexico.Analizador_Lex.get_palres()
        self.tabla = []
        self.tokens = []
        self.params = []

    def setTokens(self, tokens):
        self.tokens = tokens

    def process(self):
       function  = False
       llav = False
       para = False
       param = 0
       for num, token in enumerate(self.tokens):
            if para and token.getCodigo() == "ClosePar":
                para = False

            if llav and token.getCodigo() == "CloseLlav":
                llav = False
                self.params.append(param)
                param = 0
                self.tabla.append("Final")

            if token.getAtributo() in self.palRes:
                if token.getAtributo() == "function":
                    function = True

            if token.getCodigo() == "ID":
                if function:
                    self.addFunc(num)
                    function = False
                    llav = True
                    para = True

                else:
                    if llav:
                        param += 1
                    self.addId(num,para)


    def getTabla(self):
        return self.tabla

    def addFunc(self, num):
        lista = [self.tokens[num].getAtributo(), "function", -1 ,self.tokens[num+1].getAtributo()]
        self.tabla.append(lista)
        self.tabla.append("Inicio")


    def addId(self,num,fun = False):
        tipos = ["string", "int", "boolean"]
        lista = []
        if self.tokens[num+1].getAtributo() in tipos:
            if self.tokens[num+1].getAtributo() == "string":
                if not fun:
                    lista = [self.tokens[num].getAtributo(), "string", 128 * 8]
                else:
                    lista = [self.tokens[num].getAtributo(), "string", 0]
            else:
                if not fun:
                    lista = [self.tokens[num].getAtributo(), self.tokens[num+1].getAtributo(), 16]
                else:
                    lista = [self.tokens[num].getAtributo(), self.tokens[num + 1].getAtributo(), 0]
            self.tabla.append(lista)
    def addPal(self,token):
        """
        Posicion 0 = Lexema
        Posicion 1 = Tipo
        Posicion 2 = Direccion
        ----- solo funciones ------
        Posicion 3 = Numero Parametros
        Posicion 4 = Tipo devuleto
        Posicion 5 = Etiqueta
        :param token: Token
        """
        lista = [token.getAtributo(),token.getCodigo(), len(token.getAtributo())]
        self.tabla.append(lista)

    def printTabla(self):

        fun = False

        f = open("../Test/Archivos/Tabla.txt", "a")
        f.write("TABLA PRINCIPAL #1:\n")
        for num, fila in enumerate(self.tokens):
            if  isinstance(fila,list) and fila[1] != "function":
                f.write(f"* Lexema : \'{fila[0]}\'\n")
                if not fun:
                    f.write("  ATRIBUTOS:\n")
                f.write(f"    + tipo : {fila[1]}\n")
                f.write(f"    + despl : {fila[2]}\n")
                if not fun:
                    f.write("  --------------------------------")
                else:
                    f.write("\n")
            elif isinstance(fila,list) and fila[1] == "function":
                f.write(f"* Lexema : \'{fila[0]}\'\n")
                f.write("  ATRIBUTOS:\n")
                f.write(f"    + tipo : \'{fila[1]}\'\n")
                f.write(f"    + Nº Param: {(self).params.pop(0)}\n")
                f.write(f"    + tipoDevuelto : \'{fila[3]}\'\n")
                f.write(f"    + Etiqueta: \'Et{fila[0]}#{self.indice}\'")
                f.write("  --------------------------------")
            elif fila == "Inicio":
                f.write(f"TABLA DE LA FUNCION {self.tokens[num-1][0]}\n")
                fun = True
            elif fila == "Final":
                f.write("  --------------------------------")
                fun = False


