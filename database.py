from peewee import *
from mensajes import Mensajes

db = SqliteDatabase("db_tp_final.db")
mensaje = Mensajes()


class BaseModel(Model):
    class Meta:
        database = db


class Historiaclinica(BaseModel):
    nro_historia_clinica = AutoField(unique=True)
    nombre_mascota = CharField()
    edad = IntegerField()
    color = CharField()
    especie = CharField()
    raza = CharField()
    sexo = CharField()
    nombre_duenio = CharField()
    mail = CharField()
    telefono = IntegerField()
    direccion = TextField()
    ciudad = CharField()


try:
    db.connect()
    print("Conexión a la base de datos establecida correctamente.")
    db.create_tables([Historiaclinica])
except OperationalError as e:
    print(f"Error al conectar a la base de datos: {e}")
finally:
    db.close()
    print("Conexión a la base de datos cerrada correctamente.")
