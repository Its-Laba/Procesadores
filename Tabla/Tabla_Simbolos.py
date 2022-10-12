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

    def setTokens(self, tokens):
        self.tokens = tokens

    def process(self):
       function  = False
       para = False
       for num, token in enumerate(self.tokens):
            if para and token.getCodigo() == "CloseLlav":
                para = False
                self.tabla.append("Final")

            if token.getAtributo() in self.palRes:
                if token.getAtributo() == "function":
                    function = True

            if token.getCodigo() == "ID":
                if function:
                    self.addFunc(num)
                    function = False
                    para = True
                else:
                    self.addId(num)


    def getTabla(self):
        return self.tabla

    def addFunc(self, num):
        lista = [self.tokens[num].getAtributo(), "function", -1 ,self.tokens[num+1].getAtributo()]
        self.tabla.append(lista)
        self.tabla.append("Inicio")


    def addId(self,num):
        tipos = ["string", "int", "boolean"]
        lista = []
        if self.tokens[num+1].getAtributo() in tipos:
            if self.tokens[num+1].getAtributo() == "string":
                lista = [self.tokens[num].getAtributo(), "string", 128*8]
            else:
                lista = [self.tokens[num].getAtributo(), self.tokens[num+1].getAtributo(), 16]
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


