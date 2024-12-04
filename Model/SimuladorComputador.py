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
    def __init__(self, memory_size=256):
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
        for i, instruccion in enumerate(program):
            # Se codifica la memoria de texto a binario de 32 bits
            instruccion = self.ensamblador.codificarInstruccion(instruccion)
            print(instruccion)
            self.memory.write(i, instruccion)

        while True:
            # Se define que se hara lectura de instruccion
            self.control.señal = "00"
            #La UC toma la direccion del PC y la pone en el MAR
            self.control.moverPCaMAR(self.mar, self.pc.contador)
            #El bus de control toma la señal dada por la UC y la lleva a la memoria
            self.bus.transferirControl(self.control, self.memory)
            #El bus de direcciones toma la direccion del MAR y le indica a la Memoria que esa es la direccion
            self.bus.transferirDireccion(self.mar, self.memory)
            if self.memory.señal == "00":
                # Al definirse que se debe leer el dato, se tiene en cuenta y se elimina la dirección
                self.memory.dato = self.memory.read(int(self.memory.direccion, 2))
                self.memory.direccion = ""
                # El bus de datos toma el dato de la memoria y lo lleva al MBR
                self.bus.transferirDato(self.memory, self.mbr)
                # El bus de datos toma el dato del MBR y lo lleva al IR
                self.bus.transferirDato(self.mbr, self.ir)
                # La UC toma la instruccion del IR y la decodifica
            break

'''
        # Ejecutar ciclo de instrucciones
        while True:
            instruction = self.control.fetch(self.memory)
            if instruction == "HALT":  # Detener si se encuentra HALT
                print("Ejecución finalizada.")
                break
            try:
                op_code, operand = self.control.decode(instruction)
            except ValueError as e:
                print(f"Error en la instrucción: {e}")
                break

            if op_code == "ADD":
                self.alu.add(self.registros.read_GPR(0), operand)
                self.registros.write_GPR(0, self.alu.result)
            elif op_code == "AND":
                self.alu.and_operation(self.registros.read_GPR(0), operand)
                self.registros.write_GPR(0, self.alu.result)
            elif op_code == "MOV":
                self.registros.write_GPR(0, operand)

            # Imprimir estado de la simulación
            print(f"PC: {self.registros.PC}, IR: {self.registros.IR}, GPR: {self.registros.GPR}")
'''
