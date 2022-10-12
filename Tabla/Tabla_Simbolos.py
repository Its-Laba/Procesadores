""" --------------- Clase de Tabla de Simbolos ---------------------------"""

import Tokens.Token
import Lexico.Analizador_Lex


class TS:
    def __init__(self):
        self.indice = 2
        self.registros = 0
        self.desp = 0
        self.fun_des = 0
        self.palRes = Lexico.Analizador_Lex.get_palres()
        self.tabla = []
        self.tokens = []
        self.params = []
        self.ids = []

    def setTokens(self, tokens):
        self.tokens = tokens
    def setIds(self, ids):
        self.ids = ids
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
                    if para:
                        param += 1
                    self.addId(num,para)


    def getTabla(self):
        return self.tabla

    def addFunc(self, num):
        lista = [self.tokens[num].getAtributo(), "function", -1 ,self.tokens[num+1].getAtributo()]
        self.tabla.append(lista)
        self.tabla.append("Inicio")
        self.fun_des = 0


    def addId(self,num,fun = False):
        tipos = ["string", "int", "boolean"]
        lista = []
        if self.tokens[num+1].getAtributo() in tipos or self.tokens[num - 1].getAtributo() in tipos:
            if self.tokens[num+1].getAtributo() == "string" or self.tokens[num - 1].getAtributo() == "string":
                if not fun:
                    lista = [self.ids[self.tokens[num].getAtributo()], "string", self.desp ]
                    self.desp += 128
                else:
                    lista = [self.ids[self.tokens[num].getAtributo()], "string", self.fun_des]
                    self.fun_des += 128
            else:
                if not fun:
                    lista = [self.ids[self.tokens[num].getAtributo()], self.tokens[num + 1].getAtributo(), self.desp]
                    self.desp += 2
                else:
                    lista = [self.ids[self.tokens[num].getAtributo()], self.tokens[num - 1].getAtributo(), self.fun_des]
                    self.desp += 2
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
        print(self.tabla)
        fun = False
        zero = False
        f = open("../Test/Archivos/Tabla.txt", "a")
        f.write("TABLA PRINCIPAL #1:\n")
        for num, fila in enumerate(self.tabla):
            if isinstance(fila, list) and fila[1] != "function":
                f.write(f"* LEXEMA : \'{fila[0]}\'\n")
                if not fun:
                    f.write("  ATRIBUTOS:\n")
                f.write(f"    + tipo : \'{fila[1]}\'\n")
                f.write(f"    + despl : {fila[2]}\n")
                if not fun:
                    f.write("  --------------------------------\n")
                else:
                    f.write("\n")
            elif isinstance(fila, list) and fila[1] == "function":
                f.write(f"* LEXEMA : \'{self.ids[fila[0]]}\'\n")
                f.write("  ATRIBUTOS:\n")
                f.write(f"    + tipo : \'{fila[1]}\'\n")
                param = (self).params.pop(0)
                f.write(f"    + NumParam: {param}\n")
                if param == 0:
                    zero = True
                f.write(f"    + tipoRetorno : \'{fila[3]}\'\n")
                f.write(f"    + EtiqFuncion: \'Et{self.ids[fila[0]]}{self.indice}\'\n")
                f.write("  --------------------------------\n")
            elif fila == "Inicio" and not zero:
                f.write(f"TABLA DE LA FUNCION {self.ids[self.tabla[num-1][0]]} #{self.indice}:\n")
                fun = True
                self.indice += 1
            elif fila == "Final":
                if not zero:
                    f.write("  --------------------------------\n")
                fun = False
                zero = False


