"""Proyecto de criptografía
Autores: David Martín (100472099) / Iván Llorente (100472242)"""

#Importamos las librerias necesarias para la ejecución de la app
import inicio_sesion
import registro
import papers
from flask import Flask, request, render_template

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
    
    mensaje_estado = inicio_sesion.login_usuario(dni, password)
    return render_template('login.html', msg=mensaje_estado[0], msg_class=mensaje_estado[1])

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

    # La validación de datos se lleva a cabo en el fichero registro.py
    mensaje_estado = registro.registrar_usuario(dni, name, surname, email, phone, password, password2)
    return render_template('singup.html', msg=mensaje_estado[0], msg_class=mensaje_estado[1])

# La ruta segundo factor, al ser invocada redirige a la pagina segundo_factor.html
@app.route('/segundo_factor')
def segundo_factor():
    return render_template('segundo_factor.html')

# La siguiente ruta maneja los datos reccibidos desde la pantalla de 2FA
@app.route('/form-2fa', methods=['POST'])
def form_2fa():
    codigo_verificacion = request.form['codigo']

    # Los datos los maneja el fichero inicio_sesion.py
    mensaje_estado = inicio_sesion.comprobar_codigo_verificación(codigo_verificacion)
    return render_template('segundo_factor.html', msg=mensaje_estado[0], msg_class=mensaje_estado[1])

# Creamos la ruta principal que te redirigira a la pagina principal.html
@app.route('/principal')
def principal():
    # En esta pagina se mostraran los papers disponibles de este usuario
    # La obtencion de los titulos se da en el fichero papers.py
    titulos = papers.listar_papers()
    return render_template('principal.html', titulos=titulos)

# En esta ruta se procesan los datos de los nuevos papers introducidos
@app.route('/form-principal', methods=['POST'])
def form_principal():
    titulo = request.form['titulo']
    cuerpo = request.form['cuerpo']

    # El procesamiento de los datos introducidos es dado por el fichero papers.py
    mensaje, estado = papers.guardar_paper(titulo, cuerpo)
    titulos = papers.listar_papers()
    # Al introducir nuevos papers se redirige a la misma pagina pero con la lista de titulos actualizada
    return render_template('principal.html', msg=mensaje, msg_class=estado, titulos=titulos)

# Esta ruta muestra el paper seleccionado
@app.route('/paper', methods=['POST'])
def paper():
    titulo  = request.form['titulo']
    cuerpo, mensaje, estado = papers.recuperar_cuerpo(titulo)
    # Si no existe cuerpo en el paper, significa que no se pudo recuperar dicho paper, por lo que aparecera un 
    # mensaje de error
    if not cuerpo:
        titulos = papers.listar_papers()
        return render_template('principal.html', msg=mensaje, msg_class=estado, titulos=titulos)
    return render_template('paper.html', titulo=titulo, cuerpo=cuerpo, msg=mensaje, msg_class=estado)

# Ejecución del programa
if __name__ == '__main__':
    app.run(debug=True)