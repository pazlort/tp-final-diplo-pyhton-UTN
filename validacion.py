import re
from mensajes import Mensajes


class Validar:
    def __init__(self):
        self.mensaje = Mensajes()

    def validando_mail(self, valor_a_validar):
        patron_mail = "([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+([A-Z|a-z]{2,})+"
        if re.match(patron_mail, valor_a_validar):
            return True
        else:
            self.mensaje.showinfo("No ingreso un mail valido")

    def campos_completos(self, *valores_a_validar):
        patron_completo = r"^\s*$"
        for valor in valores_a_validar:
            if valor == "Ingrese una especie":
                self.mensaje.showinfo("Todos los campos son obligatorios")
                return False
            if valor == "Ingrese el sexo":
                self.mensaje.showinfo("Todos los campos son obligatorios")
                return False
            if re.match(patron_completo, valor):
                self.mensaje.showinfo("Todos los campos son obligatorios")
                return False
        return True

    def valor_numerico(self, valor_a_validar, campo):
        patron_nro = r"[0-9]"
        if re.match(patron_nro, valor_a_validar):
            return True
        else:
            self.mensaje.showinfo(f"Debe ingresar un campo numerico en {campo} ")
