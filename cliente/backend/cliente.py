"""
Modulo contiene implementación principal del cliente
"""
from PyQt5.QtCore import pyqtSignal, QObject
import socket
import json
from threading import Thread
from cripto import desencriptar, encriptar
from time import sleep

class Cliente(QObject):

    senal_manejar_mensaje = pyqtSignal(dict)
    senal_cerrar = pyqtSignal()

    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conectado = False
        self.iniciar_cliente()

    def iniciar_cliente(self):

        try:
            self.socket_cliente.connect((self.host, self.port))
            self.conectado = True
            self.comenzar_a_escuchar()
            #self.senal_mostrar_ventana_carga.emit()

        except ConnectionError as e:
            print(f"\n-ERROR: El servidor no está inicializado. {e}-")
        except ConnectionRefusedError as e:
            print(f"\n-ERROR: No se pudo conectar al servidor.{e}-")

    def comenzar_a_escuchar(self):

        thread = Thread(target=self.escuchar_servidor, daemon=True)
        thread.start()

    def escuchar_servidor(self):
        """
        Recibe mensajes constantes desde el servidor y responde.
        """
        try:
            while self.conectado:
                mensaje = self.recibir()
                if mensaje:
                    self.senal_manejar_mensaje.emit(mensaje)
        except ConnectionError as error:
            print("se deconecto del servidor por: ", error)
            print("Se cerrara el programa, probar iniciar todo denuevo")
            sleep(4)
            self.senal_cerrar.emit()

    def recibir(self):
        print("RECIBE MENSAJE")
        largo_bytes_mensaje = self.socket_cliente.recv(4)
        print("largo_bytes_msj:", largo_bytes_mensaje)
        largo_mensaje = int.from_bytes(largo_bytes_mensaje, byteorder="big")
        mensaje_en_bytes = bytearray()

        while len(mensaje_en_bytes) < largo_mensaje:
            numero_bloque = self.socket_cliente.recv(4)
            print("numero bloque:", numero_bloque)
            recibir_chunk = self.socket_cliente.recv(64)
            print("recibir_chunk:", recibir_chunk)
            mensaje_en_bytes += recibir_chunk
        
        #print("desordenado: ",mensaje_en_bytes)
        bytes_limpios = mensaje_en_bytes.rstrip(b"\x00")
        #mensaje_ordenado = desencriptar(bytes_limpios)
        #print("ordenado: ", mensaje_ordenado)
        mensaje = desencriptar(bytes_limpios)
        mensaje = self.decodificar(mensaje)
        print("cliente recibe:" , mensaje)
        return mensaje

    def enviar(self, mensaje):
        
        print("cliente manda:", mensaje)
        mensaje_bytes = self.codificar(mensaje)
        mensaje_bytes = encriptar(mensaje_bytes)
        print("encriptado: ", mensaje_bytes)
        largo = len(mensaje_bytes)
        largo_bytes = largo.to_bytes(4, byteorder="big")
        print("largo_bytes:", largo_bytes)
        bloques = largo // 32

        if bloques % 32 != 0 and bloques > 1:
            bloques += 1
        mensaje_enviar = bytearray(b"")

        for bloque in range(1, bloques + 1):
            mensaje_bloque = mensaje_bytes[64*(bloque - 1):bloque*64]
            while len(mensaje_bloque) % 64 !=0:
                mensaje_bloque += b"\x00"

            print("se agrega", bloque.to_bytes(4, byteorder="little") + mensaje_bloque )
            mensaje_enviar += bloque.to_bytes(4, byteorder="little") + mensaje_bloque 

        self.socket_cliente.send(largo_bytes + mensaje_enviar)
        print("mensaje_enviar:", largo_bytes + mensaje_enviar)

    def codificar(self, mensaje):
        try:
            mensaje_json = json.dumps(mensaje)
            mensaje_bytes = mensaje_json.encode()
            return mensaje_bytes
        except json.JSONDecodeError:
            print("ERROR: No se pudo codificar el mensaje")
            return b""

    def decodificar(self, mensaje):
        try:
            mensaje = json.loads(mensaje)
            return mensaje

        except json.JSONDecodeError:
            print("Error: No se pudo decodificar el mensaje")
