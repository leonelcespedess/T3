"""
Módulo principal del cliente.
"""
import sys
from os.path import join
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from backend.cliente import Cliente
from backend.interfaz import Interfaz
from frontend.lobby import Lobby
from frontend.sala_espera import SalaDeEspera
from frontend.pestaña_juego import PestañaJuego
from utils import data_json

if __name__ == "__main__":
    HOST = data_json("HOST")
    PORT = data_json("PORT")
    try:
        # =========> Instanciamos la APP <==========
        app = QApplication(sys.argv)
        #app.setWindowIcon(QIcon(RUTA_ICONO))

        # =========> Iniciamos el cliente <==========
        cliente = Cliente(HOST, PORT)
        lobby = Lobby()
        interfaz = Interfaz()
        sala_espera = SalaDeEspera()
        pestaña_juego = PestañaJuego()

        # =========> Conectamos señales <==========
        # Cliente

        cliente.senal_manejar_mensaje.connect(interfaz.manejar_mensaje)
        cliente.senal_cerrar.connect(app.exit)

        #Lobby
        lobby.senal_enviar_usuario.connect(cliente.enviar)
        lobby.senal_cambio.connect(sala_espera.abrir)
        
        #interfaz
        interfaz.senal_log.connect(lobby.validacion_login)
        interfaz.senal_actualizar_nombre.connect(sala_espera.actualizar_nombre)
        interfaz.senal_actualizar_nombre_rival.connect(sala_espera.actualizar_nombre_rival)
        interfaz.senal_sala_espera.connect(sala_espera.abrir)
        interfaz.senal_tiempo_espera.connect(sala_espera.actualizar_datos)
        interfaz.senal_comenzar_juego.connect(sala_espera.cerrar)
        interfaz.senal_comenzar_juego.connect(pestaña_juego.abrir)

        

        sys.exit(app.exec_())
        
    except ConnectionError as e:
        print("Ocurrió un error.", e)
    except KeyboardInterrupt:
        print("\nCerrando cliente...")
        cliente.salir()
        sys.exit()
