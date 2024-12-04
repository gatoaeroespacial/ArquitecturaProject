class Bus:
    def __init__(self):
        pass

    def transferirDireccion(self, origen, destino):
        destino.direccion = origen.direccion
        origen.direccion = ""

    def transferirControl(self, origen, destino):
        destino.señal = origen.señal
        origen.señal = ""
    
    def transferirDato(self, origen, destino):
        destino.dato = origen.dato
        origen.dato = ""