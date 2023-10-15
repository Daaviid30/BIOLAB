import mysql.connector

configuracion = {
    'user':'root',
    'password':'',
    'host':'localhost',
    'port':'3306',
    'database':'biolab'
}

conexion = mysql.connector.connect(**configuracion)

if conexion.is_connected():
    print("Se ha establecido conexión con la BBDD")
else:
    raise Exception("Error al conectarse")

cursor = conexion.cursor()