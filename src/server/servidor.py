from datetime import datetime
import socketserver
import os


datos_atendidos = []
BASE_DIR = os.path.dirname((os.path.abspath(__file__)))
ruta = os.path.join(BASE_DIR, "atendidos.txt")
archivo = open(ruta, "a")
diccionario = list()

# mejorar vista de tree y pantalla


class MyUDPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        socket = self.request[1]
        mensaje = self.request[0].strip()
        datos_ingresados = mensaje.decode("UTF-8")
        datos_atendidos.append(datos_ingresados)
        if len(datos_atendidos) == 6:
            data = input("ingrese su apellido: ")
            socket.sendto(data.encode("UTF-8"), self.client_address)
            datos_atendidos.append(data)
            anio = str(datetime.today().year)
            mes = str(datetime.today().month)
            dia = str(datetime.today().day)
            hora = str(datetime.today().hour)
            minuto = str(datetime.today().minute)
            diccionario.append(
                {
                    "historia clinica": datos_atendidos[0],
                    "nombre mascota": datos_atendidos[1],
                    "edad": datos_atendidos[2],
                    "especie": datos_atendidos[3],
                    "raza": datos_atendidos[4],
                    "sexo": datos_atendidos[5],
                    "fecha": dia + "/" + mes + "/" + anio + " " + hora + ":" + minuto,
                    "atendido por: ": datos_atendidos[6],
                }
            )
            escribir = str(diccionario[len(diccionario) - 1])
            archivo.write(escribir)
            archivo.close()


if __name__ == "__main__":
    # 192.168.1.04
    HOST, PORT_ASISTENTE = "localhost", 1024

    with socketserver.UDPServer((HOST, PORT_ASISTENTE), MyUDPHandler) as server:
        server.serve_forever()
