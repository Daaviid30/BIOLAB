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

    mensaje_estado = registro.registrar_usuario(dni, name, surname, email, phone, password, password2)
    return render_template('singup.html', msg=mensaje_estado[0], msg_class=mensaje_estado[1])


@app.route('/segundo_factor')
def segundo_factor():
    return render_template('segundo_factor.html')

@app.route('/form-2fa', methods=['POST'])
def form_2fa():
    codigo_verificacion = request.form['codigo']

    mensaje_estado = inicio_sesion.comprobar_codigo_verificación(codigo_verificacion)
    return render_template('segundo_factor.html', msg=mensaje_estado[0], msg_class=mensaje_estado[1])

@app.route('/principal')
def principal():
    titulos = papers.listar_papers()
    return render_template('principal.html', titulos=titulos)

@app.route('/form-principal', methods=['POST'])
def form_principal():
    titulo = request.form['titulo']
    cuerpo = request.form['cuerpo']

    mensaje, estado = papers.guardar_paper(titulo, cuerpo)
    titulos = papers.listar_papers()
    return render_template('principal.html', msg=mensaje, msg_class=estado, titulos=titulos)

@app.route('/paper', methods=['POST'])
def paper():
    titulo  = request.form['titulo']
    cuerpo, mensaje, estado = papers.recuperar_cuerpo(titulo)
    if not cuerpo:
        titulos = papers.listar_papers()
        return render_template('principal.html', msg=mensaje, msg_class=estado, titulos=titulos)
    return render_template('paper.html', titulo=titulo, cuerpo=cuerpo, msg=mensaje, msg_class=estado)

# Ejecución del programa
if __name__ == '__main__':
    app.run(debug=True)