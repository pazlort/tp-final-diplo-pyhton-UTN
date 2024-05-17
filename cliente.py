import socket
from mensajes import Mensajes

HOST, PORT = "localhost", 1024


class Cliente:
    def __init__(
        self,
    ):
        self.mensaje = Mensajes()
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def enviar_mensaje(self, mensaje):
        self.clientsocket.sendto(mensaje.encode("UTF-8"), (HOST, PORT))

    def start_cliente(
        self,
        mi_id,
        nombre_mascota,
        edad,
        especie,
        raza,
        sexo,
        nombre_duenio,
    ):
        try:
            self.enviar_mensaje(str(mi_id))
            self.enviar_mensaje(nombre_mascota)
            self.enviar_mensaje(str(edad))
            self.enviar_mensaje(especie)
            self.enviar_mensaje(raza)
            self.enviar_mensaje(sexo)
            self.enviar_mensaje(nombre_duenio)
            received = str(self.clientsocket.recv(1024), "utf-8")
            if received:
                return [True,received]

        except Exception as e:
            self.mensaje.showinfo("Hubo un error vuelve intentarlo")
