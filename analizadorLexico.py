from os import remove, mkdir
from tablaSimbolos import atributosTS

class analizador_lexico:



    def __init__(self, nombre_fich, tablaSimbolosG, tablaSimbolosL):
        self.nLinea = 1
        self.tabla = None
        self.nombre_fich = nombre_fich
        try:
            mkdir(f"salida{self.nombre_fich}")
        except FileExistsError:
            print("", end="")
        try:
            remove(f"salida{self.nombre_fich}/{self.nombre_fich}.Tokens.txt")
        except FileNotFoundError:
            print("", end="")
        #self.genArcToken()
        try:
            remove(f"salida{self.nombre_fich}/{self.nombre_fich}.Errores.txt")
        except FileNotFoundError:
            print("", end="")
        try:
            remove(f"salida{self.nombre_fich}/{self.nombre_fich}.TablaTS.txt")
        except FileNotFoundError:
            print("", end="")
        self.ftoken = open(f"salida{self.nombre_fich}/{self.nombre_fich}.Tokens.txt", "a")
        self.f = open(self.nombre_fich, "r")
        self.tablaG = tablaSimbolosG
        self.tablaL = tablaSimbolosL
        self.actual = 0
        self.char_valido = False
        self.leido = True
        self.token = ""
       # self.analizador()
        
    def cambiarActual(self, actual):
        self.actual = actual

        
    def genToken(self, codigo, atrib):
        ftoken = open(f"salida{self.nombre_fich}/{self.nombre_fich}.Tokens.txt", "a")
        if codigo != 3:
            ftoken.write(f" <{codigo},{atrib}> \n")
            self.token = f" <{codigo},{atrib}> \n"
            return f" <{codigo},{atrib}> \n"
        else:
            match atrib:
                case "true":
                    return self.genToken(4, "")
                case "false":
                    return self.genToken(5, "")
                case "let":
                    return self.genToken(13, "")
                case "int":
                    return self.genToken(14, "")
                case "string":
                    return self.genToken(15, "")
                case "boolean":
                    return self.genToken(16, "")
                case "print":
                    return self.genToken(17, "")
                case "input":
                    return self.genToken(18, "")
                case "function":
                    return self.genToken(19, "")
                case "return":
                    return self.genToken(20, "")
                case "if":
                    return self.genToken(21, "")
                case "do":
                    return self.genToken(22, "")
                case "while":
                    return self.genToken(23, "")
                case _:
                    fila = atributosTS("noDeclarado", 0, None, None, None, None, None, None)
                    if self.actual == 1:
                        pos_ts = self.tablaL.insertarFila(atrib, fila)
                        ftoken.write(f" <{codigo},{pos_ts}> \n")
                        self.token = f" <{codigo},{pos_ts}-1> \n"
                        return f" <{codigo},{pos_ts}-1> \n"
                    elif self.actual == 0:  # TSGlobal
                        pos_ts = self.tablaG.insertarFila(atrib, fila)
                        ftoken.write(f" <{codigo},{pos_ts}> \n")
                        self.token = f" <{codigo},{pos_ts}-0> \n"
                        return f" <{codigo},{pos_ts}-0> \n"



    def genError(self, codigo):
        ferr = open(f"salida{self.nombre_fich}/{self.nombre_fich}.Errores.txt", "a")
        match codigo:
            case 1:
                ferr.write(f"Error Lexico en la linea {self.nLinea}: Caracter no esperado \n")
            case 2:
                ferr.write(f"Error Lexico en la linea {self.nLinea}: Numero mayor que 2^16 \n")
            case 3:
                ferr.write(f"Error Lexico en la linea {self.nLinea}: Caracter no imprimible \n")
            case 4:
                ferr.write(f"Error Lexico en la linea {self.nLinea}: Cadena con mas de 64 caracteres \n")
            case 5:
                ferr.write(f"Error Lexico en la linea {self.nLinea}: Caracter no esperado, se espera un - \n")
            case 6:
                ferr.write(f"Error Lexico en la linea {self.nLinea}: Caracter no esperado, se espera un & \n")
            case 7:
                ferr.write(f"Error Lexico en la linea {self.nLinea}: Caracter no esperado, se espera un * \n")
            case 8:
                ferr.write(f"Error Lexico en la linea {self.nLinea}: No se han cerrado las comillas \n")


    def leerComentario(self, f2):
        c2 = f2.read(1)
        while c2 != '*':
            c2 = f2.read(1)
            if c2 == '\n':
                self.nLinea += 1
        c2 = f2.read(1)
        while c2 == '*':
            c2 = f2.read(1)
        if c2 == '/':
            return
        else:
            self.leerComentario(f2)
        return

    def leerNumero(self, f2, c2):
        num = int(c2)
        c2 = f2.read(1)
        while '0' <= c2 <= '9':
            num = num * 10 + int(c2)
            c2 = f2.read(1)
        if num < 2 ** 15:
            self.genToken(1, num)
        else:
            self.genToken(1,0)
            self.genError(2)  # error numero muy grande
        return c2

    def leerCadena(self, f2):
        c2 = f2.read(1)
        cadena = "\""
        i = 0
        int_c2 = ord(c2)
        while c2 != '\"':
            if c2 == "":
                self.genError(8)
                exit(2)
            if 31 < int_c2 < 255 and int_c2 != 127:
                cadena = cadena + c2
                c2 = f2.read(1)
            else:
                self.genToken(2,"")
                self.genError(3)  # error caracter no imprimible
            i += 1
        cadena += '\"'
        if i < 65:
            self.genToken(2, cadena)
        else:
            self.genToken(2, "")
            self.genError(4)  # error cadena muy larga, máximo 65 caracteres
        return c2

    def leerIdentificador(self, f2, c2):
        cadena = f"{c2}"
        c2 = f2.read(1)
        while 'a' <= c2 <= 'z' or 'A' <= c2 <= 'Z' or c2 == "_" or "0" <= c2 <= "9":
            cadena = cadena + c2
            c2 = f2.read(1)
        self.genToken(3, cadena)
        return c2

    def analizador(self):
        res = ""
        if self.leido:
            self.c = self.f.read(1)
        self.leido = True
        while self.c != "":
            match self.c:
                case '+':
                    self.genToken(6, "")
                    self.char_valido = True
                case '*':
                    self.genToken(7, "")
                    self.char_valido = True
                case '<':
                    self.genToken(9, "")
                    self.char_valido = True
                case '(':
                    self.genToken(24, "")
                    self.char_valido = True
                case ')':
                    self.genToken(25, "")
                    self.char_valido = True
                case '{':
                    self.genToken(26, "")
                    self.char_valido = True
                case '}':
                    self.genToken(27, "")
                    self.char_valido = True
                case '=':
                    self.c = self.f.read(1)
                    if self.c == '=':
                        self.genToken(8, "")
                        self.leido = True
                    else:
                        self.leido = False
                        self.genToken(12, "")
                    self.char_valido = True
                case '-':
                    self.c = self.f.read(1)
                    self.leido = True
                    if self.c == '-':
                        self.genToken(11, "")
                    else:
                        self.leido = False
                        self.genError(5)  # Caracter no previsto, se espera un -
                    self.char_valido = True
                case '&':
                    self.c = self.f.read(1)
                    self.leido = True
                    if self.c == '&':
                        self.genToken(10, "")
                    else:
                        self.leido = False
                        self.genError(6)  # Caracter no previsto, se espera un &
                    self.char_valido = True
                case '/':
                    self.c = self.f.read(1)
                    self.leido = True
                    if self.c == '*':
                        self.leerComentario(self.f)
                    else:
                        self.leido = False
                        self.genError(7)  # Caracter no previsto, se espera un *
                    self.char_valido = True
                case '\"':
                    self.c = self.leerCadena(self.f)
                    self.leido = True
                    self.char_valido = True
                case '\n':
                    self.nLinea += 1
                    #print(f"nLinea = {self.nLinea} ")
                    self.char_valido = True
                case ' ':
                    self.char_valido = True
                case '\t':
                    self.char_valido = True
                case ',':
                    self.genToken(29, "")
                    self.char_valido = True
                case ';':
                    self.genToken(30, "")
                    self.char_valido = True
            if self.leido and '0' <= self.c <= '9':
                self.c = self.leerNumero(self.f, self.c)
                self.leido = False
                self.char_valido = True
            elif self.leido and ('a' <= self.c <= 'z' or 'A' <= self.c <= 'Z'):
                self.c = self.leerIdentificador(self.f, self.c)
                self.char_valido = True
                self.leido = False

            if not self.char_valido:
                self.genError(1)
            self.char_valido = False

            if self.token != "":
                aux = self.token
                self.token = ""
                return aux

            if self.leido:
                self.c = self.f.read(1)
            self.leido = True


        self.genToken(31,"")

        return " <31,> "

