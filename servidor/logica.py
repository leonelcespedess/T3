from utils import data_json

class Logica:

    def __init__(self, padre) -> None:

        self.padre = padre
        self.nombre_1 = None
        self.nombre_2 = None
    
    def procesar_mensaje(self, mensaje, socket_cliente):
        try:
            accion = mensaje["accion"]
        except KeyError:
            print("No esta la llave accion en el diccionario")
        
        if mensaje["accion"] == "login":
            estado = self.validar_login(mensaje["nombre"])
            return estado

    def validar_login(self, nombre):

        if not nombre.isalnum() or not(0  < len(nombre) <= 10):
            print("|" + nombre + " login invalido".center(80, " ") + "|")
            return {"accion": "login", "estado": "invalido"}
        
        elif nombre == self.nombre_1 or nombre == self.nombre_2:
            print("|" + nombre + " login invalido".center(80, " ") + "|")
            return {"accion": "login", "estado": "nombre repetido"}

        else:
            print("|" + nombre + " login valido".center(80, " ") + "|")
            return {"accion": "login", "estado": "valido", "timer": data_json("TIMER_ESPERA")}
    

    