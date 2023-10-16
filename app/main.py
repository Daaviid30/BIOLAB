"""Proyecto de criptografía
Autores: David Martín (100472099) / Iván Llorente (100472242)"""

#Importamos las librerias necesarias para la ejecución de la app
import os
import re
import conexion_db
import correo_2FA
from flask import Flask, request, render_template
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

# Creamos la aplicación Flask
app = Flask(__name__)

# La ruta de inicio de la app será la pagina de log-in
@app.route('/')
def inicio():
    return render_template('login.html')

# La ruta /formulario dentro de la app llevará al manejo de datos del panel de log-in
@app.route('/formulario', methods=['POST'])
def procesar():
    dni = request.form['DNI']
    password = request.form['password']
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
            correo_2FA.mandar_correo(resultados[0][3])
            return render_template('login.html', msg=respuesta, msg_class="acceso")
        except:
            # Si ambas contraseñas no coinciden entonces saltará una excepción de cryptography
            respuesta = f"La contraseña es incorrecta"
    # Devolvemos un mensaje en la pagina de log-in, este varía dependiendo de si la contraseña es correcta o no
    if error == True:    
        return render_template('login.html', msg=respuesta, msg_class="error")

# La ruta /sing-up te lleva a la pagina de sing-up
@app.route('/sing-up')
def sing_up():
    return render_template('singup.html')


# La ruta /form-singup maneja los datos del formulario de registro
@app.route('/form-singup', methods=['POST'])
def form_singup():
    dni = request.form['DNI']
    name = request.form['name']
    surname = request.form['surname']
    email = request.form['email']
    phone = request.form['phone']
    password = request.form['password']
    password2 = request.form['password2']
    error = True

    # Realizamos varias comprobaciones para que la inserccion de datos en la bbdd sea correcta
    if not (re.match('^[0-9]{8}[A-Z]$', dni)):
        respuesta = 'El DNI debe tener 8 dígitos y una letra mayuscula'
    
    elif len(name) > 30:
        respuesta = 'El nombre no puede superar los 30 carácteres'

    elif len(surname) > 100:
        respuesta = 'Los apellidos no pueden superar los 100 carácteres'

    elif len(email) > 150:
        respuesta = 'El email no puede tener mas de 150 carácteres'

    elif not(re.match('^[0-9]{9}$', phone)):
        respuesta = 'El teléfono está formado por 9 dígitos'

    # Utilizamos una expresión regular para indicar que la password debe de tener minimo: una mayúscala
    # una minúscula y un dígito, ademas debe tener al menos 10 carácteres
    elif not(re.search(r'([A-Z]|[a-z]|[0-9])', password)) or len(password) < 8:
        respuesta = 'La contraseña debe de ser de 8 caracteres mínimo y debe tener una mayúscula, una minúscula y un digito.'

    # Realizamos una comprobación para que el usuario se asegure de insertar bien la contraseña
    elif password != password2:
        respuesta = 'Las contraseñas introducidas no coinciden'
    
    else:
        consulta = "SELECT dni FROM usuarios WHERE dni = %s"
        values = (dni,)
        conexion_db.cursor.execute(consulta, values)
        # Guardamos los resultados de la consulta en una lista de tuplas (solo una tupla en este caso -> 1 coincidencia)
        resultados = conexion_db.cursor.fetchall()
        # En caso de que ya exista el usuario no guardamos en la bbdd
        if len(resultados) != 0:
            respuesta = "Ya existe un usuario con ese DNI registrado"
            return render_template('singup.html', msg=respuesta, msg_class="error")
        # Una vez que todos los datos son correctos, procedemos a su insercción en la base de datos
        # Encriptamos la contraseña para almacenarla de forma segura en la bbdd
        # Generamos un salt en forma de bytes aleatorio para cada contraseña
        salt = os.urandom(16)
        # Transformamos a bytes la contraseña pasada por el formulario
        password = password.encode('utf-8')
        # Utilizamos el método de encriptación Scrypt
        metodo = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)
        encryped_password = metodo.derive(password)

        # Insertamos todos los datos en la bbdd, utilizando %s para evitar inyecciones SQL.
        query = "INSERT INTO usuarios (dni, nombre, apellidos, email, telefono, salt, encryped_pass) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (dni, name, surname, email, phone, salt, encryped_password)

        conexion_db.cursor.execute(query, values)
        conexion_db.conexion.commit()
        respuesta = "El usuario ha sido creado correctamente"
        error = False
        return render_template('singup.html', msg=respuesta, msg_class="acceso")
        

    # Mostramos el mensaje correspondiente según se haya dado una respuesta u otra.
    if error == True:
        return render_template('singup.html', msg=respuesta, msg_class="error")

# Ejecución del programa
if __name__ == '__main__':
    app.run(debug=True)