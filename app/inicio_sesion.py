import conexion_db
import correo_2FA
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

codigo_verificacion = None

def login_usuario(dni, password):
    global codigo_verificacion
    error = True

    # Consultamos los datos relevantes para el log-in en la base de datos
    consulta = "SELECT dni, salt, encryped_pass, email FROM usuarios WHERE dni = %s"
    values = (dni,)
    conexion_db.cursor.execute(consulta, values)
    # Guardamos los resultados de la consulta en una lista de tuplas (solo una tupla en este caso -> 1 coincidencia)
    resultados = conexion_db.cursor.fetchall()

    # Si la lista recibida de la consulta está vacía significará que no hay ningún usuario registrado con ese DNI.
    if len(resultados) == 0:
        respuesta = 'El usuario no tiene una cuenta activa en BioLab'
    # Si el usuario está registrado pasamos a comprobar si las contraseñas coinciden.
    else:
        # Recuperamos el salt para añadirselo a la contraseña introducida por el usuario
        salt = resultados[0][1]
        # Recuperamos la contraseña correcta del usuario para comprobarla con la introducida
        real_pass = resultados[0][2]
        # Convertimos la contraseña en bytes y utilizamos el método de derivacion Scrypt
        password = password.encode('utf-8')
        metodo = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)
        try:
            # Comparamos ambas contraseñas, si son iguales (.verify devuelve None) la contraseña es correcta
            metodo.verify(password, real_pass)
            respuesta = f"La contraseña es correcta, bienvenido usuario {dni}"
            error = False
            codigo_verificacion = correo_2FA.mandar_correo(resultados[0][3])
            return [respuesta, "acceso"]
        except:
            # Si ambas contraseñas no coinciden entonces saltará una excepción de cryptography
            respuesta = f"La contraseña es incorrecta"
    # Devolvemos un mensaje en la pagina de log-in, este varía dependiendo de si la contraseña es correcta o no
    if error == True:    
        return [respuesta, "error"]
    
def comprobar_codigo_verificación(codigo_introducido):
    global codigo_verificacion
    if str(codigo_introducido) == str(codigo_verificacion):
        respuesta = "Codigo de verificacion correcto"
        estado = "acceso"
    else:
        respuesta = "Código de verificacion incorrecto"
        estado = "error"
    return [respuesta, estado]
