from server import Servidor
from utils import data_json

if __name__ == "__main__":
    host = data_json("HOST")
    port = data_json("PORT")
    servidor = Servidor(port, host)
    while True:
        "hola"