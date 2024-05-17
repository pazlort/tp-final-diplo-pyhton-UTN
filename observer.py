from mensajes import Mensajes
from fecha import dia, mes, anio, hora, minuto

import os

diccionario = list()


class Subject:
    observadores = []

    def agregar(self, obj):
        self.observadores.append(obj)

    def notificar(self, *args):
        for observador in self.observadores:
            observador.update(args)


class Observador:
    def update(self):
        raise NotImplementedError("Delegación de actualización")


class ConcreteObservadorA(Observador):
    def __init__(self, obj):
        self.observado_a = obj
        self.observado_a.agregar(self)
        self.mensaje = Mensajes()

    def update(self, *args):
        BASE_DIR = os.path.dirname((os.path.abspath(__file__)))
        ruta = os.path.join(BASE_DIR, "registroexoticos.txt")
        archivo = open(ruta, "a")
        nombre_mascota = args[0][0]
        edad = args[0][1]
        especie = args[0][2]
        nombre_duenio = args[0][3]

        if especie != "Gato" and especie != "Perro":
            diccionario.append(
                {
                    "nombre mascota": nombre_mascota,
                    "edad": edad,
                    "especie": especie,
                    "nombre_duenio": nombre_duenio,
                    "horario": dia + "/" + mes + "/" + anio + " " + hora + ":" + minuto,
                }
            )
            escribir = str(diccionario[len(diccionario) - 1])
            archivo.write(escribir)
            archivo.close()
            self.mensaje.showinfo(
                "¡Recuerde! Debe derivarlo con un veterinario especialido"
            )
