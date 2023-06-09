from PyQt5.QtCore import pyqtSignal, QObject, QTimer
from threading import Thread
from utils import data_json

class Interfaz(QObject):

    senal_log = pyqtSignal(dict)
    senal_sala_espera = pyqtSignal()
    senal_tiempo_espera = pyqtSignal(int)
    senal_comenzar_juego = pyqtSignal()
    senal_actualizar_nombre = pyqtSignal(str)
    senal_actualizar_nombre_rival = pyqtSignal(str)
    
    def __init__(self) -> None:
        super().__init__()        
    
    def enviar_mensaje(self):
        pass 

    def manejar_mensaje(self, event):
        try:
            accion = event["accion"]
        except KeyError:
            print("No esta bien la llave enviada")
        if accion == "login":
            if event["estado"] == "valido":
                dic = {"estado": "valido", "timer": event["timer"]}
                self.senal_log.emit(dic)
                print("Valido")
            
            elif event["estado"] == "nombre repetido":
                dic = {"estado": "invalido", "razon": "nombre"}
                self.senal_log.emit(dic)
                print("invalido")  
            else:
                dic = {"estado": "invalido", "razon": "otra"}
                self.senal_log.emit(dic)
                print("invalido")
        elif accion == "sala llena":
            dic = {"estado": "sala_llena"}
            self.senal_log.emit(dic)
            print("Sala llena")
            
        elif accion == "timer_espera":
            self.senal_tiempo_espera.emit(event["tiempo"])
        
        elif accion == "comenzar_juego":
            print("comenzar")
            self.senal_comenzar_juego.emit()
        
        elif accion == "nombre_propio":
            self.senal_actualizar_nombre.emit(event["nombre"])
        
        elif accion == "nombre_rival":
            self.senal_actualizar_nombre_rival.emit(event["nombre"])

    def cambio_pestana(self, event):
        if event == "sala de espera":
            self.senal_sala_espera.emit()

    