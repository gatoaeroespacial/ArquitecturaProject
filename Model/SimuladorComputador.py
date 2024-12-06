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

                if instruccion[1] == "Memoria" and int(instruccion[2], 2) == n:
                    self.pc.contador == "" + bin(0)[2:].zfill(32)
                    print("No puede modificar el espacio de memoria donde esta el hlt")
                    break

                if instruccion[3] == "Memoria" and int(instruccion[4], 2) == n:
                    self.pc.contador == "" + bin(0)[2:].zfill(32)
                    print("No puede usar el espacio de memoria donde esta el hlt")
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
                    self.mov(instruccion)

                if instruccion[0] == "ADD":
                   self.add(instruccion)

                if instruccion[0] == "JMP":
                    self.jmp(instruccion)

                if instruccion[0] == "STORE":
                    self.store(instruccion)

                if instruccion[0] == "LOAD":
                    self.load(instruccion)

                self.alu.dato1 = self.pc.contador
                self.alu.dato2 = "01"
                self.alu.add()
                self.pc.contador = self.alu.result
    
    def mov(self, instruccion):
        if instruccion[1] == "Registro" and instruccion[3] == "Inmediato":
            self.registroControl("01", instruccion[2], instruccion[4].zfill(32))
            self.transferenciasRegistros()
            self.bus.transferirDato(self.control, self.registros)
            if self.registros.señal == "01": 
                self.registros.write()

        if instruccion[1] == "Registro" and instruccion[3] == "Memoria":
            self.registroControl("00", instruccion[4], "")
            self.transferenciasMemoria()
            if self.memory.señal == "00": self.datoMemoriaMBR()
            self.registroControl("01", instruccion[2], "")
            self.bus.transferirDato(self.mbr, self.control)
            self.transferenciasRegistros()
            self.bus.transferirDato(self.control, self.registros)
            if self.registros.señal == "01": self.registros.write()

        if instruccion[1] == "Registro" and instruccion[3] == "Registro":
            self.registroControl("00", instruccion[4], "")
            self.transferenciasRegistros()
            if self.registros.señal == "00": self.registros.read()
            self.registroControl("01", instruccion[2], "")
            self.transferenciasRegistros()
            if self.registros.señal == "01": self.registros.write()

        if instruccion[1] == "Memoria" and instruccion[3] == "Registro":
            self.registroControl("00", instruccion[4], "")
            self.transferenciasRegistros()
            if self.registros.señal == "00": self.registros.read()
            self.bus.transferirDato(self.registros, self.mbr)
            self.registroControl("01", instruccion[2], "")
            self.transferenciasMemoria()
            if self.memory.señal == "01": self.memory.write()

        if instruccion[1] == "Memoria" and instruccion[3] == "Inmediato":
            self.registroControl("01", instruccion[2], instruccion[4].zfill(32))
            self.control.moverDatoMBR(self.mbr, self.control)
            self.transferenciasMemoria()
            if self.memory.señal == "01":
                self.memory.write()

        if instruccion[1] == "Memoria" and instruccion[3] == "Memoria":
            self.registroControl("00", instruccion[4], "")
            self.transferenciasMemoria()
            if self.memory.señal == "00": self.memory.read()
            self.registroControl("01", instruccion[2], "")
            self.bus.transferirDato(self.memory, self.mbr)
            self.transferenciasMemoria()
            if self.memory.señal == "01": self.memory.write()

    def add(self, instruccion):
        if instruccion[1] == "Registro" and instruccion[3] == "Inmediato":
            self.alu.dato1 = instruccion[4]
            self.registroControl("00", instruccion[2], "")
            self.transferenciasRegistros()
            if self.registros.señal == "00": self.registros.read()
            self.bus.transferirDato(self.registros, self.control)
            self.alu.dato2 = self.control.dato
            self.alu.add()
            self.registroControl("01", instruccion[2], self.alu.result)
            self.transferenciasRegistros()
            self.bus.transferirDato(self.control, self.registros)
            if self.registros.señal == "01": self.registros.write()

        if instruccion[1] == "Registro" and instruccion[3] == "Memoria":
            print(instruccion)
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
            if valor == "No se puede ejecutar porque no se ha incializado el espacio ":
                return "No se puede ejecutar porque no se ha incializado el espacio " + "de memoria " + str(int(instruccion[4], 2))
            self.registroControl("01", instruccion[2], self.alu.result)
            self.transferenciasRegistros()
            self.bus.transferirDato(self.control, self.registros)
            if self.registros.señal == "01": self.registros.write()

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
            self.alu.add()
            self.registroControl("01", instruccion[2], self.alu.result)
            self.transferenciasRegistros()
            self.bus.transferirDato(self.control, self.registros)
            if self.registros.señal == "01": self.registros.write()

        if instruccion[1] == "Memoria" and instruccion[3] == "Inmediato":
            self.alu.dato1 = instruccion[4]
            self.registroControl("00", instruccion[2], "")
            self.transferenciasMemoria()
            if self.memory.señal == "00": self.datoMemoriaMBR()
            self.bus.transferirDato(self.mbr, self.control)
            self.alu.dato2 = self.control.dato
            self.alu.add()
            self.registroControl("01", instruccion[2], self.alu.result)
            self.bus.transferirDato(self.control, self.mbr)
            self.transferenciasMemoria()
            if self.memory.señal == "01": self.memory.write()

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
            self.alu.add()
            self.registroControl("01", instruccion[2], self.alu.result)
            self.bus.transferirDato(self.control, self.mbr)
            self.transferenciasMemoria()
            if self.memory.señal == "01": self.memory.write()

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
            self.alu.add()
            self.registroControl("01", instruccion[2], self.alu.result)
            self.bus.transferirDato(self.control, self.mbr)
            self.transferenciasMemoria()
            if self.memory.señal == "01": self.memory.write()

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
