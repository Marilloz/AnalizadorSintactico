
class tipoAUX:

    def __init__(self,elem):
        self.elem = elem
        self.atribToken = ""
        self.tabla = 0
        self.atrib = []
        self.ordenAtributos = {
            "tipo": 0,
            "ancho": 1,
            "argumentos" : 2,
            "idParametros" : 3
        }

    def getElem(self):
        return self.elem

    def setAtribToken(self, atribToken):
        if self.elem == "2":
            self.atribToken = atribToken.split("-")[0]
            self.tabla = atribToken.split("-")[1]
        else:
            self.atribToken = atribToken

    def reDefAtribTokenID(self,newPosTS,newTabla):
        self.atribToken = newPosTS
        self.tabla = newTabla

    def getAtribToken(self):
        return self.atribToken
    
    def getTabla(self):
        return self.tabla

    def anadirAtrib(self,atrib):
        self.atrib.append(atrib)

    def getAtrib(self, nombre):
        return self.atrib[self.ordenAtributos[nombre]]

    def __str__(self):
        return f"{self.elem}-{self.atribToken}-{self.atrib}"