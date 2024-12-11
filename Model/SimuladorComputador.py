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
import time

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
        self.salida = ""
        self.flags = {
            "Z": 0,  # Zero flag
            "S": 0,  # Sign flag
            "O": 0   # Overflow flag
        }

    def run(self, program, demora):

        # Cargar programa en la memoria
        n = 0
        valor = True
        for i, instruccion in enumerate(program):
            # Se codifica la memoria de texto a binario de 32 bits
            instruccion = self.ensamblador.codificarInstruccion(instruccion)
            if instruccion == "No se pueden escribir numeros negativos" or instruccion == "Excede el tamaño de la memoria" or instruccion == "Excede el tamaño posible de numero en instrucción":
                # print(instruccion)
                valor = False
                break
            self.memory.escribirInstruccion(i, str(instruccion))
            n = i
            #print(self.memory.memory[n])
            time.sleep(demora)

        while valor:
            self.registroControl("00", self.pc.contador, "")
            time.sleep(demora)
            self.transferenciasMemoria()
            time.sleep(demora)
            if self.memory.señal == "00":
                self.datoMemoriaMBR()
                time.sleep(demora)
                self.bus.transferirDato(self.mbr, self.ir)
                time.sleep(demora)
                self.bus.transferirDato(self.ir, self.control)
                time.sleep(demora)
                instruccion = self.control.decode()
                time.sleep(demora)

                if int(self.pc.contador, 2) > n:
                    self.pc.contador == "" + bin(0)[2:].zfill(32)
                    print("El contador (PC) supera el HLT")
                    break

                if instruccion[1] == "Memoria" and int(instruccion[2], 2) <= n and instruccion[0] != "JMP":
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
                    valorx = self.mov(instruccion, demora)
                    if valorx[0] == 1:
                       print("La posicion de memoria " + str(int(valorx[1], 2)) + " no ha sido inicializada")
                       break

                if instruccion[0] == "ADD":
                    valorx = self.add(instruccion, demora)
                    if valorx[0] == 1 or valorx[0] == 2:
                       print("La posicion de memoria " + str(int(valorx[1], 2)) + " no ha sido inicializada")
                       break
                    self.alu.carry = 0
                    self.alu.overflow = 0

                if instruccion[0] == "JMP":
                    self.jmp(instruccion, demora)

                if instruccion[0] == "STORE":
                    self.store(instruccion, demora)

                if instruccion[0] == "LOAD":
                    self.load(instruccion, demora)

                if instruccion[0] == "AND":
                    valorx = self.instruccionAnd(instruccion, demora)
                    if valorx[0] == 1 or valorx[0] == 2:
                        print("La posicion de memoria " + valorx[1] + " no ha sido inicializada")
                        break

                if instruccion[0] == "OR":
                    valorx = self.instruccionOr(instruccion, demora)
                    if valorx[0] == 2:
                        print("La posicion de memoria " + valorx[1] + " no ha sido inicializada")
                        break

                if instruccion[0] == "NOT":
                    valorx = self.instruccionNot(instruccion, demora)
                    if valorx[0] == 1:
                        print("La posicion de memoria " + valorx[1] + " no ha sido inicializada")
                        break

                if instruccion[0] == "SKIP":
                    self.alu.dato1 = self.pc.contador
                    time.sleep(demora)
                    self.alu.dato2 = "01".zfill(32)
                    time.sleep(demora)
                    self.alu.add()
                    time.sleep(demora)
                    self.pc.contador = self.alu.result
                    time.sleep(demora)

                self.alu.dato1 = self.pc.contador
                time.sleep(demora)
                self.alu.dato2 = "01"
                time.sleep(demora)
                self.alu.add()
                time.sleep(demora)
                self.pc.contador = self.alu.result
                time.sleep(demora)
    



    def mov(self, instruccion, demora):
        if instruccion[1] == "Registro" and instruccion[3] == "Inmediato":
            self.registroControl("01", instruccion[2], instruccion[4].zfill(32))
            time.sleep(demora)
            self.transferenciasRegistros()
            time.sleep(demora)
            self.bus.transferirDato(self.control, self.registros)
            time.sleep(demora)
            if self.registros.señal == "01": self.registros.write()
            time.sleep(demora)
            return [0, ""]

        if instruccion[1] == "Registro" and instruccion[3] == "Memoria":
            self.registroControl("00", instruccion[4], "")
            time.sleep(demora)
            self.transferenciasMemoria()
            time.sleep(demora)
            if self.memory.señal == "00": self.datoMemoriaMBR()
            time.sleep(demora)
            self.registroControl("01", instruccion[2], "")
            time.sleep(demora)
            self.bus.transferirDato(self.mbr, self.control)
            time.sleep(demora)
            if self.control.dato == "": return [2, instruccion[4]]
            time.sleep(demora)
            self.transferenciasRegistros()
            time.sleep(demora)
            self.bus.transferirDato(self.control, self.registros)
            time.sleep(demora)
            if self.registros.señal == "01": self.registros.write()
            time.sleep(demora)
            return [0, ""]

        if instruccion[1] == "Registro" and instruccion[3] == "Registro":
            self.registroControl("00", instruccion[4], "")
            time.sleep(demora)
            self.transferenciasRegistros()
            time.sleep(demora)
            if self.registros.señal == "00": self.registros.read()
            time.sleep(demora)
            if self.registros.dato == "": return [2, instruccion[4]]
            time.sleep(demora)
            self.registroControl("01", instruccion[2], "")
            time.sleep(demora)
            self.transferenciasRegistros()
            time.sleep(demora)
            if self.registros.señal == "01": self.registros.write()
            time.sleep(demora)
            return [0, ""]

        if instruccion[1] == "Memoria" and instruccion[3] == "Registro":
            self.registroControl("00", instruccion[4], "")
            time.sleep(demora)
            self.transferenciasRegistros()
            time.sleep(demora)
            if self.registros.señal == "00": self.registros.read()
            time.sleep(demora)
            if self.registros.dato == "": return [2, instruccion[4]]
            time.sleep(demora)
            self.bus.transferirDato(self.registros, self.mbr)
            time.sleep(demora)
            self.registroControl("01", instruccion[2], "")
            time.sleep(demora)
            self.transferenciasMemoria()
            time.sleep(demora)
            if self.memory.señal == "01": self.memory.write()
            time.sleep(demora)
            return [0, ""]

        if instruccion[1] == "Memoria" and instruccion[3] == "Inmediato":
            self.registroControl("01", instruccion[2], instruccion[4].zfill(32))
            time.sleep(demora)
            self.control.moverDatoMBR(self.mbr, self.control)
            time.sleep(demora)
            self.transferenciasMemoria()
            time.sleep(demora)
            if self.memory.señal == "01": self.memory.write()
            time.sleep(demora)
            return [0, ""]

        if instruccion[1] == "Memoria" and instruccion[3] == "Memoria":
            self.registroControl("00", instruccion[4], "")
            time.sleep(demora)
            self.transferenciasMemoria()
            time.sleep(demora)
            if self.memory.señal == "00": self.memory.read()
            time.sleep(demora)
            if self.memory.dato == "": return [1, instruccion[4]]
            time.sleep(demora)
            self.registroControl("01", instruccion[2], "")
            time.sleep(demora)
            self.bus.transferirDato(self.memory, self.mbr)
            time.sleep(demora)
            self.transferenciasMemoria()
            time.sleep(demora)
            if self.memory.señal == "01": self.memory.write()
            time.sleep(demora)
            return [0, ""]

    def add(self, instruccion, demora):
        if instruccion[1] == "Registro" and instruccion[3] == "Inmediato":
            time.sleep(demora)
            self.alu.dato1 = instruccion[4]
            time.sleep(demora)
            self.registroControl("00", instruccion[2], "")
            time.sleep(demora)
            self.transferenciasRegistros()
            time.sleep(demora)
            if self.registros.señal == "00": self.registros.read()
            time.sleep(demora)
            self.bus.transferirDato(self.registros, self.control)
            time.sleep(demora)
            self.alu.dato2 = self.control.dato
            time.sleep(demora)
            valor = self.alu.add()
            time.sleep(demora)
            if valor == 2: return [valor, instruccion[2]]
            time.sleep(demora)
            self.registroControl("01", instruccion[2], self.alu.result)
            time.sleep(demora)
            self.transferenciasRegistros()
            time.sleep(demora)
            self.bus.transferirDato(self.control, self.registros)
            time.sleep(demora)
            if self.registros.señal == "01": self.registros.write()
            time.sleep(demora)
            return [valor, ""]

        if instruccion[1] == "Registro" and instruccion[3] == "Memoria":
            self.registroControl("00", instruccion[4], "")
            time.sleep(demora)
            self.transferenciasMemoria()
            time.sleep(demora)
            if self.memory.señal == "00":  self.datoMemoriaMBR()
            time.sleep(demora)
            self.bus.transferirDato(self.mbr, self.control)
            time.sleep(demora)
            self.alu.dato1 = self.control.dato
            time.sleep(demora)
            self.registroControl("00", instruccion[2], "")
            time.sleep(demora)
            self.transferenciasRegistros()
            time.sleep(demora)
            if self.registros.señal == "00": self.registros.read()
            time.sleep(demora)
            self.bus.transferirDato(self.registros, self.control)
            time.sleep(demora)
            self.alu.dato2 = self.control.dato
            time.sleep(demora)
            valor = self.alu.add()
            time.sleep(demora)
            if valor == 1: return [valor, instruccion[4]]
            if valor == 2: return [valor, instruccion[2]]
            self.registroControl("01", instruccion[2], self.alu.result)
            time.sleep(demora)
            self.transferenciasRegistros()
            time.sleep(demora)
            self.bus.transferirDato(self.control, self.registros)
            time.sleep(demora)
            if self.registros.señal == "01": self.registros.write()
            time.sleep(demora)
            return [valor, ""]

        if instruccion[1] == "Registro" and instruccion[3] == "Registro":
            self.registroControl("00", instruccion[4], "")
            time.sleep(demora)
            self.transferenciasRegistros()
            time.sleep(demora)
            if self.registros.señal == "00":  self.registros.read()
            time.sleep(demora)
            self.bus.transferirDato(self.registros, self.control)
            time.sleep(demora)
            self.alu.dato1 = self.control.dato
            time.sleep(demora)
            self.registroControl("00", instruccion[2], "")
            time.sleep(demora)
            self.transferenciasRegistros()
            time.sleep(demora)
            if self.registros.señal == "00": self.registros.read()
            time.sleep(demora)
            self.bus.transferirDato(self.registros, self.control)
            time.sleep(demora)
            self.alu.dato2 = self.control.dato
            time.sleep(demora)
            valor = self.alu.add()
            time.sleep(demora)
            if valor == 1: return [valor, instruccion[4]]
            if valor == 2: return [valor, instruccion[2]]
            self.registroControl("01", instruccion[2], self.alu.result)
            time.sleep(demora)
            self.transferenciasRegistros()
            time.sleep(demora)
            self.bus.transferirDato(self.control, self.registros)
            time.sleep(demora)
            if self.registros.señal == "01": self.registros.write()
            time.sleep(demora)
            return [valor, ""]

        if instruccion[1] == "Memoria" and instruccion[3] == "Inmediato":
            self.alu.dato1 = instruccion[4]
            time.sleep(demora)
            self.registroControl("00", instruccion[2], "")
            time.sleep(demora)
            self.transferenciasMemoria()
            time.sleep(demora)
            if self.memory.señal == "00": self.datoMemoriaMBR()
            time.sleep(demora)
            self.bus.transferirDato(self.mbr, self.control)
            time.sleep(demora)
            self.alu.dato2 = self.control.dato
            time.sleep(demora)
            valor = self.alu.add()
            time.sleep(demora)
            if valor == 2: return [valor, instruccion[2]]
            self.registroControl("01", instruccion[2], self.alu.result)
            time.sleep(demora)
            self.bus.transferirDato(self.control, self.mbr)
            time.sleep(demora)
            self.transferenciasMemoria()
            time.sleep(demora)
            if self.memory.señal == "01": self.memory.write()
            time.sleep(demora)
            return [valor, ""]

        if instruccion[1] == "Memoria" and instruccion[3] == "Memoria":
            self.registroControl("00", instruccion[4], "")
            time.sleep(demora)
            self.transferenciasMemoria()
            time.sleep(demora)
            if self.memory.señal == "00":  self.datoMemoriaMBR()
            time.sleep(demora)
            self.bus.transferirDato(self.mbr, self.control)
            time.sleep(demora)
            self.alu.dato1 = self.control.dato
            time.sleep(demora)
            self.registroControl("00", instruccion[2], "")
            time.sleep(demora)
            self.transferenciasMemoria()
            time.sleep(demora)
            if self.memory.señal == "00": self.datoMemoriaMBR()
            time.sleep(demora)
            self.bus.transferirDato(self.mbr, self.control)
            time.sleep(demora)
            self.alu.dato2 = self.control.dato
            time.sleep(demora)
            valor = self.alu.add()
            time.sleep(demora)
            if valor == 1: return[valor, instruccion[4]]
            if valor == 2: return[valor, instruccion[2]]
            self.registroControl("01", instruccion[2], self.alu.result)
            time.sleep(demora)
            self.bus.transferirDato(self.control, self.mbr)
            time.sleep(demora)
            self.transferenciasMemoria()
            time.sleep(demora)
            if self.memory.señal == "01": self.memory.write()
            time.sleep(demora)
            return [valor, ""]

        if instruccion[1] == "Memoria" and instruccion[3] == "Registro":
            self.registroControl("00", instruccion[4], "")
            time.sleep(demora)
            self.transferenciasRegistros()
            time.sleep(demora)
            if self.registros.señal == "00":  self.registros.read()
            time.sleep(demora)
            self.bus.transferirDato(self.registros, self.control)
            time.sleep(demora)
            self.alu.dato1 = self.control.dato
            time.sleep(demora)
            self.registroControl("00", instruccion[2], "")
            time.sleep(demora)
            self.transferenciasMemoria()
            time.sleep(demora)
            if self.memory.señal == "00": self.datoMemoriaMBR()
            time.sleep(demora)
            self.bus.transferirDato(self.mbr, self.control)
            time.sleep(demora)
            self.alu.dato2 = self.control.dato
            time.sleep(demora)
            valor = self.alu.add()
            time.sleep(demora)
            if valor == 1:  return [valor, instruccion[4]]
            if valor == 2:  return [valor, instruccion[2]]
            self.registroControl("01", instruccion[2], self.alu.result)
            time.sleep(demora)
            self.bus.transferirDato(self.control, self.mbr)
            time.sleep(demora)
            self.transferenciasMemoria()
            time.sleep(demora)
            if self.memory.señal == "01": self.memory.write()
            time.sleep(demora)
            return [valor, ""]

    def jmp(self, instruccion, demora):
        if instruccion[1] == "Registro":
            self.registroControl("00", instruccion[2], "")
            time.sleep(demora)
            self.transferenciasRegistros()
            time.sleep(demora)
            if self.registros.señal == "00": self.registros.read()
            time.sleep(demora)
            self.bus.transferirDato(self.registros, self.control)
            time.sleep(demora)
            self.pc.contador = bin(int(self.control.dato, 2) - 1)[2:].zfill(32)
            time.sleep(demora)

        if instruccion[1] == "Inmediato":
            self.control.dato = instruccion[2]
            time.sleep(demora)
            self.pc.contador = bin(int(self.control.dato, 2) - 1)[2:].zfill(32)
            time.sleep(demora)

        if instruccion[1] == "Memoria":
            self.control.direccion = instruccion[2]
            time.sleep(demora)
            self.pc.contador = bin(int(self.control.direccion, 2) - 1)[2:].zfill(32)
            time.sleep(demora)
         
    def store(self, instruccion, demora):
        self.registroControl("00", instruccion[4], "")
        time.sleep(demora)
        self.transferenciasRegistros()
        time.sleep(demora)
        if self.registros.señal == "00": self.registros.read()
        time.sleep(demora)
        self.registroControl("01", instruccion[2], "")
        time.sleep(demora)
        self.bus.transferirDato(self.registros, self.mbr)
        time.sleep(demora)
        self.transferenciasMemoria()
        time.sleep(demora)
        if self.memory.señal == "01": self.memory.write()
        time.sleep(demora)

    def load(self, instruccion, demora):
        self.registroControl("00", instruccion[4], "")
        time.sleep(demora)
        self.transferenciasMemoria()
        time.sleep(demora)
        if self.memory.señal == "00": self.datoMemoriaMBR()
        time.sleep(demora)
        self.registroControl("01", instruccion[2], "")
        time.sleep(demora)
        self.transferenciasRegistros()
        time.sleep(demora)
        self.bus.transferirDato(self.mbr, self.registros)
        time.sleep(demora)
        if self.registros.señal == "01": self.registros.write()
        time.sleep(demora)
    
    def instruccionAnd(self, instruccion, demora):
        if instruccion[1] == "Registro" and instruccion[3] == "Inmediato":
            self.alu.dato1 = instruccion[4].zfill(32)
            time.sleep(demora)
            self.registroControl("00", instruccion[2], "")
            time.sleep(demora)
            self.transferenciasRegistros()
            time.sleep(demora)
            if self.registros.señal == "00": self.registros.read()
            time.sleep(demora)
            self.bus.transferirDato(self.registros, self.control)
            time.sleep(demora)
            self.alu.dato2 = self.control.dato
            time.sleep(demora)
            valor = self.alu.operacionAnd()
            time.sleep(demora)
            if valor == 2: [valor, str(int(instruccion[2], 2))]
            time.sleep(demora)
            self.registroControl("01", instruccion[2], self.alu.result)
            time.sleep(demora)
            self.transferenciasRegistros()
            time.sleep(demora)
            self.bus.transferirDato(self.control, self.registros)
            time.sleep(demora)
            if self.registros.señal == "01": self.registros.write()
            time.sleep(demora)
            return [0, ""]

        if instruccion[1] == "Registro" and instruccion[3] == "Memoria":
            self.registroControl("00", instruccion[4], "")
            time.sleep(demora)
            self.transferenciasMemoria()
            time.sleep(demora)
            if self.memory.señal == "00":  self.datoMemoriaMBR()
            time.sleep(demora)
            self.bus.transferirDato(self.mbr, self.control)
            time.sleep(demora)
            self.alu.dato1 = self.control.dato
            time.sleep(demora)
            self.registroControl("00", instruccion[2], "")
            time.sleep(demora)
            self.transferenciasRegistros()
            time.sleep(demora)
            if self.registros.señal == "00": self.registros.read()
            time.sleep(demora)
            self.bus.transferirDato(self.registros, self.control)
            time.sleep(demora)
            self.alu.dato2 = self.control.dato
            time.sleep(demora)
            valor = self.alu.operacionAnd()
            time.sleep(demora)
            if valor == 1: return [valor, str(int(instruccion[4], 2))]
            if valor == 2: return [valor, str(int(instruccion[2], 2))]
            self.registroControl("01", instruccion[2], self.alu.result)
            time.sleep(demora)
            self.transferenciasRegistros()
            time.sleep(demora)
            self.bus.transferirDato(self.control, self.registros)
            time.sleep(demora)
            if self.registros.señal == "01": self.registros.write()
            time.sleep(demora)
            return [valor, ""]

        if instruccion[1] == "Registro" and instruccion[3] == "Registro":
            self.registroControl("00", instruccion[4], "")
            time.sleep(demora)
            self.transferenciasRegistros()
            time.sleep(demora)
            if self.registros.señal == "00":  self.registros.read()
            time.sleep(demora)
            self.bus.transferirDato(self.registros, self.control)
            time.sleep(demora)
            self.alu.dato1 = self.control.dato
            time.sleep(demora)
            self.registroControl("00", instruccion[2], "")
            time.sleep(demora)
            self.transferenciasRegistros()
            time.sleep(demora)
            if self.registros.señal == "00": self.registros.read()
            time.sleep(demora)
            self.bus.transferirDato(self.registros, self.control)
            time.sleep(demora)
            self.alu.dato2 = self.control.dato
            time.sleep(demora)
            valor = self.alu.operacionAnd()
            time.sleep(demora)
            if valor == 1: return [valor, str(int(instruccion[4], 2))]
            if valor == 2: return [valor, str(int(instruccion[2], 2))]
            self.registroControl("01", instruccion[2], self.alu.result)
            time.sleep(demora)
            self.transferenciasRegistros()
            time.sleep(demora)
            self.bus.transferirDato(self.control, self.registros)
            time.sleep(demora)
            if self.registros.señal == "01": self.registros.write()
            time.sleep(demora)
            return [valor, ""]

        if instruccion[1] == "Memoria" and instruccion[3] == "Inmediato":
            self.alu.dato1 = instruccion[4].zfill(32)
            time.sleep(demora)
            self.registroControl("00", instruccion[2], "")
            time.sleep(demora)
            self.transferenciasMemoria()
            time.sleep(demora)
            if self.memory.señal == "00": self.datoMemoriaMBR()
            time.sleep(demora)
            self.bus.transferirDato(self.mbr, self.control)
            time.sleep(demora)
            self.alu.dato2 = self.control.dato
            time.sleep(demora)
            valor = self.alu.operacionAnd()
            time.sleep(demora)
            if valor == 2: return [valor, str(int(instruccion[2], 2))]
            self.registroControl("01", instruccion[2], self.alu.result)
            time.sleep(demora)
            self.bus.transferirDato(self.control, self.mbr)
            time.sleep(demora)
            self.transferenciasMemoria()
            time.sleep(demora)
            if self.memory.señal == "01": self.memory.write()
            time.sleep(demora)
            return [0, ""]

        if instruccion[1] == "Memoria" and instruccion[3] == "Memoria":
            self.registroControl("00", instruccion[4], "")
            time.sleep(demora)
            self.transferenciasMemoria()
            time.sleep(demora)
            if self.memory.señal == "00":  self.datoMemoriaMBR()
            time.sleep(demora)
            self.bus.transferirDato(self.mbr, self.control)
            time.sleep(demora)
            self.alu.dato1 = self.control.dato
            time.sleep(demora)
            self.registroControl("00", instruccion[2], "")
            time.sleep(demora)
            self.transferenciasMemoria()
            time.sleep(demora)
            if self.memory.señal == "00": self.datoMemoriaMBR()
            time.sleep(demora)
            self.bus.transferirDato(self.mbr, self.control)
            time.sleep(demora)
            self.alu.dato2 = self.control.dato
            time.sleep(demora)
            valor = self.alu.operacionAnd()
            time.sleep(demora)
            if valor == 1: return [valor, str(int(instruccion[4], 2))]
            if valor == 2: return [valor, str(int(instruccion[2], 2))]
            self.registroControl("01", instruccion[2], self.alu.result)
            time.sleep(demora)
            self.bus.transferirDato(self.control, self.mbr)
            time.sleep(demora)
            self.transferenciasMemoria()
            time.sleep(demora)
            if self.memory.señal == "01": self.memory.write()
            time.sleep(demora)
            return [valor, ""]

        if instruccion[1] == "Memoria" and instruccion[3] == "Registro":
            self.registroControl("00", instruccion[4], "")
            time.sleep(demora)
            self.transferenciasRegistros()
            time.sleep(demora)
            if self.registros.señal == "00":  self.registros.read()
            time.sleep(demora)
            self.bus.transferirDato(self.registros, self.control)
            time.sleep(demora)
            self.alu.dato1 = self.control.dato
            time.sleep(demora)
            self.registroControl("00", instruccion[2], "")
            time.sleep(demora)
            self.transferenciasMemoria()
            time.sleep(demora)
            if self.memory.señal == "00": self.datoMemoriaMBR()
            time.sleep(demora)
            self.bus.transferirDato(self.mbr, self.control)
            time.sleep(demora)
            self.alu.dato2 = self.control.dato
            time.sleep(demora)
            valor = self.alu.operacionAnd()
            time.sleep(demora)
            if valor == 1: return [valor, str(int(instruccion[4], 2))]
            if valor == 2: return [valor, str(int(instruccion[2], 2))]
            self.registroControl("01", instruccion[2], self.alu.result)
            time.sleep(demora)
            self.bus.transferirDato(self.control, self.mbr)
            time.sleep(demora)
            self.transferenciasMemoria()
            time.sleep(demora)
            if self.memory.señal == "01": self.memory.write()
            time.sleep(demora)
            return [valor, ""]

    def instruccionOr(self, instruccion, demora):
        if instruccion[1] == "Registro" and instruccion[3] == "Inmediato":
            self.alu.dato1 = instruccion[4].zfill(32)
            time.sleep(demora)
            self.registroControl("00", instruccion[2], "")
            time.sleep(demora)
            self.transferenciasRegistros()
            time.sleep(demora)
            if self.registros.señal == "00": self.registros.read()
            time.sleep(demora)
            self.bus.transferirDato(self.registros, self.control)
            time.sleep(demora)
            self.alu.dato2 = self.control.dato
            time.sleep(demora)
            valor = self.alu.operacionOr()
            time.sleep(demora)
            if valor == 2: [valor, str(int(instruccion[2], 2))]
            time.sleep(demora)
            self.registroControl("01", instruccion[2], self.alu.result)
            time.sleep(demora)
            self.transferenciasRegistros()
            time.sleep(demora)
            self.bus.transferirDato(self.control, self.registros)
            time.sleep(demora)
            if self.registros.señal == "01": self.registros.write()
            time.sleep(demora)
            return [0, ""]

        if instruccion[1] == "Registro" and instruccion[3] == "Memoria":
            self.registroControl("00", instruccion[4], "")
            time.sleep(demora)
            self.transferenciasMemoria()
            time.sleep(demora)
            if self.memory.señal == "00":  self.datoMemoriaMBR()
            time.sleep(demora)
            self.bus.transferirDato(self.mbr, self.control)
            time.sleep(demora)
            self.alu.dato1 = self.control.dato
            time.sleep(demora)
            self.registroControl("00", instruccion[2], "")
            time.sleep(demora)
            self.transferenciasRegistros()
            time.sleep(demora)
            if self.registros.señal == "00": self.registros.read()
            time.sleep(demora)
            self.bus.transferirDato(self.registros, self.control)
            time.sleep(demora)
            self.alu.dato2 = self.control.dato
            time.sleep(demora)
            valor = self.alu.operacionOr()
            time.sleep(demora)
            if valor == 1: return [valor, str(int(instruccion[4], 2))]
            if valor == 2: return [valor, str(int(instruccion[2], 2))]
            self.registroControl("01", instruccion[2], self.alu.result)
            time.sleep(demora)
            self.transferenciasRegistros()
            time.sleep(demora)
            self.bus.transferirDato(self.control, self.registros)
            time.sleep(demora)
            if self.registros.señal == "01": self.registros.write()
            time.sleep(demora)
            return [valor, ""]

        if instruccion[1] == "Registro" and instruccion[3] == "Registro":
            self.registroControl("00", instruccion[4], "")
            time.sleep(demora)
            self.transferenciasRegistros()
            time.sleep(demora)
            if self.registros.señal == "00":  self.registros.read()
            time.sleep(demora)
            self.bus.transferirDato(self.registros, self.control)
            time.sleep(demora)
            self.alu.dato1 = self.control.dato
            time.sleep(demora)
            self.registroControl("00", instruccion[2], "")
            time.sleep(demora)
            self.transferenciasRegistros()
            time.sleep(demora)
            if self.registros.señal == "00": self.registros.read()
            time.sleep(demora)
            self.bus.transferirDato(self.registros, self.control)
            time.sleep(demora)
            self.alu.dato2 = self.control.dato
            time.sleep(demora)
            valor = self.alu.operacionOr()
            time.sleep(demora)
            if valor == 1: return [valor, str(int(instruccion[4], 2))]
            if valor == 2: return [valor, str(int(instruccion[2], 2))]
            self.registroControl("01", instruccion[2], self.alu.result)
            time.sleep(demora)
            self.transferenciasRegistros()
            time.sleep(demora)
            self.bus.transferirDato(self.control, self.registros)
            time.sleep(demora)
            if self.registros.señal == "01": self.registros.write()
            time.sleep(demora)
            return [valor, ""]

        if instruccion[1] == "Memoria" and instruccion[3] == "Inmediato":
            self.alu.dato1 = instruccion[4].zfill(32)
            time.sleep(demora)
            self.registroControl("00", instruccion[2], "")
            time.sleep(demora)
            self.transferenciasMemoria()
            time.sleep(demora)
            if self.memory.señal == "00": self.datoMemoriaMBR()
            time.sleep(demora)
            self.bus.transferirDato(self.mbr, self.control)
            time.sleep(demora)
            self.alu.dato2 = self.control.dato
            time.sleep(demora)
            valor = self.alu.operacionOr()
            time.sleep(demora)
            if valor == 2: return [valor, str(int(instruccion[2], 2))]
            time.sleep(demora)
            self.registroControl("01", instruccion[2], self.alu.result)
            time.sleep(demora)
            self.bus.transferirDato(self.control, self.mbr)
            time.sleep(demora)
            self.transferenciasMemoria()
            time.sleep(demora)
            if self.memory.señal == "01": self.memory.write()
            time.sleep(demora)
            return [0, ""]

        if instruccion[1] == "Memoria" and instruccion[3] == "Memoria":
            self.registroControl("00", instruccion[4], "")
            time.sleep(demora)
            self.transferenciasMemoria()
            time.sleep(demora)
            if self.memory.señal == "00":  self.datoMemoriaMBR()
            time.sleep(demora)
            self.bus.transferirDato(self.mbr, self.control)
            time.sleep(demora)
            self.alu.dato1 = self.control.dato
            time.sleep(demora)
            self.registroControl("00", instruccion[2], "")
            time.sleep(demora)
            self.transferenciasMemoria()
            time.sleep(demora)
            if self.memory.señal == "00": self.datoMemoriaMBR()
            time.sleep(demora)
            self.bus.transferirDato(self.mbr, self.control)
            time.sleep(demora)
            self.alu.dato2 = self.control.dato
            time.sleep(demora)
            valor = self.alu.operacionOr()
            time.sleep(demora)
            if valor == 1: return [valor, str(int(instruccion[4], 2))]
            if valor == 2: return [valor, str(int(instruccion[2], 2))]
            self.registroControl("01", instruccion[2], self.alu.result)
            time.sleep(demora)
            self.bus.transferirDato(self.control, self.mbr)
            time.sleep(demora)
            self.transferenciasMemoria()
            time.sleep(demora)
            if self.memory.señal == "01": self.memory.write()
            time.sleep(demora)
            return [valor, ""]

        if instruccion[1] == "Memoria" and instruccion[3] == "Registro":
            self.registroControl("00", instruccion[4], "")
            time.sleep(demora)
            self.transferenciasRegistros()
            time.sleep(demora)
            if self.registros.señal == "00":  self.registros.read()
            time.sleep(demora)
            self.bus.transferirDato(self.registros, self.control)
            time.sleep(demora)
            self.alu.dato1 = self.control.dato
            time.sleep(demora)
            self.registroControl("00", instruccion[2], "")
            time.sleep(demora)
            self.transferenciasMemoria()
            time.sleep(demora)
            if self.memory.señal == "00": self.datoMemoriaMBR()
            time.sleep(demora)
            self.bus.transferirDato(self.mbr, self.control)
            time.sleep(demora)
            self.alu.dato2 = self.control.dato
            time.sleep(demora)
            valor = self.alu.operacionOr()
            time.sleep(demora)
            if valor == 1: return [valor, str(int(instruccion[4], 2))]
            if valor == 2: return [valor, str(int(instruccion[2], 2))]
            self.registroControl("01", instruccion[2], self.alu.result)
            time.sleep(demora)
            self.bus.transferirDato(self.control, self.mbr)
            time.sleep(demora)
            self.transferenciasMemoria()
            time.sleep(demora)
            if self.memory.señal == "01": self.memory.write()
            time.sleep(demora)
            return [valor, ""]

    def instruccionNot(self, instruccion, demora):
        if instruccion[1] == "Registro":
            self.registroControl("00", instruccion[2], "")
            time.sleep(demora)
            self.transferenciasRegistros()
            time.sleep(demora)
            if self.registros.señal == "00": self.registros.read()
            time.sleep(demora)
            self.bus.transferirDato(self.registros, self.control)
            time.sleep(demora)
            self.alu.dato1 = self.control.dato
            time.sleep(demora)
            valor = self.alu.operacionNot()
            time.sleep(demora)
            if valor == 1: return [valor, str(int(instruccion[2], 2))]
            self.registroControl("01", instruccion[2], self.alu.result)
            time.sleep(demora)
            self.bus.transferirDato(self.control, self.registros)
            time.sleep(demora)
            self.transferenciasRegistros()
            time.sleep(demora)
            if self.registros.señal == "01": self.registros.write()
            time.sleep(demora)
            return [valor, ""]

        if instruccion[1] == "Memoria":
            self.registroControl("00", instruccion[2], "")
            time.sleep(demora)
            self.transferenciasMemoria()
            time.sleep(demora)
            if self.memory.señal == "00": self.datoMemoriaMBR()
            time.sleep(demora)
            self.bus.transferirDato(self.mbr, self.control)
            time.sleep(demora)
            self.alu.dato1 = self.control.dato
            time.sleep(demora)
            valor = self.alu.operacionNot()
            time.sleep(demora)
            if valor == 1: return [valor, str(int(instruccion[2], 2))]
            self.registroControl("01", instruccion[2], self.alu.result)
            time.sleep(demora)
            self.bus.transferirDato(self.control, self.mbr)
            time.sleep(demora)
            self.transferenciasMemoria()
            time.sleep(demora)
            if self.memory.señal == "01": self.memory.write()
            time.sleep(demora)
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

    # paso a paso
    def step(self):
        """
        Ejecuta una instrucción y actualiza el estado del simulador.
        """
        # Dirección actual del PC
        direccion_actual = int(self.pc.contador, 2)

        # Leer instrucción de la memoria
        self.mar.direccion = bin(direccion_actual)[2:].zfill(10)
        self.memory.read()
        self.mbr.dato = self.memory.dato

        # Decodificar instrucción
        self.ir.dato = self.mbr.dato
        instruccion = self.control.decode()

        # Ejecutar instrucción
        if instruccion[0] == "HLT":
            print("Programa detenido.")
            return

        instrucciones = {
            "MOV": self.mov,
            "ADD": self.add,
            "JMP": self.jmp,
            "STORE": self.store,
            "LOAD": self.load,
            "AND": self.instruccionAnd,
            "OR": self.instruccionOr,
            "NOT": self.instruccionNot,
        }

        if instruccion[0] in instrucciones:
            instrucciones[instruccion[0]](instruccion)

        # Incrementar PC
        self.alu.dato1 = self.pc.contador
        self.alu.dato2 = "00000000000000000000000000000001"
        self.alu.add()
        self.pc.contador = self.alu.result
