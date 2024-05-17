from database import Historiaclinica
from validacion import Validar
from mensajes import Mensajes
from fecha import dia, mes, anio, hora, minuto
from observer import Subject
from cliente import Cliente

import sys
import subprocess
import threading
from pathlib import Path
import os

BASE_DIR = os.path.dirname((os.path.abspath(__file__)))
ruta = os.path.join(BASE_DIR, "registro.txt")
archivo = open(ruta, "a")
diccionario = list()
theproc = ""


def aviso_alta(func):
    def inner(*args, **kwargs):
        global archivo
        registro_correcto = func(*args, **kwargs)
        if registro_correcto[0] == True:
            print("***Ingreso de nuevo registro correcto***")
            diccionario.append(
                {
                    "tipo_registro": "Alta",
                    "usuario": registro_correcto[1],
                    "fecha": dia + "/" + mes + "/" + anio + " " + hora + ":" + minuto,
                }
            )
            escribir = str(diccionario[len(diccionario) - 1])
            archivo.write(escribir)
            archivo.close()

    return inner


def aviso_baja(func):
    def inner(*args, **kwargs):
        global archivo
        registro_correcto = func(*args, **kwargs)
        if registro_correcto[0] == True:
            print("***Eliminación de registro correcto***")
            diccionario.append(
                {
                    "tipo_registro": "Baja",
                    "usuario": registro_correcto[1],
                    "fecha": dia + "/" + mes + "/" + anio + " " + hora + ":" + minuto,
                }
            )
            escribir = str(diccionario[len(diccionario) - 1])
            archivo.write(escribir)
            archivo.close()

    return inner


def aviso_actualizacion(func):
    def inner(*args, **kwargs):
        global archivo
        registro_correcto = func(*args, **kwargs)
        if registro_correcto[0] == True:
            print("***Actualización de registro correcto***")
            diccionario.append(
                {
                    "tipo_registro": "Modificación",
                    "usuario": registro_correcto[1],
                    "fecha": dia + "/" + mes + "/" + anio + " " + hora + ":" + minuto,
                }
            )
            escribir = str(diccionario[len(diccionario) - 1])
            archivo.write(escribir)
            archivo.close()

    return inner


class Crud(Subject):
    def __init__(self):
        self.complementos = Complementos()
        self.validar = Validar()
        self.mensaje = Mensajes()
        self.cliente = Cliente()

    @aviso_alta
    def alta(
        self,
        nombre_mascota,
        edad,
        color,
        especie,
        raza,
        sexo,
        nombre_duenio,
        mail,
        telefono,
        direccion,
        ciudad,
        tree,
        entry_nombre_mascota,
        entry_edad,
        entry_color,
        entry_raza,
        entry_nombre_duenio,
        entry_mail,
        entry_telefono,
        entry_direccion,
        entry_ciudad,
    ):
        if (
            self.validar.campos_completos(
                nombre_mascota,
                edad,
                color,
                especie.get(),
                raza,
                sexo.get(),
                nombre_duenio,
                mail,
                telefono,
                direccion,
                ciudad,
            )
            and self.validar.valor_numerico(edad, "EDAD")
            and self.validar.valor_numerico(telefono, "TELEFONO")
            and self.validar.validando_mail(mail)
        ):
            hc = Historiaclinica()
            hc.nombre_mascota = nombre_mascota
            hc.edad = edad
            hc.color = color
            hc.especie = especie.get()
            hc.raza = raza
            hc.sexo = sexo.get()
            hc.nombre_duenio = nombre_duenio
            hc.mail = mail
            hc.telefono = telefono
            hc.direccion = direccion
            hc.ciudad = ciudad
            hc.save()
            self.notificar(
                nombre_mascota,
                edad,
                especie.get(),
                nombre_duenio,
            )
            self.complementos.update_tree(tree)
            self.complementos.vaciar_campos(
                especie,
                sexo,
                entry_nombre_mascota,
                entry_edad,
                entry_color,
                entry_raza,
                entry_nombre_duenio,
                entry_mail,
                entry_telefono,
                entry_direccion,
                entry_ciudad,
            )
            self.mensaje.showinfo("Su historia clínica se dio de alta exitosamente")
            return [True, nombre_duenio]

    @aviso_actualizacion
    def modificar(
        self,
        par_nombre_mascota,
        par_edad,
        par_color,
        par_especie,
        par_raza,
        par_sexo,
        par_nombre_duenio,
        par_mail,
        par_telefono,
        par_direccion,
        par_ciudad,
        tree,
        entry_nombre_mascota,
        entry_edad,
        entry_color,
        entry_raza,
        entry_nombre_duenio,
        entry_mail,
        entry_telefono,
        entry_direccion,
        entry_ciudad,
    ):
        valor = tree.selection()
        item = tree.item(valor)
        mi_id = item["text"]
        if (
            mi_id
            and self.validar.campos_completos(
                par_nombre_mascota,
                par_edad,
                par_color,
                par_especie.get(),
                par_raza,
                par_sexo.get(),
                par_nombre_duenio,
                par_mail,
                par_telefono,
                par_direccion,
                par_ciudad,
            )
            and self.validar.valor_numerico(par_edad, "EDAD")
            and self.validar.valor_numerico(par_telefono, "TELEFONO")
        ):
            res = self.mensaje.askquestion(
                "Modificar historia clínica",
                "¿Está seguro que desea modificar esta historia clínica?",
            )

            if res == "yes":
                actualizar = Historiaclinica.update(
                    nombre_mascota=par_nombre_mascota,
                    edad=par_edad,
                    color=par_color,
                    especie=par_especie.get(),
                    raza=par_raza,
                    sexo=par_sexo.get(),
                    nombre_duenio=par_nombre_duenio,
                    mail=par_mail,
                    telefono=par_telefono,
                    direccion=par_direccion,
                    ciudad=par_ciudad,
                ).where(Historiaclinica.nro_historia_clinica == mi_id)
                actualizar.execute()
                self.complementos.update_tree(tree)
                self.complementos.vaciar_campos(
                    par_especie,
                    par_sexo,
                    entry_nombre_mascota,
                    entry_edad,
                    entry_color,
                    entry_raza,
                    entry_nombre_duenio,
                    entry_mail,
                    entry_telefono,
                    entry_direccion,
                    entry_ciudad,
                )
                return [True, par_nombre_duenio]
        elif not mi_id:
            self.mensaje.showinfo(
                "Por favor hacer click en una historia clínica del listado"
            )

    def seleccionar(
        self,
        especie,
        sexo,
        entry_nombre_mascota,
        entry_edad,
        entry_color,
        entry_raza,
        entry_nombre_duenio,
        entry_mail,
        entry_telefono,
        entry_direccion,
        entry_ciudad,
        tree,
    ):
        self.complementos.vaciar_campos(
            especie,
            sexo,
            entry_nombre_mascota,
            entry_edad,
            entry_color,
            entry_raza,
            entry_nombre_duenio,
            entry_mail,
            entry_telefono,
            entry_direccion,
            entry_ciudad,
        )
        valor = tree.selection()
        item = tree.item(valor)
        mi_id = item["text"]
        if mi_id:
            hc = Historiaclinica.get_by_id(mi_id)
            entry_nombre_mascota.insert(0, hc.nombre_mascota)
            entry_edad.insert(0, hc.edad)
            entry_color.insert(0, hc.color)
            especie.set(hc.especie)
            entry_raza.insert(0, hc.raza)
            sexo.set(hc.sexo)
            entry_nombre_duenio.insert(0, hc.nombre_duenio)
            entry_mail.insert(0, hc.mail)
            entry_telefono.insert(0, hc.telefono)
            entry_direccion.insert(0, hc.direccion)
            entry_ciudad.insert(0, hc.ciudad)
        else:
            self.mensaje.showinfo(
                "Por favor hacer click en una historia clínica del listado"
            )

    @aviso_baja
    def baja(
        self,
        tree,
    ):
        valor = tree.selection()
        item = tree.item(valor)
        mi_id = item["text"]
        if mi_id:
            hc = Historiaclinica.get_by_id(mi_id)
            res = self.mensaje.askquestion(
                "Eliminar historia clínica",
                "¿Está seguro que desea eliminar esta historia clínica?",
            )
            if res == "yes":
                borrar = Historiaclinica.get(
                    Historiaclinica.nro_historia_clinica == mi_id
                )
                borrar.delete_instance()
                tree.delete(valor)
                self.mensaje.showinfo("La historia clinica se borro con exito")
                return [True, hc.nombre_duenio]
        else:
            self.mensaje.showinfo("No seleccionó una historia clínica para eliminar")

    def atender(
        self,
        especie,
        sexo,
        entry_nombre_mascota,
        entry_edad,
        entry_color,
        entry_raza,
        entry_nombre_duenio,
        entry_mail,
        entry_telefono,
        entry_direccion,
        entry_ciudad,
        tree,
    ):
        self.complementos.vaciar_campos(
            especie,
            sexo,
            entry_nombre_mascota,
            entry_edad,
            entry_color,
            entry_raza,
            entry_nombre_duenio,
            entry_mail,
            entry_telefono,
            entry_direccion,
            entry_ciudad,
        )
        valor = tree.selection()
        item = tree.item(valor)
        mi_id = item["text"]
        if mi_id:
            hc = Historiaclinica.get_by_id(mi_id)
            ejecuto = self.cliente.start_cliente(
                mi_id,
                hc.nombre_mascota,
                hc.edad,
                hc.especie,
                hc.raza,
                hc.sexo,
                hc.nombre_duenio,
            )
            if ejecuto[0] == True:
                mensaje_cartel = f"El paciente {hc.nombre_mascota} (Historia Clinica nro: {mi_id}) sera atendido a la brevedad por {ejecuto[1]}"
                self.mensaje.showinfo(mensaje_cartel)
                self.complementos.stop_server()
                self.complementos.try_connection()
        else:
            self.mensaje.showinfo(
                "Por favor hacer click en la historia clínica del listado"
            )


class Complementos:
    def vaciar_campos(
        self,
        especie,
        sexo,
        entry_nombre_mascota,
        entry_edad,
        entry_color,
        entry_raza,
        entry_nombre_duenio,
        entry_mail,
        entry_telefono,
        entry_direccion,
        entry_ciudad,
    ):
        entry_nombre_mascota.delete(0, "end")
        entry_edad.delete(0, "end")
        entry_color.delete(0, "end")
        especie.set("Ingrese una especie")
        entry_raza.delete(0, "end")
        sexo.set("Ingrese el sexo")
        entry_nombre_duenio.delete(0, "end")
        entry_mail.delete(0, "end")
        entry_telefono.delete(0, "end")
        entry_direccion.delete(0, "end")
        entry_ciudad.delete(0, "end")

    def update_tree(self, tree):
        ids = tree.get_children()
        for i in ids:
            tree.delete(i)
        for row in Historiaclinica.select():
            tree.insert(
                "",
                0,
                text=row.nro_historia_clinica,
                values=(
                    row.nombre_mascota,
                    row.edad,
                    row.color,
                    row.especie,
                    row.raza,
                    row.sexo,
                    row.nombre_duenio,
                    row.mail,
                    row.telefono,
                    row.direccion,
                    row.ciudad,
                ),
            )

    def try_connection(
        self,
    ):
        if theproc != "":
            theproc.kill()
            threading.Thread(
                target=self.start_server, args=(True,), daemon=True
            ).start()
        else:
            threading.Thread(
                target=self.start_server, args=(True,), daemon=True
            ).start()

    def start_server(self, var):
        self.raiz = Path(__file__).resolve().parent
        the_path = os.path.join(self.raiz, "src", "server", "servidor.py")
        if var == True:
            global theproc
            theproc = subprocess.Popen([sys.executable, the_path])
            theproc.communicate()
        else:
            print("")

    def stop_server(
        self,
    ):
        global theproc
        if theproc != "":
            theproc.kill()
