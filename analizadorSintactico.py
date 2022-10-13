from os import remove
from collections import deque
from analizadorLexico import analizador_lexico
from tablaSimbolos import tablaSimbolos
from tablaSimbolos import atributosTS
from pilaAUX import tipoAUX

class AnalizadorSintactico:

    def __init__(self, n_fich):

        self.tabla = None
        self.n_regla = None
        # self.tabla = numpy.zeros((21, 31))  # matriz de 21 filas y 31 columnas, a ceros
        self.token_list = []
        self.parse = "Descendente "
        self.parseAux = ""
        self.pila = deque()
        self.pilaAUX = deque()
        # self.sig_token = token("", "")
        self.token = ""
        self.atrib = ""
        self.sacarNuevoToken = True

        self.tablaSimbolosG = tablaSimbolos(1)
        self.tablaSimbolosL = tablaSimbolos(2)
        self.tablaActual = 0
        self.anLex = analizador_lexico(n_fich, self.tablaSimbolosG, self.tablaSimbolosL)

        self.despG = 0
        self.despL = 0
        self.zonaReturn = False

        # matriz de decision (noTerminales x Terminales : reglas)
        self.crearTablaReglas()
        self.actualizarTablaReglas()

        self.nombre_fich = n_fich
        try:
            remove(f"salida{self.nombre_fich}/{self.nombre_fich}.Errores.txt")
        except FileNotFoundError:
            print("", end="")
        self.fd = open(f"salida{self.nombre_fich}/{self.nombre_fich}.Tokens.txt", "r")

        # self.pila.append("$")
        self.pila.append(tipoAUX("P"))

        self.tradNoTerm = ["P", "B", "T", "S", "S'", "X", "C", "L", "Q", "F", "H", "A", "K",
                           "E", "E'", "R", "R'", "U", "U'", "V", "V'"]

        # sacar todos los codigos de la lista de tokens del fichero y meterlos en token_list

        '''
        while (cod_token := self.fd.readline()) != "":
            cod_token = cod_token.split(",")[0].split("<")[1]
            self.token_list.append(cod_token)
        '''

        self.tradTerm = ["Entero","Cadena","ID", "true", "false", "+", "*", "==", "<", "&&", "--", "=", "let","int", "string", "boolean","print", "input", "function","return","if","do","while","(",")","{","}","",",",";","EOF"]

        # Ya tenemos lista de tokens y matriz de decision,
        # empezamos analizador descendente tabular

        self.ejec1_1()
        self.tabular()

    # llena una matriz 21x31 de E (error)
    def crearTablaReglas(self):
        self.tabla = []
        for i in range(21):
            fila = []
            for j in range(31):
                fila.append("E")
            self.tabla.append(fila)

        self.n_regla = []
        for i in range(21):
            fila =[]
            for j in range(31):
                fila.append("E")
            self.n_regla.append(fila)

    # inserta las reglas en la matriz de decisión
    def actualizarTablaReglas(self):
        tabla = self.tabla
        n_regla = self.n_regla
        # P
        for i in [2, 12, 16, 17, 19, 20, 21]:
            tabla[0][i] = "P|{2.1}|B|P|{2.2}"; n_regla[0][i] = "1"
        tabla[0][18] = "P|F|P|{3.1}"; n_regla[0][18] = "2"
        tabla[0][30] = "P|30|{4.1}";  n_regla[0][30] = "3"

        # B
        tabla[1][12] = "B|12|T|2|29|{5.1}"; n_regla[1][12]="4"
        tabla[1][20] = "B|20|23|E|24|{6.1}|S|{6.2}"; n_regla[1][20]="5"
        for i in [2, 16, 17, 19]:
            tabla[1][i] = "B|{7.1}|S|{7.2}"; n_regla[1][i]="6"
        tabla[1][21] = "B|21|{8.1}|25|C|26|22|23|E|24|29|{8.2}"; n_regla[1][21]="7"
        # T
        tabla[2][13] = "T|13|{9.1}"; n_regla[2][13]="8"
        tabla[2][14] = "T|14|{10.1}"; n_regla[2][14] = "9"
        tabla[2][15] = "T|15|{11.1}"; n_regla[2][15] = "10"
        # S
        tabla[3][2] = "S|2|S'|29|{12.1}"; n_regla[3][2]="11"
        tabla[3][19] = "S|{13.1}|19|X|29|{13.2}"; n_regla[3][19]="12"
        tabla[3][16] = "S|16|23|E|24|29|{14.1}"; n_regla[3][16]="13"
        tabla[3][17] = "S|17|23|2|24|29|{15.1}"; n_regla[3][17]="14"
        # S'
        tabla[4][11] = "S'|11|E|{16.1}"; n_regla[4][11]="15"
        tabla[4][23] = "S'|{17.1}|23|L|24|{17.2}"; n_regla[4][23]="16"
        # X
        for i in [0, 1, 2, 3, 4, 10, 23]:
            tabla[5][i] = "X|E|{18.1}"; n_regla[5][i]="17"
        tabla[5][29] = "X|{19.1}"; n_regla[5][29]="18"

        # C
        for i in [2, 12, 16, 17, 19, 20, 21]:
            tabla[6][i] = "C|{20.1}|B|C|{20.2}"; n_regla[6][i]="19"
        tabla[6][26] = "C|{21.1}"; n_regla[6][26]="20"

        # L
        for i in [0, 1, 2, 3, 4, 10, 23, 24]:
            tabla[7][i] = "L|E|Q|{22.1}"; n_regla[7][i]="21"
        tabla[7][24] = "L|{23.1}"; n_regla[7][24]="22"

        # Q
        tabla[8][28] = "Q|28|E|Q|{24.1}"; n_regla[8][28]="23"
        tabla[8][24] = "Q|{25.1}"; n_regla[8][24]="24"

        # F
        tabla[9][18] = "F|{26.1}|18|2|H|{26.2}|23|A|24|{26.3}|25|C|26|{26.4}"; n_regla[9][18]="25"
        # H
        for i in [13, 14, 15]:
            tabla[10][i] = "H|T|{27.1}"; n_regla[10][i]="26"
        tabla[10][23] = "H|{28.1}"; n_regla[10][23]="27"

        # A
        for i in [13, 14, 15]:
            tabla[11][i] = "A|T|2|{29.1}|K|{29.2}"; n_regla[11][i]="28"
        tabla[11][24] = "A|{30.1}"; n_regla[11][24]="29"

        # K
        tabla[12][28] = "K|28|T|2|{31.1}|K|{31.2}"; n_regla[12][28]="30"
        tabla[12][24] = "K|{32.1}"; n_regla[12][24]="31"

        # E
        for i in [0, 1, 2, 3, 4, 10, 23]:
            tabla[13][i] = "E|R|E'|{33.1}"; n_regla[13][i]="32"
        # E'
        tabla[14][9] = "E'|9|R|E'|{34.1}"; n_regla[14][9]="33"
        for i in [24, 28, 29]:
            tabla[14][i] = "E'|{35.1}"; n_regla[14][i]="34"
       # R
        for i in [0, 1, 2, 3, 4, 10, 23]:
            tabla[15][i] = "R|U|R'|{36.1}"; n_regla[15][i]="35"
        # R'
        tabla[16][8] = "R'|8|U|R'|{37.1}"; n_regla[16][8]="36"
        tabla[16][7] = "R'|7|U|R'|{38.1}"; n_regla[16][7]="37"
        for i in [9, 24, 28, 29]:
            tabla[16][i] = "R'|{39.1}"; n_regla[16][i]="38"
        # U
        for i in [0, 1, 2, 3, 4, 10, 23]:
            tabla[17][i] = "U|V|U'|{40.1}"; n_regla[17][i]="39"
        # U'
        tabla[18][5] = "U'|5|V|U'|{41.1}"; n_regla[18][5]="40"
        tabla[18][6] = "U'|6|V|U'|{42.1}"; n_regla[18][6]="41"
        for i in [7, 8, 9, 24, 28, 29]:
            tabla[18][i] = "U'|{43.1}"; n_regla[18][i]="42"
        # V
        tabla[19][2] = "V|2|V'|{44.1}"; n_regla[19][2]="43"
        tabla[19][10] = "V|10|2|{45.1}"; n_regla[19][10]="44"
        tabla[19][23] = "V|23|E|24|{46.1}"; n_regla[19][23]="45"
        tabla[19][0] = "V|0|{47.1}"; n_regla[19][0]="46"
        tabla[19][1] = "V|1|{48.1}"; n_regla[19][1]="47"
        tabla[19][3] = "V|3|{49.1}"; n_regla[19][3]="48"
        tabla[19][4] = "V|4|{50.1}"; n_regla[19][4]="49"

        # V'
        tabla[20][23] = "V'|{51.1}|23|L|24|{51.2}"; n_regla[20][23]="50"
        for i in [5, 6, 7, 8, 9, 24, 28, 29]:
            tabla[20][i] = "V'|{52.1}"; n_regla[20][i]="51"
        # FIN
        self.tabla = tabla

    # devuelve la fila de la matriz en la que esta un no terminal
    def buscaNoTerminal(self, noTerminal):
        for i in range(self.tradNoTerm.__len__()):
            if noTerminal == self.tradNoTerm[i]:
                return i
        return -1

    # devuelve la regla dentro de la matriz (noTerminal x token)
    def reglaEnTabla(self, noTerminal, token):
        if noTerminal[0] == '{':
            return -2

        indice_nt = self.buscaNoTerminal(noTerminal)

        if indice_nt == -1:
            self.genError(1)
            exit(1)

        if (regla := self.tabla[indice_nt][int(token)-1]) == "E":

            self.genError(1)
            exit(1)
        self.parse += self.n_regla[indice_nt][int(token)-1] + " "
        self.parseAux = self.n_regla[indice_nt][int(token)-1]
        return regla

    def printPila(self):
        print("pila[",end = "")
        for el in self.pila:
            print(f"{el},",end = "")
        print("]")

    def printpilaAUX(self):
        print("pilaAUX[", end="")
        for el in self.pilaAUX:
            print(f"{el},",end="")
        print("]")

    def aux(self):
        aux = self.pila.pop()

        ret = aux.getElem()
        if ret[0] == '{':
            print("",end = "")
        elif ret == str(int(self.token)-1):
            aux.setAtribToken(self.atrib)
            self.pilaAUX.append(aux)
        else:
            self.pilaAUX.append(aux)
        return ret

    # Analizador descendente tabular
    def tabular(self):

        while self.token != "FIN":
            if self.sacarNuevoToken:
                tokenC = self.anLex.analizador()

                if tokenC == "FIN":
                    self.token = "FIN"
                    break
                self.token = tokenC.split(",")[0].split("<")[1]
                self.atrib = tokenC.split(",")[1].split(">")[0]

            while (noTerminal := self.aux()) != str(int(self.token)-1):
                regla = self.reglaEnTabla(noTerminal, self.token)
                if regla == -2:
                    self.ejecAcSemantica(noTerminal)
                else:
                    if regla == "E":
                        self.genError(1)
                        exit(1)
                    partes_regla = regla.split("|")
                    for i2 in range(len(partes_regla)-1, 0, -1):
                        if partes_regla[i2] != "":
                            aux = tipoAUX(partes_regla[i2])
                            self.pila.append(aux)


                if len(self.pila) == 0:
                    self.token = "FIN"
                    break
        fT = open(f"salida{self.nombre_fich}/{self.nombre_fich}.TablaTS.txt", "a")
        fT.write(self.tablaSimbolosG.__str__())
        f = open(f"salida{self.nombre_fich}/{self.nombre_fich}.Parse.txt", "w")
        f.write(self.parse)
        self.ejec1_2()

        exit(0)

    def genError(self, codigo):
        nombre_token = self.tradTerm[int(self.token)-1]
        f = open(f"salida{self.nombre_fich}/{self.nombre_fich}.Parse.txt", "w")
        f.write(self.parse)
        ferr = open(f"salida{self.nombre_fich}/{self.nombre_fich}.Errores.txt", "a")
        ferr.write(f"Error Sintactico: Token no esperado: {nombre_token}. En linea:{self.anLex.nLinea} \n")
        #print(f"Error Sintáctico: Token no esperado: {nombre_token}. En linea:{self.anLex.nLinea} \n")

    def ejecAcSemantica(self,AcSem):
        match AcSem:
            case "{1.1}":
                self.ejec1_1()
            case "{1.2}":
                self.ejec1_2()
            case "{2.1}":
                self.ejec2_1()
            case "{2.2}":
                self.ejec2_2()
            case "{3.1}":
                self.ejec3_1()
            case "{4.1}":
                self.ejec4_1()
            case "{5.1}":
                self.ejec5_1()
            case "{6.1}":
                self.ejec6_1()
            case "{6.2}":
                self.ejec6_2()
            case "{7.1}":
                self.ejec7_1()
            case "{7.2}":
                self.ejec7_2()
            case "{8.1}":
                self.ejec8_1()
            case "{8.2}":
                self.ejec8_2()
            case "{9.1}":
                self.ejec9_1()
            case "{10.1}":
                self.ejec10_1()
            case "{11.1}":
                self.ejec11_1()
            case "{12.1}":
                self.ejec12_1()
            case "{13.1}":
                self.ejec13_1()
            case "{13.2}":
                self.ejec13_2()
            case "{14.1}":
                self.ejec14_1()
            case "{15.1}":
                self.ejec15_1()
            case "{16.1}":
                self.ejec16_1()
            case "{17.1}":
                self.ejec17_1()
            case "{17.2}":
                self.ejec17_2()
            case "{18.1}":
                self.ejec18_1()
            case "{19.1}":
                self.ejec19_1()
            case "{20.1}":
                self.ejec20_1()
            case "{20.2}":
                self.ejec20_2()
            case "{21.1}":
                self.ejec21_1()
            case "{22.1}":
                self.ejec22_1()
            case "{23.1}":
                self.ejec23_1()
            case "{24.1}":
                self.ejec24_1()
            case "{25.1}":
                self.ejec25_1()
            case "{26.1}":
                self.ejec26_1()
            case "{26.2}":
                self.ejec26_2()
            case "{26.3}":
                self.ejec26_3()
            case "{26.4}":
                self.ejec26_4()
            case "{27.1}":
                self.ejec27_1()
            case "{28.1}":
                self.ejec28_1()
            case "{29.1}":
                self.ejec29_1()
            case "{29.2}":
                self.ejec29_2()
            case "{30.1}":
                self.ejec30_1()
            case "{31.1}":
                self.ejec31_1()
            case "{31.2}":
                self.ejec31_2()
            case "{32.1}":
                self.ejec32_1()
            case "{33.1}":
                self.ejec33_1()
            case "{34.1}":
                self.ejec34_1()
            case "{35.1}":
                self.ejec35_1()
            case "{36.1}":
                self.ejec36_1()
            case "{37.1}":
                self.ejec37_1()
            case "{38.1}":
                self.ejec38_1()
            case "{39.1}":
                self.ejec39_1()
            case "{40.1}":
                self.ejec40_1()
            case "{41.1}":
                self.ejec41_1()
            case "{42.1}":
                self.ejec42_1()
            case "{43.1}":
                self.ejec43_1()
            case "{44.1}":
                self.ejec44_1()
            case "{45.1}":
                self.ejec45_1()
            case "{46.1}":
                self.ejec46_1()
            case "{47.1}":
                self.ejec47_1()
            case "{48.1}":
                self.ejec48_1()
            case "{49.1}":
                self.ejec49_1()
            case "{50.1}":
                self.ejec50_1()
            case "{51.1}":
                self.ejec51_1()
            case "{51.2}":
                self.ejec51_2()
            case "{52.1}":
                self.ejec52_1()
            case _:
                print(f"algo se te ha olvidado: {AcSem}")


    def poppilaAUX(self,num_pops):
        for i in range(num_pops):
            self.pilaAUX.pop()

    def ejec1_1(self):
        self.tablaActual = 0
        self.anLex.cambiarActual(0)
        self.zonaReturn = False
        self.despG = 0
        self.despL = 0

    def ejec1_2(self):
        self.poppilaAUX(1)

    def ejec2_1(self):
        B = self.pila[len(self.pila)-1]
        B.anadirAtrib("tipo_error")


    def ejec2_2(self):
        self.poppilaAUX(2)

    def ejec3_1(self):
        self.poppilaAUX(2)

    def ejec4_1(self):
        self.poppilaAUX(1)

    def ejec5_1(self):
        posTS = int(self.pilaAUX[len(self.pilaAUX) - 2].getAtribToken())
        T = self.pilaAUX[len(self.pilaAUX) - 3]
        tipo = T.getAtrib("tipo")
        if self.tablaActual == 0:
            if self.tablaSimbolosG.getTipo(posTS) != "noDeclarado":
                lex = self.tablaSimbolosG.getLexema(posTS)
                self.errorSem("",15,lex,0)
            else:
                self.tablaSimbolosG.anadirTipoTS(posTS,tipo,self.despG)
                self.despG += T.getAtrib("ancho")
        else:
            if self.tablaSimbolosL.getTipo(posTS) != "noDeclarado":
                lex = self.tablaSimbolosL.getLexema(posTS)
                self.errorSem("",15,lex,1)
            else:
                self.tablaSimbolosL.anadirTipoTS(posTS, tipo, self.despL)
                self.despL += T.getAtrib("ancho")
        self.poppilaAUX(4)

    def ejec6_1(self):
        if self.zonaReturn:
            B = self.pilaAUX[len(self.pilaAUX) - 5]
            S = self.pila[len(self.pila)-1]
            S.anadirAtrib(B.getAtrib("tipo"))


    def ejec6_2(self):
        E = self.pilaAUX[len(self.pilaAUX)-3]
        tipo = E.getAtrib("tipo")
        if tipo != "boolean":
            self.errorSem("6_1",1,tipo,None)

        self.poppilaAUX(5)

    def ejec7_1(self):
        if self.zonaReturn: # si esta dentro de funcion, hereda tipo de B a S
            S = self.pila[len(self.pila)-1]
            B = self.pilaAUX[len(self.pilaAUX)-1]
            S.anadirAtrib(B.getAtrib("tipo"))


    def ejec7_2(self):
        self.poppilaAUX(1)

    def ejec8_1(self):
        if self.zonaReturn:
            C = self.pila[len(self.pila)-2]
            B = self.pilaAUX[len(self.pilaAUX)-2]
            C.anadirAtrib(B.getAtrib("tipo"))

    def ejec8_2(self):
        E = self.pilaAUX[len(self.pilaAUX) - 3]
        tipo = E.getAtrib("tipo")
        if tipo != "boolean":
            self.errorSem("8_1",2,tipo,None)
        self.poppilaAUX(9)

    def ejec9_1(self):
        T = self.pilaAUX[len(self.pilaAUX) - 2]
        T.anadirAtrib("int")
        T.anadirAtrib(2)

        self.poppilaAUX(1)

    def ejec10_1(self):
        T = self.pilaAUX[len(self.pilaAUX) - 2]
        T.anadirAtrib("string")
        T.anadirAtrib(0)
        self.poppilaAUX(1)

    def ejec11_1(self):
        T = self.pilaAUX[len(self.pilaAUX) - 2]
        T.anadirAtrib("boolean")
        T.anadirAtrib(2)
        self.poppilaAUX(1)

    def ejec12_1(self):
        id_ = self.pilaAUX[len(self.pilaAUX) - 3]
        S1 = self.pilaAUX[len(self.pilaAUX) - 2]
        idTipo = ""
        posTS = int(id_.getAtribToken())
        tablaVar = int(id_.getTabla())
        if self.tablaActual == 0:  # TSGlobal
            idTipo = self.tablaSimbolosG.getTipo(id_.getAtribToken())
            if idTipo == "noDeclarado":  # variable no declarada --> global entera
                idTipo = "int"
                self.tablaSimbolosG.anadirTipoTS(posTS, "int", self.despG)
                self.despG += 2
        elif self.tablaActual == 1 and tablaVar == 0:  # variable global declarada
            idTipo = self.tablaSimbolosG.getTipo(id_.getAtribToken())
        else:  # TSLocalF
            if self.tablaSimbolosL.getTipo(id_.getAtribToken()) == "noDeclarado":
                # variable no declarada --> global entera
                lexema = self.tablaSimbolosL.getLexema(id_.getAtribToken())
                if lexema in self.tablaSimbolosG.tabla.keys():
                    atributos = self.tablaSimbolosG.tabla.get(lexema)
                    indice = atributos.indice
                    id_.reDefAtribTokenID(indice, 0)
                    self.tablaSimbolosL.tabla.get(lexema).contador -= 1
                    if self.tablaSimbolosL.tabla.get(lexema).contador == 0:
                        self.tablaSimbolosL.eliminarFila(lexema)
                    idTipo = atributos.tipo
                else:
                    atributos = atributosTS("int", self.despG, None, None, None, None, None, None)
                    lexema = self.tablaSimbolosL.getLexema(id_.getAtribToken())
                    self.tablaSimbolosG.insertarFila(lexema, atributos)
                    self.tablaSimbolosL.eliminarFila(lexema)
                    self.tablaSimbolosG.tabla.get(lexema).desplazamiento = self.despG
                    idTipo = "int"
                    self.despG += 2
            else:  # variable local
                idTipo = self.tablaSimbolosL.getTipo(id_.getAtribToken())
        if idTipo != S1.getAtrib("tipo"):
            self.errorSem("12_1 - 1",14,idTipo,S1.getAtrib("tipo"))
        else:
            if idTipo == "function" and self.tablaSimbolosG.getParametros(id_.getAtribToken()) != S1.getAtrib("argumentos"):
                self.errorSem("12_1 - 2",3,self.tablaSimbolosG.getParametros(id_.getAtribToken()),S1.getAtrib("argumentos"))

        self.poppilaAUX(3)

    def ejec13_1(self):
        if not self.zonaReturn:
            S = self.pilaAUX[len(self.pilaAUX) - 1]
            S.anadirAtrib("tipo_error")
            self.errorSem("13_1",4,None,None)
        print("",end="")

    def ejec13_2(self):
        S = self.pilaAUX[len(self.pilaAUX) - 4]
        X = self.pilaAUX[len(self.pilaAUX) - 2]

        if S.getAtrib("tipo") != X.getAtrib("tipo"):
            self.errorSem("13_2",5,S.getAtrib("tipo"),X.getAtrib("tipo"))
        self.poppilaAUX(3)

    def ejec14_1(self):
        E = self.pilaAUX[len(self.pilaAUX) - 3]
        if E.getAtrib("tipo") != "string" and E.getAtrib("tipo") != "int":
            self.errorSem("14_1",6,E.getAtrib("tipo"),None)
        self.poppilaAUX(5)

    def ejec15_1(self):
        id_ = self.pilaAUX[len(self.pilaAUX) - 3]
        posTS = int(id_.getAtribToken())
        tablaVar = int(id_.getTabla())

        if self.tablaActual == 0:  # TSGlobal
            idTipo = self.tablaSimbolosG.getTipo(posTS)
            if idTipo == "noDeclarado":  # variable no declarada --> global entera
                idTipo = "int"
                self.tablaSimbolosG.anadirTipoTS(posTS, "int", self.despG)
                self.despG += 2
        elif self.tablaActual == 1 and tablaVar == 0:  # variable global declarada
            idTipo = self.tablaSimbolosG.getTipo(id_.getAtribToken())
        else:  # TSLocal
            if self.tablaSimbolosL.getTipo(id_.getAtribToken()) == "noDeclarado":
                # variable no declarada --> global entera
                lexema = self.tablaSimbolosL.getLexema(id_.getAtribToken())
                if lexema in self.tablaSimbolosG.tabla.keys():
                    atributos = self.tablaSimbolosG.tabla.get(lexema)
                    indice = atributos.indice
                    id_.reDefAtribTokenID(indice, 0)
                    self.tablaSimbolosL.tabla.get(lexema).contador -= 1
                    if self.tablaSimbolosL.tabla.get(lexema).contador == 0:
                        self.tablaSimbolosL.eliminarFila(lexema)
                    idTipo = atributos.tipo
                else:
                    atributos = atributosTS("int", self.despG, None, None, None, None, None, None)
                    self.despG += 2
                    lexema = self.tablaSimbolosL.getLexema(id_.getAtribToken())
                    self.tablaSimbolosG.insertarFila(lexema, atributos)
                    self.tablaSimbolosL.eliminarFila(lexema)
                    idTipo = "int"
            else:  # variable local
                idTipo = self.tablaSimbolosL.getTipo(id_.getAtribToken())

        if idTipo != "string" and idTipo != "int":
            self.errorSem("15_1 - 1",7,idTipo,None)
        self.poppilaAUX(5)

    def ejec16_1(self):
        S1 = self.pilaAUX[len(self.pilaAUX) - 3]
        E = self.pilaAUX[len(self.pilaAUX) - 1]
        S1.anadirAtrib(E.getAtrib("tipo"))
        self.poppilaAUX(2)

    def ejec17_1(self):
        print("",end="")

    def ejec17_2(self):
        S1 = self.pilaAUX[len(self.pilaAUX) - 4]
        L = self.pilaAUX[len(self.pilaAUX) - 2]

        S1.anadirAtrib("function")
        S1.anadirAtrib(0)
        S1.anadirAtrib(L.getAtrib("tipo"))
        self.poppilaAUX(3)

    def ejec18_1(self):
        X = self.pilaAUX[len(self.pilaAUX) - 2]
        E = self.pilaAUX[len(self.pilaAUX) - 1]
        X.anadirAtrib(E.getAtrib("tipo"))
        self.poppilaAUX(1)

    def ejec19_1(self):  # lambda
        X = self.pilaAUX[len(self.pilaAUX) - 1]
        X.anadirAtrib("tipoVacio")

    def ejec20_1(self):
        if self.zonaReturn:
            B = self.pila[len(self.pila)-1]
            C = self.pilaAUX[len(self.pilaAUX)-1]
            C2 = self.pila[len(self.pila)-2]
            C2.anadirAtrib(C.getAtrib("tipo"))
            B.anadirAtrib(C.getAtrib("tipo"))

    def ejec20_2(self):
        self.poppilaAUX(2)

    def ejec21_1(self):  # lambda
        C = self.pilaAUX[len(self.pilaAUX) - 1]
        C.anadirAtrib("tipoVacio")


    def ejec22_1(self):
        L = self.pilaAUX[len(self.pilaAUX) - 3]
        E = self.pilaAUX[len(self.pilaAUX) - 2]
        Q = self.pilaAUX[len(self.pilaAUX) - 1]
        if Q.getAtrib("tipo") != "tipoVacio":
            L.anadirAtrib(E.getAtrib("tipo") + " " + Q.getAtrib("tipo"))
        else:
            L.anadirAtrib(E.getAtrib("tipo"))
        self.poppilaAUX(2)

    def ejec23_1(self):   # lambda
        L = self.pilaAUX[len(self.pilaAUX) - 1]
        L.anadirAtrib("tipoVacio")


    def ejec24_1(self):
        Q1 = self.pilaAUX[len(self.pilaAUX) - 4]
        E = self.pilaAUX[len(self.pilaAUX) - 2]
        Q2 = self.pilaAUX[len(self.pilaAUX) - 1]
        if Q2.getAtrib("tipo") != "tipoVacio":
            Q1.anadirAtrib(E.getAtrib("tipo") + " " + Q2.getAtrib("tipo"))
        else:
            Q1.anadirAtrib(E.getAtrib("tipo"))
        self.poppilaAUX(3)

    def ejec25_1(self): # lambda
        Q = self.pilaAUX[len(self.pilaAUX)-1]
        Q.anadirAtrib("tipoVacio")

    def ejec26_1(self):
        self.zonaReturn=True


    def ejec26_2(self):
        H = self.pilaAUX[len(self.pilaAUX) - 1]
        id_ = self.pilaAUX[len(self.pilaAUX) - 2]
        posTS = int(id_.getAtribToken())
        self.tablaSimbolosG.anadirTipoTS(posTS, "function", self.despG)
        self.tablaSimbolosG.anadirTipoDevuelto(posTS,H.getAtrib("tipo"))
        self.tablaActual = 1
        self.anLex.cambiarActual(1)
        self.despL = 0


    def ejec26_3(self):
        id_= self.pilaAUX[len(self.pilaAUX) - 5]
        A = self.pilaAUX[len(self.pilaAUX) - 2]
        C = self.pila[len(self.pila) - 2]
        H = self.pilaAUX[len(self.pilaAUX) - 4]
        C.anadirAtrib(H.getAtrib("tipo"))
        posTS = int(id_.getAtribToken())
        self.tablaSimbolosG.anadirParametros(posTS,A.getAtrib("tipo"))


    def ejec26_4(self):
        fT = open(f"salida{self.nombre_fich}/{self.nombre_fich}.TablaTS.txt", "a")
        fT.write(self.tablaSimbolosL.__str__())
        self.tablaActual = 0
        self.anLex.cambiarActual(0)
        self.zonaReturn=False
        self.tablaSimbolosL.limpiarTS()
        self.tablaSimbolosL.num += 1
        self.poppilaAUX(9)

    def ejec27_1(self):
        H = self.pilaAUX[len(self.pilaAUX) - 2]
        T = self.pilaAUX[len(self.pilaAUX) - 1]
        H.anadirAtrib(T.getAtrib("tipo"))
        self.poppilaAUX(1)

    def ejec28_1(self): # lambda
        H = self.pilaAUX[len(self.pilaAUX) - 1]
        H.anadirAtrib("tipoVacio")


    def ejec29_1(self): # anadir_TS(id.posTS, T.tipo, DespAct); DespAct += T.ancho;
        posTS = int(self.pilaAUX[len(self.pilaAUX) - 1].getAtribToken())
        T = self.pilaAUX[len(self.pilaAUX) - 2]
        tipo = T.getAtrib("tipo")
        if self.tablaActual == 0:    #Tabla_Actual = Global
            self.tablaSimbolosG.anadirTipoTS(posTS, tipo, self.despG)
            self.despG += T.getAtrib("ancho")
        else:                        #Tabla_Actual = Local
            self.tablaSimbolosL.anadirTipoTS(posTS, tipo, self.despL)
            self.despL += T.getAtrib("ancho")


    def ejec29_2(self):
        A = self.pilaAUX[len(self.pilaAUX) - 4]
        T = self.pilaAUX[len(self.pilaAUX) - 3]
        K = self.pilaAUX[len(self.pilaAUX) - 1]
        if K.getAtrib("tipo") != "tipoVacio":
            A.anadirAtrib(T.getAtrib("tipo") + " " + K.getAtrib("tipo"))
        else:
            A.anadirAtrib(T.getAtrib("tipo"))
        self.poppilaAUX(3)

    def ejec30_1(self): # lambda
        A = self.pilaAUX[len(self.pilaAUX)-1]
        A.anadirAtrib("tipoVacio")

    def ejec31_1(self): # anadir_TS(id.posTS, T.tipo, DespAct); DespAct += T.ancho;
        posTS = int(self.pilaAUX[len(self.pilaAUX) - 1].getAtribToken())
        T = self.pilaAUX[len(self.pilaAUX) - 2]
        tipo = T.getAtrib("tipo")
        if self.tablaActual == 0:    #Tabla_Actual = Global
            self.tablaSimbolosG.anadirTipoTS(posTS, tipo, self.despG)
            self.despG += T.getAtrib("ancho")
        else:                        #Tabla_Actual = Local
            self.tablaSimbolosL.anadirTipoTS(posTS, tipo, self.despL)
            self.despL += T.getAtrib("ancho")


    def ejec31_2(self):
        K1 = self.pilaAUX[len(self.pilaAUX) - 5]
        T = self.pilaAUX[len(self.pilaAUX) - 3]
        K2 = self.pilaAUX[len(self.pilaAUX) - 1]
        if K2.getAtrib("tipo") != "tipoVacio":
            K1.anadirAtrib(T.getAtrib("tipo") + " " +K2.getAtrib("tipo"))
        else:
            K1.anadirAtrib(T.getAtrib("tipo"))
        self.poppilaAUX(4)

    def ejec32_1(self): # lambda
        K = self.pilaAUX[len(self.pilaAUX)-1]
        K.anadirAtrib("tipoVacio")

    def ejec33_1(self):
        E = self.pilaAUX[len(self.pilaAUX) - 3]
        E1 = self.pilaAUX[len(self.pilaAUX)- 1]
        R = self.pilaAUX[len(self.pilaAUX) - 2]
        if E1.getAtrib("tipo") != "tipoVacio":
           if R.getAtrib("tipo") != "boolean":
                E.anadirAtrib("tipo_error")
                self.errorSem("33_1 - 1",8,R.getAtrib("tipo"),None)
           else:
                 E.anadirAtrib("boolean")
        else:
            E.anadirAtrib(R.getAtrib("tipo"))
        self.poppilaAUX(2)

    def ejec34_1(self):
        E1_1 = self.pilaAUX[len(self.pilaAUX)-4]
        R = self.pilaAUX[len(self.pilaAUX)-2]
        E1_2 = self.pilaAUX[len(self.pilaAUX)-1]
        if R.getAtrib("tipo") != "boolean":
            E1_1.anadirAtrib("tipo_error")
            self.errorSem("34_1 - 1",8,R.getAtrib("tipo"),None)
        elif E1_2.getAtrib("tipo") != "boolean" and E1_2.getAtrib("tipo") != "tipoVacio":
            E1_1.anadirAtrib("tipo_error")
            self.errorSem("34_1 - 2",8,E1_2.getAtrib("tipo"),None)
        else:
            E1_1.anadirAtrib("boolean")

        self.poppilaAUX(3)

    def ejec35_1(self): # lambda
        E1 = self.pilaAUX[len(self.pilaAUX)-1]
        E1.anadirAtrib("tipoVacio")

    def ejec36_1(self):
        U = self.pilaAUX[len(self.pilaAUX)  - 2]
        R1 = self.pilaAUX[len(self.pilaAUX) - 1]
        R = self.pilaAUX[len(self.pilaAUX)  - 3]
        if R1.getAtrib("tipo") == "tipoVacio":
            R.anadirAtrib(U.getAtrib("tipo"))
        elif U.getAtrib("tipo") != "int":
            R.anadirAtrib("tipo_error")
            self.errorSem("36_1 - 1",9,U.getAtrib("tipo"),None)
        else:
            R.anadirAtrib("boolean")
        self.poppilaAUX(2)

    def ejec37_1(self):
        R1_1 = self.pilaAUX[len(self.pilaAUX)-4]
        U = self.pilaAUX[len(self.pilaAUX)-2]
        if U.getAtrib("tipo") != "int":
            R1_1.anadirAtrib("tipo_error")
            self.errorSem("37_1 - 1",9,U.getAtrib("tipo"),None)
        else:
            R1_1.anadirAtrib("boolean")
        self.poppilaAUX(3)

    def ejec38_1(self):
        R1_1 = self.pilaAUX[len(self.pilaAUX)-4]
        U = self.pilaAUX[len(self.pilaAUX)-2]
        if U.getAtrib("tipo") != "int":
            R1_1.anadirAtrib("tipo_error")
            self.errorSem("38_1 - 1",10,U.getAtrib("tipo"),None)
        else:
            R1_1.anadirAtrib("boolean")
        self.poppilaAUX(3)

    def ejec39_1(self): #  lambda
        R1 = self.pilaAUX[len(self.pilaAUX)-1]
        R1.anadirAtrib("tipoVacio")

    def ejec40_1(self):
        U1 = self.pilaAUX[len(self.pilaAUX) - 1]
        V = self.pilaAUX[len(self.pilaAUX) - 2]
        U = self.pilaAUX[len(self.pilaAUX) - 3]

        if U1.getAtrib("tipo") == "tipoVacio":
            U.anadirAtrib(V.getAtrib("tipo"))
        elif V.getAtrib("tipo") != "int":
            U.anadirAtrib("tipo_error")
            self.errorSem("40_1",11,V.getAtrib("tipo"),None)
        else:
            U.anadirAtrib("int")

        self.poppilaAUX(2)

    def ejec41_1(self):
        U1_1 = self.pilaAUX[len(self.pilaAUX) - 4]
        V = self.pilaAUX[len(self.pilaAUX) - 2]
        if V.getAtrib("tipo") != "int":
            U1_1.anadirAtrib("tipo_error")
            self.errorSem("41_1",11,V.getAtrib("tipo"),None)
        else:
            U1_1.anadirAtrib("int")

        self.poppilaAUX(3)

    def ejec42_1(self):
        U1_1 = self.pilaAUX[len(self.pilaAUX) - 4]
        V = self.pilaAUX[len(self.pilaAUX) - 2]
        if V.getAtrib("tipo") != "int":
            U1_1.anadirAtrib("tipo_error")
            self.errorSem("41_1",12,V.getAtrib("tipo"),None)
        else:
            U1_1.anadirAtrib("int")

        self.poppilaAUX(3)

    def ejec43_1(self):
        U1 = self.pilaAUX[len(self.pilaAUX)-1]
        U1.anadirAtrib("tipoVacio")

    def ejec44_1(self):
        V = self.pilaAUX[len(self.pilaAUX) - 3]
        id_ = self.pilaAUX[len(self.pilaAUX) - 2]
        V1 = self.pilaAUX[len(self.pilaAUX) - 1]
        posTS = int(id_.getAtribToken())
        tablaVar = int(id_.getTabla())
        if self.tablaActual == 0:  # TSGlobal
            idTipo = self.tablaSimbolosG.getTipo(id_.getAtribToken())
            if idTipo == "noDeclarado":  # variable no declarada --> global entera
                idTipo = "int"
                self.tablaSimbolosG.anadirTipoTS(posTS, "int", self.despG)
                self.despG += 2
        elif self.tablaActual == 1 and tablaVar == 0:  # variable global declarada
            idTipo = self.tablaSimbolosG.getTipo(id_.getAtribToken())
        else:  # TSLocal
            if self.tablaSimbolosL.getTipo(id_.getAtribToken()) == "noDeclarado":
                # variable no declarada --> global entera
                lexema = self.tablaSimbolosL.getLexema(id_.getAtribToken())
                if lexema in self.tablaSimbolosG.tabla.keys():
                    atributos = self.tablaSimbolosG.tabla.get(lexema)
                    indice = atributos.indice
                    id_.reDefAtribTokenID(indice,0)
                    self.tablaSimbolosL.tabla.get(lexema).contador -= 1
                    if self.tablaSimbolosL.tabla.get(lexema).contador==0:
                        self.tablaSimbolosL.eliminarFila(lexema)
                    idTipo = atributos.tipo
                else:
                    atributos = atributosTS("int", self.despG, None, None, None, None, None, None)
                    self.despG += 2
                    lexema = self.tablaSimbolosL.getLexema(id_.getAtribToken())
                    self.tablaSimbolosG.insertarFila(lexema, atributos)
                    self.tablaSimbolosL.eliminarFila(lexema)
                    idTipo = "int"
            else:  # variable local
                idTipo = self.tablaSimbolosL.getTipo(id_.getAtribToken())


        if idTipo == "function" and self.tablaSimbolosG.getParametros(id_.getAtribToken()) != V1.getAtrib("argumentos"):
            V.anadirAtrib(self.tablaSimbolosG.getTipoDevuelto(id_.getAtribToken()))
            self.errorSem("12_1 - 2", 3, self.tablaSimbolosG.getParametros(id_.getAtribToken()),
                          V1.getAtrib("argumentos"))
        elif idTipo == "function":
            V.anadirAtrib(self.tablaSimbolosG.getTipoDevuelto(id_.getAtribToken()))
        if idTipo != "function":
            V.anadirAtrib(idTipo)
        self.poppilaAUX(2)

    def ejec45_1(self):
        id_ = self.pilaAUX[len(self.pilaAUX) - 1]
        posTS = int(id_.getAtribToken())
        tablaVar = int(id_.getTabla())
        if self.tablaActual == 0:  # TSGlobal
            idTipo = self.tablaSimbolosG.getTipo(id_.getAtribToken())
            if idTipo == "noDeclarado":  # variable no declarada --> global entera
                idTipo = "int"
                self.tablaSimbolosG.anadirTipoTS(posTS, "int", self.despG)
                self.despG += 2
        elif self.tablaActual == 1 and tablaVar == 0:  # variable global declarada
            idTipo = self.tablaSimbolosG.getTipo(id_.getAtribToken())
        else:  # TSLocal
            if self.tablaSimbolosL.getTipo(id_.getAtribToken()) == "noDeclarado":
                # variable no declarada --> global entera
                lexema = self.tablaSimbolosL.getLexema(id_.getAtribToken())
                if lexema in self.tablaSimbolosG.tabla.keys():
                    atributos = self.tablaSimbolosG.tabla.get(lexema)
                    indice = atributos.indice
                    id_.reDefAtribTokenID(indice, 0)
                    self.tablaSimbolosL.tabla.get(lexema).contador -= 1
                    if self.tablaSimbolosL.tabla.get(lexema).contador == 0:
                        self.tablaSimbolosL.eliminarFila(lexema)
                    idTipo = atributos.tipo
                else:
                    atributos = atributosTS("int", self.despG, None, None, None, None, None, None)
                    self.despG += 2
                    lexema = self.tablaSimbolosL.getLexema(id_.getAtribToken())
                    self.tablaSimbolosG.insertarFila(lexema, atributos)
                    self.tablaSimbolosL.eliminarFila(lexema)
                    idTipo = "int"
            else:  # variable local
                idTipo = self.tablaSimbolosL.getTipo(id_.getAtribToken())


        if idTipo != "int":
            V = self.pilaAUX[len(self.pilaAUX) - 3]
            V.anadirAtrib("tipo_error")
            lexema = self.tablaSimbolosG.getLexema(id_.getAtribToken())
            self.errorSem("45_1 - 3",13,idTipo,lexema)
        else:
            V = self.pilaAUX[len(self.pilaAUX) - 3]
            V.anadirAtrib(idTipo)

        self.poppilaAUX(2)

    def ejec46_1(self):
        V = self.pilaAUX[len(self.pilaAUX) - 4]
        E = self.pilaAUX[len(self.pilaAUX) - 2]
        V.anadirAtrib(E.getAtrib("tipo"))
        self.poppilaAUX(3)

    def ejec47_1(self):
        V = self.pilaAUX[len(self.pilaAUX) - 2]
        V.anadirAtrib("int")
        self.poppilaAUX(1)

    def ejec48_1(self):
        V = self.pilaAUX[len(self.pilaAUX) - 2]
        V.anadirAtrib("string")
        cadena = self.pilaAUX[len(self.pilaAUX) - 1]
        V.anadirAtrib(len(cadena.getAtribToken())-2)
        self.poppilaAUX(1)

    def ejec49_1(self):
        V = self.pilaAUX[len(self.pilaAUX) - 2]
        V.anadirAtrib("boolean")
        self.poppilaAUX(1)

    def ejec50_1(self):
        V = self.pilaAUX[len(self.pilaAUX) - 2]
        V.anadirAtrib("boolean")
        self.poppilaAUX(1)

    def ejec51_1(self):
        print("", end="")

    def ejec51_2(self):
       V1 = self.pilaAUX[len(self.pilaAUX) - 4]
       L =  self.pilaAUX[len(self.pilaAUX) - 2]
       V1.anadirAtrib("function")
       V1.anadirAtrib(0)
       V1.anadirAtrib(L.getAtrib("tipo"))
       self.poppilaAUX(3)

    def ejec52_1(self):
        V1 = self.pilaAUX[len(self.pilaAUX) - 1]
        V1.anadirAtrib("tipoVacio")

    def errorSem(self, error, codigoErr, parametroErr1, parametroErr2):
        '''
        fT = open(f"salida{self.nombre_fich}/{self.nombre_fich}.TablaTS.txt", "a")
        fT.write(self.tablaSimbolosG.__str__())
        f = open(f"salida{self.nombre_fich}/{self.nombre_fich}.Parse.txt", "w")
        f.write(self.parse)
        print(self.parse)
        '''
        men_err = f"Error semantico en linea: {self.anLex.nLinea} \n"
        match codigoErr:
            case 1:
                men_err += "     -Error en el condicional de la sentencia if, se espera un tipo boolean"
            case 2:
                men_err += "     -Error en el condicional de la sentencia while, se espera un tipo boolean"
            case 3:
                men_err += f"    -Error al llamar a la funcion:, la lista de parametros de la funcion no concuerda con la establecida. Esperada =  {parametroErr1}, Obtenido =  {parametroErr2}"
            case 4:
                men_err += f"    -Error detectado return fuera de una función"
            case 5:
                if parametroErr1 != "tipo_error":
                    men_err += f"    -Error tipo devuelto por el return incorrecto. Esperado: {parametroErr1}, Obtenido: {parametroErr2}"
                else:
                    men_err = ""
            case 6:
                men_err += f"    -Error tipo de parametros del print. Se esperaba un String o int. Recibido : {parametroErr1}"
            case 7:
                men_err += f"    -Error tipo de parametros del input. Se esperaba un String o int. Recibido : {parametroErr1}"
            case 8:
                men_err += f"    -Error en el tipo al usar &&. Se esperaba un Boolean. Recibido: {parametroErr1}"
            case 9:
                men_err += f"    -Error en el tipo al usar <. Se esperaba un int. Recibido: {parametroErr1}"
            case 10:
                men_err += f"    -Error en el tipo al usar ==. Se esperaba un int. Recibido: {parametroErr1}"
            case 11:
                men_err += f"    -Error en el tipo al usar +. Se esperaba un int. Recibido: {parametroErr1}"
            case 12:
                men_err += f"    -Error en el tipo al usar *. Se esperaba un int. Recibido: {parametroErr1}"
            case 13:
                men_err += f"    -Error en el tipo de la variable: {parametroErr2} al usar --. Se esperaba un int. Recibido: {parametroErr1}"
            case 14:
                if parametroErr1 == "function":
                    men_err+= f" Intentando igualar una funcion a un {parametroErr2}"
                elif parametroErr2 == "function":
                    men_err+= f" Intentado llamar a una variable como si fuera una funcion"
                else:
                    if parametroErr1 != "tipo_error" and parametroErr2 != "tipo_error":
                        men_err+= f" Los tipos de las variables no coinciden. Esperaba un {parametroErr1}. Recibido {parametroErr2}"
                    else:
                        men_err = ""
            case 15:
                if int(parametroErr2) == 0:
                    ambito = "Global"
                else:
                    ambito = "Local"
                men_err += f"    -Error al declarar la variable: {parametroErr1}, ya esta declarada en el ambito: {ambito}"
        if men_err != "":
            ferr = open(f"salida{self.nombre_fich}/{self.nombre_fich}.Errores.txt", "a")
            ferr.write(men_err)
            ferr.write("\n")
            #print(men_err)
        #exit(1)