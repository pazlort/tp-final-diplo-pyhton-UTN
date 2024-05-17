from tkinter import Tk
from vista import Ventana
from observer import ConcreteObservadorA

if __name__ == "__main__":
    master = Tk()
    ventana = Ventana(master)
    ConcreteObservadorA(ventana.crud)
    master.mainloop()