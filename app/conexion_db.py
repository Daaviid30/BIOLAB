import mysql.connector

# Datos de configuracion de la base de datos
configuracion = {
    'user':'root',
    'password':'',
    'host':'localhost',
    'port':'3306',
    'database':'biolab'
}

# Conectamos con la base de datos
conexion = mysql.connector.connect(**configuracion)

if conexion.is_connected():
    print("Se ha establecido conexión con la BBDD")
else:
    raise Exception("Error al conectarse")

# Si la conexión se establece creamos un cursor para realizar operaciones con la bbdd
cursor = conexion.cursor()