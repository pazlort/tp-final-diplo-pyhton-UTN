from tkinter import StringVar
from tkinter import Label
from tkinter import Entry
from tkinter import ttk
from tkinter import Button
from tkinter import OptionMenu
from modelo import Crud
from modelo import Complementos


from parametros import (
    letra,
    estilo,
    tamaño_title,
    tamaño_text,
    param_fg,
    param_bg,
    letra_boton,
    size_boton,
    color_boton,
)


class Ventana:
    def __init__(self, master):
        self.master = master
        self.crud = Crud()
        self.complementos = Complementos()

        self.complementos.try_connection()

        var_nombre_mascota = StringVar()
        var_edad = StringVar()
        var_color = StringVar()
        var_especie = StringVar(value="Ingrese una especie")
        var_raza = StringVar()
        var_sexo = StringVar(value="Ingrese el sexo")
        var_nombre_duenio = StringVar()
        var_mail = StringVar()
        var_telefono = StringVar()
        var_direccion = StringVar()
        var_ciudad = StringVar()

        # configuracion de la página
        self.master.attributes("-zoomed", True)
        self.master.attributes("-type", "splash")
        self.master.title("Historias clínicas veterinarias")
        self.master.configure(bg=param_bg)

        # treeview
        self.tree = ttk.Treeview(master, selectmode="browse", height=20)
        self.tree["columns"] = (
            "col1",
            "col2",
            "col3",
            "col4",
            "col5",
            "col6",
            "col7",
            "col8",
            "col9",
            "col10",
            "col11",
        )
        self.tree.pack(side="left", fill="both", expand=True)

        # scrollbar
        scrollbar = ttk.Scrollbar(master, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # creo todos los campos
        insert_text = self.formulario(
            "HISTORIA CLÍNICA", fonts=(letra, tamaño_title, estilo)
        )
        nombre_mascota = self.formulario("Nombre mascota: ")
        edad = self.formulario("Edad: ")
        color = self.formulario("Color: ")
        especie = self.formulario("Especie: ")
        raza = self.formulario("Raza: ")
        sexo = self.formulario("Sexo: ")
        nombre_duenio = self.formulario("Nombre dueño: ")
        mail = self.formulario("E-mail: ")
        telefono = self.formulario("Teléfono: ")
        direccion = self.formulario("Dirección: ")
        ciudad = self.formulario("Ciudad: ")

        lista_especies = ["Perro", "Gato", "Pajaro", "Tortuga", "Hamster", "Otro"]
        lista_sexo = ["Macho", "Hembra", "Ns/Nc"]

        entry_nombre_mascota = self.entrys(var_nombre_mascota)
        entry_edad = self.entrys(var_edad)
        entry_color = self.entrys(var_color)
        entry_especie = OptionMenu(master, var_especie, *lista_especies)
        entry_raza = self.entrys(var_raza)
        entry_sexo = OptionMenu(master, var_sexo, *lista_sexo)
        entry_nombre_duenio = self.entrys(var_nombre_duenio)
        entry_mail = self.entrys(var_mail)
        entry_telefono = self.entrys(var_telefono)
        entry_direccion = self.entrys(var_direccion)
        entry_ciudad = self.entrys(var_ciudad)

        # place
        nombre_mascota.place(x=150, y=50)
        edad.place(x=150, y=80)
        color.place(x=150, y=110)
        especie.place(x=150, y=140)
        raza.place(x=150, y=170)
        sexo.place(x=150, y=200)
        nombre_duenio.place(x=600, y=50)
        mail.place(x=600, y=80)
        telefono.place(x=600, y=110)
        direccion.place(x=600, y=140)
        ciudad.place(x=600, y=170)
        self.tree.place(x=0, y=300)

        entry_nombre_mascota.place(x=300, y=50)
        entry_edad.place(x=300, y=80)
        entry_color.place(x=300, y=110)
        entry_especie.place(x=300, y=140)
        entry_raza.place(x=300, y=170)
        entry_sexo.place(x=300, y=200)
        entry_nombre_duenio.place(x=750, y=50)
        entry_mail.place(x=750, y=80)
        entry_telefono.place(x=750, y=110)
        entry_direccion.place(x=750, y=140)
        entry_ciudad.place(x=750, y=170)
        insert_text.place(relx=0.5, y=20, anchor="center")

        self.armando_tree(50, 50, "Nro", 0)
        self.armando_tree(150, 150, "Nombre Mascota", 1)
        self.armando_tree(50, 50, "Edad", 2)
        self.armando_tree(75, 75, "Color", 3)
        self.armando_tree(100, 100, "Especie", 4)
        self.armando_tree(100, 100, "Raza", 5)
        self.armando_tree(100, 100, "Sexo", 6)
        self.armando_tree(150, 150, "Nombre del dueño", 7)
        self.armando_tree(200, 200, "E-mail", 8)
        self.armando_tree(100, 100, "Teléfono", 9)
        self.armando_tree(200, 200, "Dirección", 10)
        self.armando_tree(100, 100, "Ciudad", 11)
        self.complementos.update_tree(self.tree)

        # insertamos botones
        boton_alta = self.botones(
            "Alta",
            lambda: self.crud.alta(
                var_nombre_mascota.get(),
                var_edad.get(),
                var_color.get(),
                var_especie,
                var_raza.get(),
                var_sexo,
                var_nombre_duenio.get(),
                var_mail.get(),
                var_telefono.get(),
                var_direccion.get(),
                var_ciudad.get(),
                self.tree,
                entry_nombre_mascota,
                entry_edad,
                entry_color,
                entry_raza,
                entry_nombre_duenio,
                entry_mail,
                entry_telefono,
                entry_direccion,
                entry_ciudad,
            ),
            color_boton,
            letra_boton,
            size_boton,
        )
        boton_alta.place(x=200, y=240)
        boton_selecccionar = self.botones(
            "Seleccionar",
            lambda: self.crud.seleccionar(
                var_especie,
                var_sexo,
                entry_nombre_mascota,
                entry_edad,
                entry_color,
                entry_raza,
                entry_nombre_duenio,
                entry_mail,
                entry_telefono,
                entry_direccion,
                entry_ciudad,
                self.tree,
            ),
            color_boton,
            letra_boton,
            size_boton,
        )
        boton_selecccionar.place(x=350, y=240)
        boton_modificar = self.botones(
            "Modificar",
            lambda: self.crud.modificar(
                var_nombre_mascota.get(),
                var_edad.get(),
                var_color.get(),
                var_especie,
                var_raza.get(),
                var_sexo,
                var_nombre_duenio.get(),
                var_mail.get(),
                var_telefono.get(),
                var_direccion.get(),
                var_ciudad.get(),
                self.tree,
                entry_nombre_mascota,
                entry_edad,
                entry_color,
                entry_raza,
                entry_nombre_duenio,
                entry_mail,
                entry_telefono,
                entry_direccion,
                entry_ciudad,
            ),
            color_boton,
            letra_boton,
            size_boton,
        )
        boton_modificar.place(x=500, y=240)
        boton_baja = self.botones(
            "Eliminar",
            lambda: self.crud.baja(
                self.tree,
            ),
            color_boton,
            letra_boton,
            10,
        )
        boton_baja.place(x=650, y=240)
        boton_borrar = self.botones(
            "Vaciar campos",
            lambda: self.complementos.vaciar_campos(
                var_especie,
                var_sexo,
                entry_nombre_mascota,
                entry_edad,
                entry_color,
                entry_raza,
                entry_nombre_duenio,
                entry_mail,
                entry_telefono,
                entry_direccion,
                entry_ciudad,
            ),
            color_boton,
            letra_boton,
            size_boton,
        )
        boton_borrar.place(x=800, y=240)
        boton_atender = self.botones(
            "Atender",
            lambda: self.crud.atender(
                var_especie,
                var_sexo,
                entry_nombre_mascota,
                entry_edad,
                entry_color,
                entry_raza,
                entry_nombre_duenio,
                entry_mail,
                entry_telefono,
                entry_direccion,
                entry_ciudad,
                self.tree,
            ),
            color_boton,
            letra_boton,
            size_boton,
        )
        boton_atender.place(x=1050, y=240)
        boton_cerrar = self.botones("X", lambda: master.destroy(), "red", "Arial", 10)
        boton_cerrar.place(relx=1, y=20, anchor="e")

    def botones(
        self,
        text_button,
        funcion,
        param_color_boton,
        param_letra_boton,
        param_size_boton,
    ):
        return Button(
            self.master,
            text=text_button,
            command=funcion,
            bg=param_color_boton,
            font=(param_letra_boton, param_size_boton),
        )

    def armando_tree(self, nro_width, nro_minwidth, param_text, nro, nro_anchor="w"):
        if nro > 0:
            self.tree.column(
                "col" + str(nro),
                width=nro_width,
                minwidth=nro_minwidth,
                anchor=nro_anchor,
            )
            self.tree.heading("col" + str(nro), text=param_text)
        elif nro == 0:
            self.tree.column(
                "#0", width=nro_width, minwidth=nro_minwidth, anchor=nro_anchor
            )
            self.tree.heading("#0", text=param_text)

    def formulario(self, texto_label, fonts=(letra, tamaño_text, estilo)):
        return Label(
            self.master,
            text=texto_label,
            bg=param_bg,
            fg=param_fg,
            font=fonts,
        )

    def entrys(self, var_tkinter):
        return Entry(
            self.master,
            textvariable=var_tkinter,
        )
