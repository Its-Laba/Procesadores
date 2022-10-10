""" -------- Clase Token ----------"""

class Token:
    def __init__(self,codigo,atributo = ""):
        self.codigo = codigo
        self.atributo = atributo

    def __str__(self):
        """ Formato de printeo del token"""
        return f"<{self.codigo}, {self.atributo}>"

    def getCodigo(self):
        return self.codigo

    def getAtributo(self):
        return self.atributo

    def setCodigo(self,codigo):
        self.codigo = codigo

    def setAtributo(self,atributo):
        self.atributo = atributo
