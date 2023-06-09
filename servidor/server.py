import socket
from threading import Thread
import json
from cripto import desencriptar, encriptar
from logica import Logica
from utils import data_json
from PyQt5.QtCore import QTimer,QObject
from time import sleep


class Servidor(QObject):
    

    def __init__(self, port, host):
        self.host = host
        self.port = port
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sockets = {}
        self.cliente_1 = False
        self.cliente_1_nombre = None
        self.cliente_2 = False
        self.cliente_2_nombre = None
        self.jugando = False

        self.logica = Logica(self)

        self.listos = {1: False, 2: False}

        #bindeo
        self.socket_server.bind((self.host, self.port))
        self.socket_server.listen()
        #aceptar
        thread = Thread(target= self.aceptar_conecciones, daemon= True)
        thread.start()

    def aceptar_conecciones(self):
        while True:
            cliente = 0
            try:
                socket_cliente, address = self.socket_server.accept()

                print("se conecto el de direccion ", address)
                if not self.cliente_1:
                    cliente = 1
                    self.cliente_1 = True

                elif not self.cliente_2:
                    cliente = 2
                    self.cliente_2 = True

                if cliente != 0:
                    thread = Thread(target=self.escuchar_cliente, 
                            args= (cliente, socket_cliente), daemon=True)
                    thread.start()
                    self.sockets[cliente] = socket_cliente

                else:
                    data = {"accion": "sala llena"}
                    self.enviar_mensaje(socket_cliente, data)
                    self.log(f"Un cliente intento ingresar a la sala" 
                        + " pero esta llena")


            except ConnectionError:
                print("error")
                return

    def escuchar_cliente(self, id_cliente ,socket_cliente: socket):
        self.log(f"Comenzando a escuchar al cliente {id_cliente}...")
        # TODO: Completado por estudiante
    
        try:
            while True:

                mensaje = self.recibir_mensaje(socket_cliente)
                
                if not mensaje:
                    raise ConnectionError

                respuesta = self.logica.procesar_mensaje(mensaje, socket_cliente)
                if respuesta:
                    self.enviar_mensaje(socket_cliente, respuesta)
                if respuesta["accion"] == "login" and respuesta["estado"] == "valido":
                    self.listos[id_cliente] = True
                    nombre = mensaje["nombre"]
                    dic = {"accion": "nombre_propio", "nombre": nombre}
                    self.enviar_mensaje(socket_cliente, dic)
                    if id_cliente == 1:
                        self.cliente_1_nombre = nombre
                        self.logica.nombre_1 = nombre
                        
                    else: 
                        self.cliente_2_nombre = nombre
                        self.logica.nombre_2 = nombre

                if self.listos[1] and self.listos[2] and not self.jugando:
                    self.jugando = True
                    dic = {"accion": "nombre_rival", "nombre": self.cliente_1_nombre}
                    self.enviar_mensaje(self.sockets[2], dic)
                    dic = {"accion": "nombre_rival", "nombre": self.cliente_2_nombre}
                    self.enviar_mensaje(self.sockets[1], dic)
                    self.log(f"Comenzando la partida, jugadores:" + 
                        f"{self.cliente_1_nombre} y {self.cliente_2_nombre}")
                    self.iniciar_juego()
                    


        except ConnectionError as error:
            print("error tipo : ", error)
            self.log(f"se ha cerrado la coneccion con {id_cliente}")
            self.jugando = False
            data = {"accion": "timer_espera","tiempo": data_json("TIMER_ESPERA")}
            data_2 = {"accion": "nombre_rival","nombre": "jugador 2"}
            if id_cliente == 1:
                self.cliente_1 = False
                self.listos[1] = False
                self.cliente_1_nombre = None
                self.logica.nombre_1 = None
                self.sockets[1] = None
                if self.cliente_2:
                    self.enviar_mensaje(self.sockets[2],data)
                    self.enviar_mensaje(self.sockets[2],data_2)
                print("cliente 1")
            else:
                self.cliente_2 = False
                self.listos[2] = False
                self.cliente_2_nombre= None
                self.logica.nombre_2 = None
                self.sockets[2] = None
                if self.cliente_1:
                    self.enviar_mensaje(self.sockets[1],data)
                    self.enviar_mensaje(self.sockets[1],data_2)
                print("cliente 2")
    
    
    def recibir_mensaje(self, socket_cliente):

        largo_bytes_mensaje = socket_cliente.recv(4)
        print("largo_bytes_mensaje", largo_bytes_mensaje)
        largo_mensaje = int.from_bytes(largo_bytes_mensaje, byteorder="big")
        mensaje_en_bytes = bytearray()

        while len(mensaje_en_bytes) < largo_mensaje:
            numero_bloque = socket_cliente.recv(4)
            print("numero bloque:", numero_bloque)
            recibir_chunk = socket_cliente.recv(64)
            print("recibir_chunk:", recibir_chunk)
            mensaje_en_bytes += recibir_chunk

        #print("desordenado: ",mensaje_en_bytes)
        bytes_limpios = mensaje_en_bytes.rstrip(b"\x00")
        #mensaje_ordenado = desencriptar(bytes_limpios)
        #print("ordenado: ", mensaje_ordenado)
        print("bytes_limpios: ",bytes_limpios)
        bytes_limpios = desencriptar(bytes_limpios)
        mensaje = self.decodificar(bytes_limpios)
        
        print("servidor recibe: ", mensaje)
        return mensaje

    def enviar_mensaje(self, socket_cliente, mensaje):

        print("servidor manda: ", mensaje)
        mensaje_bytes = self.codificar(mensaje)
        print("mensaje_butes", mensaje_bytes)
        mensaje_bytes = encriptar(mensaje_bytes)
        largo = len(mensaje_bytes)
        largo_bytes = largo.to_bytes(4, byteorder="big")
        print("largo_bytes", largo_bytes)
        bloques = largo // 32

        if bloques % 32 != 0 and bloques > 1:
            bloques += 1
        if bloques == 0:
            bloques = 1
        mensaje_enviar = bytearray(b"")

        for bloque in range(1, bloques + 1):
            mensaje_bloque = mensaje_bytes[64*(bloque - 1):bloque*64]
            while len(mensaje_bloque) % 64 !=0:
                mensaje_bloque += b"\x00"

            print("se agrega", bloque.to_bytes(4, byteorder="little") + mensaje_bloque )
            mensaje_enviar += bloque.to_bytes(4, byteorder="little") + mensaje_bloque         

        socket_cliente.send(largo_bytes + mensaje_enviar)
        print("mensaje_enviar:", largo_bytes + mensaje_enviar)
        
    def iniciar_juego(self):
        self.tiempo_restante = data_json("TIMER_ESPERA")

        self.actualizar_timer()

    def actualizar_timer(self):
        while True:
            sleep(1)
            self.tiempo_restante -= 1

            print(self.tiempo_restante)
            if self.tiempo_restante == -1:
                print("acabo el tiempo")
                dic = {"accion": "comenzar_juego"}
                self.enviar_mensaje(self.sockets[1], dic)
                self.enviar_mensaje(self.sockets[2], dic)
                break
            dic = {"accion": "timer_espera", "tiempo": self.tiempo_restante}
            self.enviar_mensaje(self.sockets[1], dic)
            self.enviar_mensaje(self.sockets[2], dic)
            

    def codificar(self, mensaje):
        try:
            mensaje_json = json.dumps(mensaje)
            mensaje_bytes = mensaje_json.encode()
            return mensaje_bytes
        except json.JSONDecodeError:
            print("mensaje de erro : ", mensaje)
            self.log("ERROR: No se pudo codificar el mensaje")
            return b""

    def decodificar(self, mensaje):
        try:
            mensaje = json.loads(mensaje)
            return mensaje

        except json.JSONDecodeError:
            self.log("Error: No se pudo decodificar el mensaje")

    def log(self, mensaje: str):
        """
        Imprime un mensaje en consola
        """
        print("|" + mensaje.center(80, " ") + "|")


if __name__ == "__main__":
    host = data_json("HOST")
    port = data_json("PORT")
    servidor = Servidor(port, host)
    while True:
        mensaje = input()
        servidor.enviar_mensaje(servidor.sockets[1], mensaje)
