# lexema | tipoLexema | desplazamiento | numParam | tipoParam | modoPaso | tipoDevuelto | Etiq

# TS : <key, val>
#      key: lexema
#      val: atributosTS -> array

class tablaSimbolos:

    def __init__(self, num):
        self.tabla = {}
        self.num = num
        self.desp = 0

    def existeID(self, posTS):
        posTS = int(posTS)
        for fila in self.tabla.values():
            if fila.indice == posTS:
                return True
        return False

    def getTipo(self, posTS):
        posTS = int(posTS)
        for fila in self.tabla.values():
            if fila.indice == posTS:
                return fila.tipo

    def insertarFila(self, lexema, atributoTS):
        if lexema not in self.tabla:
            self.tabla.setdefault(lexema, atributoTS)
            tam_atrib = atributoTS.desplazamiento
            atributoTS.desplazamiento = self.desp
            atributoTS.setIndex(len(self.tabla)-1)
            self.desp += tam_atrib
            atributoTS.contador += 1
            return len(self.tabla)-1
        else:
            fila = self.tabla.get(lexema)
            fila.contador += 1
            return fila.indice

    def getLexema(self, posTS):
        posTS = int(posTS)
        for lexema in self.tabla.keys():
            if self.tabla[lexema].indice == posTS:
                return lexema
            
    def getParametros(self,posTS):
        posTS = int(posTS)
        for fila in self.tabla.values():
            if fila.indice == posTS:
                return fila.tipoParam
            
    def getTipoDevuelto(self,posTS):
        posTS = int(posTS)
        for fila in self.tabla.values():
            if fila.indice == posTS:
                return fila.tipoDevuelto
            
    def eliminarFila(self, lexema):
        v = self.tabla.pop(lexema)
        return v

    def anadirTipoTS(self, posTS, tipo, desp):
        for fila in self.tabla.values():
            if fila.indice == posTS:
                fila.tipo = tipo
                fila.desplazamiento = desp

    def anadirTipoDevuelto(self,posTS,tipo):
        for fila in self.tabla.values():
            if fila.indice == posTS:
                fila.tipoDevuelto = tipo

    def anadirParametros(self,posTS,parametros):
        for fila in self.tabla.values():
            if fila.indice == posTS:
                fila.numParam = self.contarEspacios(parametros) +1
                fila.tipoParam = parametros

    def contarEspacios(self,string):
        count = 0
        if string == "tipoVacio":
            return -1;
        for i in range(0, len(string)):
            if string[i] == " ":
                count += 1
        return count

    def limpiarTS(self):
        self.tabla.clear()

    def __str__(self):
        keys = []
        for k in self.tabla.keys():
            if self.tabla.get(k).tipo == "noDeclarado":
                keys.append(k)
        for k2 in keys:
            self.tabla.pop(k2)
        cadena = f"\n \nMostrando contenido de la tabla # {self.num} : \n"
        for key in self.tabla:
            linea = self.tabla.get(key)
            cadena += f"\n* LEXEMA : \'{key}\' \n"
            cadena += f" ATRIBUTOS:\n"
            cadena += f"  + Tipo: \'{linea.tipo}\' \n"
            cadena += f"  + Despl: {linea.desplazamiento} \n"
            if linea.numParam is not None:
                cadena += f"  + numParam: {linea.numParam} \n"
            if linea.tipoParam is not None and linea.tipoParam != "tipoVacio":
                cadena += f"  + TipoParam: {linea.tipoParam} \n"
            if linea.modoPaso is not None:
                cadena += f"  + ModoParam: {linea.modoPaso} \n"
            if linea.tipoDevuelto is not None and linea.tipoDevuelto != "tipoVacio":
                cadena += f"  + TipoRetorno: {linea.tipoDevuelto} \n"
            if linea.etiq is not None:
                cadena += f"  + EtiqFuncion: {linea.etiq} \n"
            if linea.param is not None:
                cadena += f"  + Param: {linea.param} \n"

            # cadena += f"{key} | {linea.tipo} | {linea.desplazamiento} | {linea.numParam} | {linea.tipoParam} | {
            # linea.modoPaso} | {linea.tipoDevuelto} | {linea.etiq}\n"
            cadena += "----------------------------------------------------"
        return cadena


class atributosTS:

    def __init__(self, tipo, desplazamiento, numParam, tipoParam, modoPaso, tipoDevuelto, etiq, param):
        self.indice = 0
        self.tipo = tipo  # tipo de dato
        self.desplazamiento = desplazamiento  # num bytes usados en memoria
        self.numParam = numParam  # numero de parametros (solo funciones)
        self.tipoParam = tipoParam  # tipo de los paramatros (solo funciones) (array)
        self.modoPaso = modoPaso  # modo en el que se pasan los parametros (solo funciones) (array)
        self.tipoDevuelto = tipoDevuelto  # tipo Devuelto (solo funciones)
        self.etiq = etiq  # Un identificador para las funciones del estilo de Et1_funcion1
        self.param = param
        self.contador = 0

    def setIndex(self,index):
        self.indice = index