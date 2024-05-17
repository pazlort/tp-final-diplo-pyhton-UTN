from tkinter import messagebox


class Mensajes:
    def showinfo(self, mensaje):
        return messagebox.showinfo(
            message=mensaje, title="Historias Clinicas Veterinarias"
        )

    def askquestion(self, mensaje1, mensaje2):
        return messagebox.askquestion(mensaje1, mensaje2)
