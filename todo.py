# Clase Alu

class Alu:
    def __init__(self):
        self.result = ""
        self.dato1 = "00"
        self.dato2 = "00"
        self.flags = {"zero": 0, "carry": 0}  # Banderas para carry y zero

    def add(self):
        if self.dato1 == "":
            return 2
        if self.dato2 == "":
            return 3
        self.result = int(self.dato1, 2) + int(self.dato2, 2)
        
        # Verificar si hay desbordamiento o no
        if self.result > 2147483647 or self.result < -2147483648:
            return 1

        # Banderas
        self.flags["carry"] = 1 if self.result > 255 else 0  # Asumiendo overflow en 8 bits
        self.result = bin(self.result)[2:].zfill(32)

        # Verificar si el resultado es cero
        self.flags["zero"] = 1 if self.result == "0" else 0
        
        self.dato1 = ""
        self.dato2 = ""
        return 0

    def operacionAnd(self):
        if self.dato1 == "":
            return 1
        if self.dato2 == "":
            return 2
        self.result = ""
        n = 0
        for i in self.dato1:
            if i == "1" and self.dato2[n] == "1":
                self.result += "1"
            else:
                self.result += "0"
            n += 1
        
        # Banderas
        self.flags["zero"] = 1 if self.result == "0" * len(self.result) else 0
        
        self.dato1 = ""
        self.dato2 = ""
        return 0

    def operacionOr(self):
        if self.dato1 == "":
            return 1
        if self.dato2 == "":
            return 2
        self.result = ""
        n = 0
        for i in self.dato1:
            if i == "1" or self.dato2[n] == "1":
                self.result += "1"
            else:
                self.result += "0"
            n += 1
        
        # Banderas
        self.flags["zero"] = 1 if self.result == "0" * len(self.result) else 0
        
        self.dato1 = ""
        self.dato2 = ""
        return 0

    def operacionNot(self):
        if self.dato1 == "":
            return 1
        self.result = ""
        n = 0
        for i in self.dato1:
            if i == "1":
                self.result += "0"
            else:
                self.result += "1"
            n += 1
        
        # Banderas
        self.flags["zero"] = 1 if self.result == "0" * len(self.result) else 0
        
        self.dato1 = ""
        return 0

# Clase Bus

class Bus:
    def __init__(self):
        pass

    # El bus de direccion toma la señal dada por un origen y la lleva al destino
    def transferirDireccion(self, origen, destino):
        destino.direccion = origen.direccion
        origen.direccion = ""

    # El bus de control toma la señal dada por un origen y la lleva al destino
    def transferirControl(self, origen, destino):
        destino.señal = origen.señal
        origen.señal = ""

    #El bus de datos toma la señal dada por un origen y la lleva al destino
    def transferirDato(self, origen, destino):
        destino.dato = origen.dato
        origen.dato = ""
    
    def transferirContador(self, contador, destino):
        destino.direccion = contador

# Clase Ensamblador

class Ensamblador:
    def __init__(self):
        pass

    def codificarInstruccion(self, instruccion):
        instruccion = instruccion.split()
        nuevaInstruccion = ""
        for i in instruccion:
            i = i.strip(",")
            if i == "MOV": nuevaInstruccion += "00000000"
            if i == "ADD": nuevaInstruccion += "00000001"
            if i == "HLT": nuevaInstruccion += "00000010" + bin(0)[2:].zfill(24)
            if i == "JMP": nuevaInstruccion += "00000011"
            if i == "STORE": nuevaInstruccion += "00000100"
            if i == "LOAD": nuevaInstruccion += "00000101"
            if i == "AND": nuevaInstruccion += "00000110"
            if i == "OR": nuevaInstruccion += "00000111"
            if i == "NOT": nuevaInstruccion += "00001000"
            if i == "SKIP": nuevaInstruccion += "00001001"
            if i == "AL": nuevaInstruccion += "000000000000"
            if i == "BL": nuevaInstruccion += "000000000001"
            if i == "CL": nuevaInstruccion += "000000000010"
            if i == "DL": nuevaInstruccion += "000000000011"
            if self.es_numero(i) == True: 
                if int(i) < 0:
                    return "No se pueden escribir numeros negativos"
                if int(i) > 511:
                    return "Excede el tamaño posible de numero en instrucción"
                nuevaInstruccion += "11" + bin(int(i))[2:].zfill(10)
            if i[0] == "[":
                i = i.replace('[', '').replace(']', '').strip()
                if int(i) > 1023:
                    return "Excede el tamaño de la memoria"
                nuevaInstruccion += '01' + bin(int(i))[2:].zfill(10)
        if len(nuevaInstruccion) != 32:
            n = 32 - len(nuevaInstruccion)
            nuevaInstruccion += bin(0)[2:].zfill(n)
        return nuevaInstruccion

    def es_numero(self, numero):
        try:
            int(numero)  # Intentamos convertir a float
            return True
        except ValueError:
            return False
        
# Clase Ir

class Ir:
    def __init__(self):
        self.dato = ""

# Clase Mar

class Mar:
    def __init__(self):
        self.direccion = ""

# Clase Mbr

class Mbr:
    def __init__(self):
        self.dato = ""

# Clase Memoria

class Memoria:
    def __init__(self, size):
        self.memory = [0] * size  # Iniciar memoria de tamaño `size` cambie yo por 0 en vez de ""
        self.direccion = "" # Direccion que necesita la memoria
        self.señal = "" # Accion a realizar dada por el bus de control
        self.dato = "" # Dato que se encontraba en la direccion

    def write(self):
        self.memory[int(self.direccion, 2)] = self.dato

    def escribirInstruccion(self, address, value):
        self.memory[address] = str(value)

    def read(self):
        self.dato = self.memory[int(self.direccion, 2)]

# Clase Pc

class Pc:
    def __init__(self):
        self.contador = "" + bin(0)[2:].zfill(32)



# Clase Registros
class Registros:
    def __init__(self):
        self.AL = ""
        self.BL = ""
        self.CL = ""
        self.DL = ""
        self.señal = ""
        self.dato = ""
        self.direccion = ""

    def write(self):
        if self.direccion == "0000000000": self.AL = self.dato
        if self.direccion == "0000000001": self.BL = self.dato
        if self.direccion == "0000000010": self.CL = self.dato
        if self.direccion == "0000000011": self.DL = self.dato

    def read(self):
        if self.direccion == "0000000000": self.dato = self.AL
        if self.direccion == "0000000001": self.dato = self.BL
        if self.direccion == "0000000010": self.dato = self.CL
        if self.direccion == "0000000011": self.dato = self.DL

# Clase UnidadControl
class UnidadControl:
    def __init__(self):
        self.señal = ""
        self.direccion = ""
        self.dato = ""

    def moverDatoMBR(self, destino, origen):
        destino.dato = origen.dato
        origen.dato = ""

    def transferirDireccion(self, direccion, destino):
        destino.direccion = direccion

    def tranferirSeñal(self, señal, destino):
        destino.señal = señal

    def transferirDato(self, dato, destino):
        destino.dato = dato

    def decode(self):
        instruccion = [self.dato[:8]]
        instruccion.append(self.dato[8:20])
        instruccion.append(self.dato[20:])
        nuevaInstruccion = []
        for i in instruccion:
            if i == "00000000": nuevaInstruccion.append("MOV")
            if i == "00000001": nuevaInstruccion.append("ADD")
            if i == "00000010": nuevaInstruccion.append("HLT")
            if i == "00000011": nuevaInstruccion.append("JMP")
            if i == "00000100": nuevaInstruccion.append("STORE")
            if i == "00000101": nuevaInstruccion.append("LOAD")
            if i == "00000110": nuevaInstruccion.append("AND")
            if i == "00000111": nuevaInstruccion.append("OR")
            if i == "00001000": nuevaInstruccion.append("NOT")
            if i == "00001001": nuevaInstruccion.append("SKIP")
            if len(i) == 12:
                if i[:2] == "00": nuevaInstruccion.append("Registro")
                if i[:2] == "01": nuevaInstruccion.append("Memoria")
                if i[:2] == "11": nuevaInstruccion.append("Inmediato")
                nuevaInstruccion.append(i[2:])
        return nuevaInstruccion

# Clase SimuladorComputador

from Model.Alu import Alu
from Model.UnidadControl import UnidadControl
from Model.Memoria import Memoria
from Model.Registros import Registros
from Model.Bus import Bus
from Model.Ensamblador import Ensamblador
from Model.Pc import Pc
from Model.Mar import Mar
from Model.Mbr import Mbr
from Model.Ir import Ir



class SimuladorComputador:
    def __init__(self, memory_size = 1024):
        self.alu = Alu()
        self.control = UnidadControl()
        self.memory = Memoria(memory_size)
        self.registros = Registros()
        self.bus = Bus()
        self.ensamblador = Ensamblador()
        self.pc = Pc()
        self.mar = Mar()
        self.mbr = Mbr()
        self.ir = Ir()
        self.flags = {
            "Z": 0,  # Zero flag
            "S": 0,  # Sign flag
            "O": 0   # Overflow flag
        }

    def run(self, program):

        # Cargar programa en la memoria
        n = 0
        valor = True
        for i, instruccion in enumerate(program):
            # Se codifica la memoria de texto a binario de 32 bits
            instruccion = self.ensamblador.codificarInstruccion(instruccion)
            if instruccion == "No se pueden escribir numeros negativos" or instruccion == "Excede el tamaño de la memoria" or instruccion == "Excede el tamaño posible de numero en instrucción":
                print(instruccion)
                valor = False
                break
            self.memory.escribirInstruccion(i, str(instruccion))
            n = i

        while valor:
            self.registroControl("00", self.pc.contador, "")
            self.transferenciasMemoria()
            if self.memory.señal == "00":
                self.datoMemoriaMBR()
                self.bus.transferirDato(self.mbr, self.ir)
                self.bus.transferirDato(self.ir, self.control)
                instruccion = self.control.decode()

                if int(self.pc.contador, 2) > n:
                    self.pc.contador == "" + bin(0)[2:].zfill(32)
                    print("El contador (PC) supera el HLT")
                    break

                if instruccion[1] == "Memoria" and int(instruccion[2], 2) <= n:
                    self.pc.contador == "" + bin(0)[2:].zfill(32)
                    print("No puede modificar los espacios de memoria antes del hlt")
                    break

                if instruccion[3] == "Memoria" and int(instruccion[4], 2) <= n:
                    self.pc.contador == "" + bin(0)[2:].zfill(32)
                    print("No puede usar los espacios de memoria antes del hlt")
                    break

                if instruccion[0] == "JMP" and instruccion[1] == "Memoria" and int(instruccion[2], 2) > n:
                    self.pc.contador == "" + bin(0)[2:].zfill(32)
                    print("No puede saltar a un espacio de memoria mayor al hlt")
                    break

                if instruccion[0] == "STORE" and (instruccion[1] != "Memoria" or instruccion[3] != "Registro"):
                    self.pc.contador == "" + bin(0)[2:].zfill(32)
                    print("La estructura del store es STORE [Direccion de memoria], Registro. Cualquier otro valor no se ejecutara")
                    break

                if instruccion[0] == "STORE" and int(instruccion[2], 2) < n:
                    self.pc.contador == "" + bin(0)[2:].zfill(32)
                    print("No se puede hacer Store en los espacios de memoria usados para el programa")
                    break

                if instruccion[0] == "LOAD" and (instruccion[1] != "Registro" or instruccion[3] != "Memoria"):
                    self.pc.contador == "" + bin(0)[2:].zfill(32)
                    print("La estructura del load es LOAD Registro, [Direccion de memoria]. cualquier otro valor no se ejecutara")
                    break      

                if instruccion[0] == "LOAD" and int(instruccion[4], 2) < n:
                    self.pc.contador == "" + bin(0)[2:].zfill(32)
                    print("No se puede hacer load en los espacios de memoria usados para el programa")
                    break            

                if instruccion[0] == "HLT":
                    print("PC: " + self.pc.contador)
                    self.pc.contador == "" + bin(0)[2:].zfill(32)
                    self.imprimir()
                    break

                if instruccion[0] == "MOV":
                    valorx = self.mov(instruccion)
                    if valorx[0] == 1:
                       print("La posicion de memoria " + str(int(valorx[1], 2)) + " no ha sido inicializada")
                       break

                if instruccion[0] == "ADD":
                    valorx = self.add(instruccion)
                    if valorx[0] == 1:
                        print("El resultado no se puede almacenar porque supera los valores minimos y maximos permitidos")
                        break
                    if valorx[0] == 2:
                       print("La posicion de memoria " + str(int(valorx[1], 2)) + " no ha sido inicializada")
                       break

                if instruccion[0] == "JMP":
                    self.jmp(instruccion)

                if instruccion[0] == "STORE":
                    self.store(instruccion)

                if instruccion[0] == "LOAD":
                    self.load(instruccion)

                if instruccion[0] == "AND":
                    valorx = self.instruccionAnd(instruccion)
                    if valorx[0] == 1 or valorx[0] == 2:
                        print("La posicion de memoria " + valorx[1] + " no ha sido inicializada")
                        break
                
                if instruccion[0] == "AND":
                    valorx = self.instruccionAnd(instruccion)
                    if valorx[0] == 2:
                        print("La posicion de memoria " + valorx[1] + " no ha sido inicializada")
                        break

                if instruccion[0] == "OR":
                    valorx = self.instruccionOr(instruccion)
                    if valorx[0] == 2:
                        print("La posicion de memoria " + valorx[1] + " no ha sido inicializada")
                        break

                if instruccion[0] == "NOT":
                    valorx = self.instruccionNot(instruccion)
                    if valorx[0] == 1:
                        print("La posicion de memoria " + valorx[1] + " no ha sido inicializada")
                        break

                if instruccion[0] == "SKIP":
                    self.alu.dato1 = self.pc.contador
                    self.alu.dato2 = "01"
                    self.alu.add()
                    self.pc.contador = self.alu.result

                self.alu.dato1 = self.pc.contador
                self.alu.dato2 = "01"
                self.alu.add()
                self.pc.contador = self.alu.result
    
    def mov(self, instruccion):
        if instruccion[1] == "Registro" and instruccion[3] == "Inmediato":
            self.registroControl("01", instruccion[2], instruccion[4].zfill(32))
            self.transferenciasRegistros()
            self.bus.transferirDato(self.control, self.registros)
            if self.registros.señal == "01": self.registros.write()
            return [0, ""]

        if instruccion[1] == "Registro" and instruccion[3] == "Memoria":
            self.registroControl("00", instruccion[4], "")
            self.transferenciasMemoria()
            if self.memory.señal == "00": self.datoMemoriaMBR()
            self.registroControl("01", instruccion[2], "")
            self.bus.transferirDato(self.mbr, self.control)
            if self.control.dato == "": return [2, instruccion[4]]
            self.transferenciasRegistros()
            self.bus.transferirDato(self.control, self.registros)
            if self.registros.señal == "01": self.registros.write()
            return [0, ""]

        if instruccion[1] == "Registro" and instruccion[3] == "Registro":
            self.registroControl("00", instruccion[4], "")
            self.transferenciasRegistros()
            if self.registros.señal == "00": self.registros.read()
            if self.registros.dato == "": return [2, instruccion[4]]
            self.registroControl("01", instruccion[2], "")
            self.transferenciasRegistros()
            if self.registros.señal == "01": self.registros.write()
            return [0, ""]

        if instruccion[1] == "Memoria" and instruccion[3] == "Registro":
            self.registroControl("00", instruccion[4], "")
            self.transferenciasRegistros()
            if self.registros.señal == "00": self.registros.read()
            if self.registros.dato == "": return [2, instruccion[4]]
            self.bus.transferirDato(self.registros, self.mbr)
            self.registroControl("01", instruccion[2], "")
            self.transferenciasMemoria()
            if self.memory.señal == "01": self.memory.write()
            return [0, ""]

        if instruccion[1] == "Memoria" and instruccion[3] == "Inmediato":
            self.registroControl("01", instruccion[2], instruccion[4].zfill(32))
            self.control.moverDatoMBR(self.mbr, self.control)
            self.transferenciasMemoria()
            if self.memory.señal == "01": self.memory.write()
            return [0, ""]

        if instruccion[1] == "Memoria" and instruccion[3] == "Memoria":
            self.registroControl("00", instruccion[4], "")
            self.transferenciasMemoria()
            if self.memory.señal == "00": self.memory.read()
            if self.memory.dato == "": return [1, instruccion[4]]
            self.registroControl("01", instruccion[2], "")
            self.bus.transferirDato(self.memory, self.mbr)
            self.transferenciasMemoria()
            if self.memory.señal == "01": self.memory.write()
            return [0, ""]

    def add(self, instruccion):
        if instruccion[1] == "Registro" and instruccion[3] == "Inmediato":
            self.alu.dato1 = instruccion[4]
            self.registroControl("00", instruccion[2], "")
            self.transferenciasRegistros()
            if self.registros.señal == "00": self.registros.read()
            self.bus.transferirDato(self.registros, self.control)
            self.alu.dato2 = self.control.dato
            valor = self.alu.add()
            if valor == 1:
                return [valor, ""]
            self.registroControl("01", instruccion[2], self.alu.result)
            self.transferenciasRegistros()
            self.bus.transferirDato(self.control, self.registros)
            if self.registros.señal == "01": self.registros.write()
            return [valor, ""]

        if instruccion[1] == "Registro" and instruccion[3] == "Memoria":
            self.registroControl("00", instruccion[4], "")
            self.transferenciasMemoria()
            if self.memory.señal == "00":  self.datoMemoriaMBR()
            self.bus.transferirDato(self.mbr, self.control)
            self.alu.dato1 = self.control.dato
            self.registroControl("00", instruccion[2], "")
            self.transferenciasRegistros()
            if self.registros.señal == "00": self.registros.read()
            self.bus.transferirDato(self.registros, self.control)
            self.alu.dato2 = self.control.dato
            valor = self.alu.add()
            if valor == 1:
                return [valor, ""]
            if valor == 2:
                return [valor, instruccion[4]]
            self.registroControl("01", instruccion[2], self.alu.result)
            self.transferenciasRegistros()
            self.bus.transferirDato(self.control, self.registros)
            if self.registros.señal == "01": self.registros.write()
            return [valor, ""]

        if instruccion[1] == "Registro" and instruccion[3] == "Registro":
            self.registroControl("00", instruccion[4], "")
            self.transferenciasRegistros()
            if self.registros.señal == "00":  self.registros.read()
            self.bus.transferirDato(self.registros, self.control)
            self.alu.dato1 = self.control.dato
            self.registroControl("00", instruccion[2], "")
            self.transferenciasRegistros()
            if self.registros.señal == "00": self.registros.read()
            self.bus.transferirDato(self.registros, self.control)
            self.alu.dato2 = self.control.dato
            valor = self.alu.add()
            if valor == 1:
                return [valor, ""]
            self.registroControl("01", instruccion[2], self.alu.result)
            self.transferenciasRegistros()
            self.bus.transferirDato(self.control, self.registros)
            if self.registros.señal == "01": self.registros.write()
            return [valor, ""]

        if instruccion[1] == "Memoria" and instruccion[3] == "Inmediato":
            self.alu.dato1 = instruccion[4]
            self.registroControl("00", instruccion[2], "")
            self.transferenciasMemoria()
            if self.memory.señal == "00": self.datoMemoriaMBR()
            self.bus.transferirDato(self.mbr, self.control)
            self.alu.dato2 = self.control.dato
            valor = self.alu.add()
            if valor == 1:
                return [valor, ""]
            self.registroControl("01", instruccion[2], self.alu.result)
            self.bus.transferirDato(self.control, self.mbr)
            self.transferenciasMemoria()
            if self.memory.señal == "01": self.memory.write()
            return [valor, ""]

        if instruccion[1] == "Memoria" and instruccion[3] == "Memoria":
            self.registroControl("00", instruccion[4], "")
            self.transferenciasMemoria()
            if self.memory.señal == "00":  self.datoMemoriaMBR()
            self.bus.transferirDato(self.mbr, self.control)
            self.alu.dato1 = self.control.dato
            self.registroControl("00", instruccion[2], "")
            self.transferenciasMemoria()
            if self.memory.señal == "00": self.datoMemoriaMBR()
            self.bus.transferirDato(self.mbr, self.control)
            self.alu.dato2 = self.control.dato
            valor = self.alu.add()
            if valor == 1:
                return [valor, ""]
            if valor == 2:
                return[valor, instruccion[4]]
            if valor == 1:
                return[valor, instruccion[2]]
            self.registroControl("01", instruccion[2], self.alu.result)
            self.bus.transferirDato(self.control, self.mbr)
            self.transferenciasMemoria()
            if self.memory.señal == "01": self.memory.write()
            return [valor, ""]

        if instruccion[1] == "Memoria" and instruccion[3] == "Registro":
            self.registroControl("00", instruccion[4], "")
            self.transferenciasRegistros()
            if self.registros.señal == "00":  self.registros.read()
            self.bus.transferirDato(self.registros, self.control)
            self.alu.dato1 = self.control.dato
            self.registroControl("00", instruccion[2], "")
            self.transferenciasMemoria()
            if self.memory.señal == "00": self.datoMemoriaMBR()
            self.bus.transferirDato(self.mbr, self.control)
            self.alu.dato2 = self.control.dato
            valor = self.alu.add()
            if valor == 1:
                return [valor, ""]
            self.registroControl("01", instruccion[2], self.alu.result)
            self.bus.transferirDato(self.control, self.mbr)
            self.transferenciasMemoria()
            if self.memory.señal == "01": self.memory.write()
            return [valor, ""]

    def jmp(self, instruccion):
        if instruccion[1] == "Registro":
            self.registroControl("00", instruccion[2], "")
            self.transferenciasRegistros()
            if self.registros.señal == "00": self.registros.read()
            self.bus.transferirDato(self.registros, self.control)
            self.pc.contador = bin(int(self.control.dato, 2) - 1)[2:].zfill(32)

        if instruccion[1] == "Inmediato":
            self.control.dato = instruccion[2]
            self.pc.contador = bin(int(self.control.dato, 2) - 1)[2:].zfill(32)

        if instruccion[1] == "Memoria":
            self.control.direccion = instruccion[2]
            self.pc.contador = bin(int(self.control.direccion, 2) - 1)[2:].zfill(32)
         
    def store(self, instruccion):
        self.registroControl("00", instruccion[4], "")
        self.transferenciasRegistros()
        if self.registros.señal == "00": self.registros.read()
        self.registroControl("01", instruccion[2], "")
        self.bus.transferirDato(self.registros, self.mbr)
        self.transferenciasMemoria()
        if self.memory.señal == "01": self.memory.write()

    def load(self, instruccion):
        self.registroControl("00", instruccion[4], "")
        self.transferenciasMemoria()
        if self.memory.señal == "00": self.datoMemoriaMBR()
        self.registroControl("01", instruccion[2], "")
        self.transferenciasRegistros()
        self.bus.transferirDato(self.mbr, self.registros)
        if self.registros.señal == "01": self.registros.write()
    
    def instruccionAnd(self, instruccion):
        if instruccion[1] == "Registro" and instruccion[3] == "Inmediato":
            self.alu.dato1 = instruccion[4].zfill(32)
            self.registroControl("00", instruccion[2], "")
            self.transferenciasRegistros()
            if self.registros.señal == "00": self.registros.read()
            self.bus.transferirDato(self.registros, self.control)
            self.alu.dato2 = self.control.dato
            valor = self.alu.operacionAnd()
            if valor == 2: [valor, str(int(instruccion[2], 2))]
            self.registroControl("01", instruccion[2], self.alu.result)
            self.transferenciasRegistros()
            self.bus.transferirDato(self.control, self.registros)
            if self.registros.señal == "01": self.registros.write()
            return [0, ""]

        if instruccion[1] == "Registro" and instruccion[3] == "Memoria":
            self.registroControl("00", instruccion[4], "")
            self.transferenciasMemoria()
            if self.memory.señal == "00":  self.datoMemoriaMBR()
            self.bus.transferirDato(self.mbr, self.control)
            self.alu.dato1 = self.control.dato
            self.registroControl("00", instruccion[2], "")
            self.transferenciasRegistros()
            if self.registros.señal == "00": self.registros.read()
            self.bus.transferirDato(self.registros, self.control)
            self.alu.dato2 = self.control.dato
            valor = self.alu.operacionAnd()
            if valor == 1: return [valor, str(int(instruccion[4], 2))]
            if valor == 2: return [valor, str(int(instruccion[2], 2))]
            self.registroControl("01", instruccion[2], self.alu.result)
            self.transferenciasRegistros()
            self.bus.transferirDato(self.control, self.registros)
            if self.registros.señal == "01": self.registros.write()
            return [valor, ""]

        if instruccion[1] == "Registro" and instruccion[3] == "Registro":
            self.registroControl("00", instruccion[4], "")
            self.transferenciasRegistros()
            if self.registros.señal == "00":  self.registros.read()
            self.bus.transferirDato(self.registros, self.control)
            self.alu.dato1 = self.control.dato
            self.registroControl("00", instruccion[2], "")
            self.transferenciasRegistros()
            if self.registros.señal == "00": self.registros.read()
            self.bus.transferirDato(self.registros, self.control)
            self.alu.dato2 = self.control.dato
            valor = self.alu.operacionAnd()
            if valor == 1: return [valor, str(int(instruccion[4], 2))]
            if valor == 2: return [valor, str(int(instruccion[2], 2))]
            self.registroControl("01", instruccion[2], self.alu.result)
            self.transferenciasRegistros()
            self.bus.transferirDato(self.control, self.registros)
            if self.registros.señal == "01": self.registros.write()
            return [valor, ""]

        if instruccion[1] == "Memoria" and instruccion[3] == "Inmediato":
            self.alu.dato1 = instruccion[4].zfill(32)
            self.registroControl("00", instruccion[2], "")
            self.transferenciasMemoria()
            if self.memory.señal == "00": self.datoMemoriaMBR()
            self.bus.transferirDato(self.mbr, self.control)
            self.alu.dato2 = self.control.dato
            valor = self.alu.operacionAnd()
            if valor == 2: return [valor, str(int(instruccion[2], 2))]
            self.registroControl("01", instruccion[2], self.alu.result)
            self.bus.transferirDato(self.control, self.mbr)
            self.transferenciasMemoria()
            if self.memory.señal == "01": self.memory.write()
            return [0, ""]

        if instruccion[1] == "Memoria" and instruccion[3] == "Memoria":
            self.registroControl("00", instruccion[4], "")
            self.transferenciasMemoria()
            if self.memory.señal == "00":  self.datoMemoriaMBR()
            self.bus.transferirDato(self.mbr, self.control)
            self.alu.dato1 = self.control.dato
            self.registroControl("00", instruccion[2], "")
            self.transferenciasMemoria()
            if self.memory.señal == "00": self.datoMemoriaMBR()
            self.bus.transferirDato(self.mbr, self.control)
            self.alu.dato2 = self.control.dato
            valor = self.alu.operacionAnd()
            if valor == 1: return [valor, str(int(instruccion[4], 2))]
            if valor == 2: return [valor, str(int(instruccion[2], 2))]
            self.registroControl("01", instruccion[2], self.alu.result)
            self.bus.transferirDato(self.control, self.mbr)
            self.transferenciasMemoria()
            if self.memory.señal == "01": self.memory.write()
            return [valor, ""]

        if instruccion[1] == "Memoria" and instruccion[3] == "Registro":
            self.registroControl("00", instruccion[4], "")
            self.transferenciasRegistros()
            if self.registros.señal == "00":  self.registros.read()
            self.bus.transferirDato(self.registros, self.control)
            self.alu.dato1 = self.control.dato
            self.registroControl("00", instruccion[2], "")
            self.transferenciasMemoria()
            if self.memory.señal == "00": self.datoMemoriaMBR()
            self.bus.transferirDato(self.mbr, self.control)
            self.alu.dato2 = self.control.dato
            valor = self.alu.operacionAnd()
            if valor == 1: return [valor, str(int(instruccion[4], 2))]
            if valor == 2: return [valor, str(int(instruccion[2], 2))]
            self.registroControl("01", instruccion[2], self.alu.result)
            self.bus.transferirDato(self.control, self.mbr)
            self.transferenciasMemoria()
            if self.memory.señal == "01": self.memory.write()
            return [valor, ""]

    def instruccionOr(self, instruccion):
        if instruccion[1] == "Registro" and instruccion[3] == "Inmediato":
            self.alu.dato1 = instruccion[4].zfill(32)
            self.registroControl("00", instruccion[2], "")
            self.transferenciasRegistros()
            if self.registros.señal == "00": self.registros.read()
            self.bus.transferirDato(self.registros, self.control)
            self.alu.dato2 = self.control.dato
            valor = self.alu.operacionOr()
            if valor == 2: [valor, str(int(instruccion[2], 2))]
            self.registroControl("01", instruccion[2], self.alu.result)
            self.transferenciasRegistros()
            self.bus.transferirDato(self.control, self.registros)
            if self.registros.señal == "01": self.registros.write()
            return [0, ""]

        if instruccion[1] == "Registro" and instruccion[3] == "Memoria":
            self.registroControl("00", instruccion[4], "")
            self.transferenciasMemoria()
            if self.memory.señal == "00":  self.datoMemoriaMBR()
            self.bus.transferirDato(self.mbr, self.control)
            self.alu.dato1 = self.control.dato
            self.registroControl("00", instruccion[2], "")
            self.transferenciasRegistros()
            if self.registros.señal == "00": self.registros.read()
            self.bus.transferirDato(self.registros, self.control)
            self.alu.dato2 = self.control.dato
            valor = self.alu.operacionOr()
            if valor == 1: return [valor, str(int(instruccion[4], 2))]
            if valor == 2: return [valor, str(int(instruccion[2], 2))]
            self.registroControl("01", instruccion[2], self.alu.result)
            self.transferenciasRegistros()
            self.bus.transferirDato(self.control, self.registros)
            if self.registros.señal == "01": self.registros.write()
            return [valor, ""]

        if instruccion[1] == "Registro" and instruccion[3] == "Registro":
            self.registroControl("00", instruccion[4], "")
            self.transferenciasRegistros()
            if self.registros.señal == "00":  self.registros.read()
            self.bus.transferirDato(self.registros, self.control)
            self.alu.dato1 = self.control.dato
            self.registroControl("00", instruccion[2], "")
            self.transferenciasRegistros()
            if self.registros.señal == "00": self.registros.read()
            self.bus.transferirDato(self.registros, self.control)
            self.alu.dato2 = self.control.dato
            valor = self.alu.operacionOr()
            if valor == 1: return [valor, str(int(instruccion[4], 2))]
            if valor == 2: return [valor, str(int(instruccion[2], 2))]
            self.registroControl("01", instruccion[2], self.alu.result)
            self.transferenciasRegistros()
            self.bus.transferirDato(self.control, self.registros)
            if self.registros.señal == "01": self.registros.write()
            return [valor, ""]

        if instruccion[1] == "Memoria" and instruccion[3] == "Inmediato":
            self.alu.dato1 = instruccion[4].zfill(32)
            self.registroControl("00", instruccion[2], "")
            self.transferenciasMemoria()
            if self.memory.señal == "00": self.datoMemoriaMBR()
            self.bus.transferirDato(self.mbr, self.control)
            self.alu.dato2 = self.control.dato
            valor = self.alu.operacionOr()
            if valor == 2: return [valor, str(int(instruccion[2], 2))]
            self.registroControl("01", instruccion[2], self.alu.result)
            self.bus.transferirDato(self.control, self.mbr)
            self.transferenciasMemoria()
            if self.memory.señal == "01": self.memory.write()
            return [0, ""]

        if instruccion[1] == "Memoria" and instruccion[3] == "Memoria":
            self.registroControl("00", instruccion[4], "")
            self.transferenciasMemoria()
            if self.memory.señal == "00":  self.datoMemoriaMBR()
            self.bus.transferirDato(self.mbr, self.control)
            self.alu.dato1 = self.control.dato
            self.registroControl("00", instruccion[2], "")
            self.transferenciasMemoria()
            if self.memory.señal == "00": self.datoMemoriaMBR()
            self.bus.transferirDato(self.mbr, self.control)
            self.alu.dato2 = self.control.dato
            valor = self.alu.operacionOr()
            if valor == 1: return [valor, str(int(instruccion[4], 2))]
            if valor == 2: return [valor, str(int(instruccion[2], 2))]
            self.registroControl("01", instruccion[2], self.alu.result)
            self.bus.transferirDato(self.control, self.mbr)
            self.transferenciasMemoria()
            if self.memory.señal == "01": self.memory.write()
            return [valor, ""]

        if instruccion[1] == "Memoria" and instruccion[3] == "Registro":
            self.registroControl("00", instruccion[4], "")
            self.transferenciasRegistros()
            if self.registros.señal == "00":  self.registros.read()
            self.bus.transferirDato(self.registros, self.control)
            self.alu.dato1 = self.control.dato
            self.registroControl("00", instruccion[2], "")
            self.transferenciasMemoria()
            if self.memory.señal == "00": self.datoMemoriaMBR()
            self.bus.transferirDato(self.mbr, self.control)
            self.alu.dato2 = self.control.dato
            valor = self.alu.operacionOr()
            if valor == 1: return [valor, str(int(instruccion[4], 2))]
            if valor == 2: return [valor, str(int(instruccion[2], 2))]
            self.registroControl("01", instruccion[2], self.alu.result)
            self.bus.transferirDato(self.control, self.mbr)
            self.transferenciasMemoria()
            if self.memory.señal == "01": self.memory.write()
            return [valor, ""]

    def instruccionNot(self, instruccion):
        if instruccion[1] == "Registro":
            self.registroControl("00", instruccion[2], "")
            self.transferenciasRegistros()
            if self.registros.señal == "00": self.registros.read()
            self.bus.transferirDato(self.registros, self.control)
            self.alu.dato1 = self.control.dato
            valor = self.alu.operacionNot()
            if valor == 1: return [valor, str(int(instruccion[2], 2))]
            self.registroControl("01", instruccion[2], self.alu.result)
            self.bus.transferirDato(self.control, self.registros)
            self.transferenciasRegistros()
            if self.registros.señal == "01": self.registros.write()
            return [valor, ""]

        if instruccion[1] == "Memoria":
            self.registroControl("00", instruccion[2], "")
            self.transferenciasMemoria()
            if self.memory.señal == "00": self.datoMemoriaMBR()
            self.bus.transferirDato(self.mbr, self.control)
            self.alu.dato1 = self.control.dato
            valor = self.alu.operacionNot()
            if valor == 1: return [valor, str(int(instruccion[2], 2))]
            self.registroControl("01", instruccion[2], self.alu.result)
            self.bus.transferirDato(self.control, self.mbr)
            self.transferenciasMemoria()
            if self.memory.señal == "01": self.memory.write()
            return [valor, ""]
    
    def registroControl(self, señal, direccion, dato):
        self.control.señal = señal
        self.control.direccion = direccion
        self.control.dato = dato

    def transferenciasRegistros(self):
        self.bus.transferirControl(self.control, self.registros)
        self.bus.transferirDireccion(self.control, self.registros)
    
    def transferenciasMemoria(self):
        self.bus.transferirDireccion(self.control, self.mar)
        self.bus.transferirControl(self.control, self.memory)
        self.bus.transferirDireccion(self.mar, self.memory)
        self.bus.transferirDato(self.mbr, self.memory)

    def datoMemoriaMBR(self):
        self.memory.read()
        self.bus.transferirDato(self.memory, self.mbr)

    def imprimir(self):
        print("AL: " + self.registros.AL)
        print("BL: " + self.registros.BL)
        print("CL: " + self.registros.CL)
        print("DL: " + self.registros.DL)
        n = 0
        for i in self.memory.memory:
            if i != "":
                print("Memory " + str(n) + "  " + str(i))
            n += 1


    def get_registers(self):
        return self.registros  # Donde registers es un diccionario o estructura similar.
    
    def get_flags(self):
        """
        Retorna los estados actuales de las banderas.
        """
        return self.flags

    def set_flag(self, flag, value):
        """
        Actualiza el valor de una bandera específica.
        """
        if flag in self.flags:
            self.flags[flag] = value
        else:
            raise ValueError(f"Flag '{flag}' no es válida.")

    def reset_flags(self):
        """
        Reinicia todas las banderas a su valor por defecto (0).
        """
        for flag in self.flags:
            self.flags[flag] = 0

    def execute_cmp(self, reg1, reg2):
        """
        Compara dos registros y actualiza las banderas.
        """
        valor1 = int(self.registros.__dict__[reg1], 2)  # Convierte el binario a entero
        valor2 = int(self.registros.__dict__[reg2], 2)

        # Actualizar banderas
        self.flags["Z"] = int(valor1 == valor2)  # Zero flag
        self.flags["S"] = int(valor1 < valor2)  # Sign flag
        self.flags["O"] = 0  # Overflow no aplica aquí

# contenido de main.py

import streamlit as st
from Model.SimuladorComputador import SimuladorComputador
from ui.visualizer import render_state_viewer
from ui.forms import render_code_editor

if "simulador" not in st.session_state:
    # Crear una instancia del simulador
    st.session_state.simulador = SimuladorComputador()
    
st.title("Simulador de Computador")
st.sidebar.title("Opciones")
opcion = st.sidebar.selectbox("Selecciona una vista", ["Estado", "Ejecutar Programa"])

if opcion == "Estado":
    render_code_editor()
    render_state_viewer()