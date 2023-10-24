import smtplib
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Creamos la funcion que mandará un correo a aquellos que inicien sesión de forma exitosa, para el 2FA
def mandar_correo(destinatario):
    # Configuramos el servicio smtp, indicando el servidor de google y nuestro correo ademas de contraseña
    # exclusiva de esta app
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'biolabuc3m@gmail.com'
    smtp_password = 'wwxmtwykanpxgewp'

    # Generamos un codigo de verificacion que será un nuemro random de 5 cifras
    codigo_verificacion = random.randint(10000,99999)
    # Creamos asunto y cuerpo del email
    subject = f'Codigo de verificacion BioLab: {codigo_verificacion}'
    mensaje = f"Para terminar de iniciar sesión es necesario completar este 2FA (segundo factor de autentificación), para ello introduzca el siguiente código de verificación:\n\n\t Codigo verificación: {codigo_verificacion} \n\n\nEquipo de BioLab"
    
    # Creamos el objeto del correo
    correo = MIMEMultipart()
    correo['From'] = smtp_username
    correo['To'] = destinatario
    correo['Subject'] = subject
    # Adjuntamos el cuerpo al correo
    correo.attach(MIMEText(mensaje, 'plain'))

    # Establecemos conexión con servidor SMTP
    try:
        servidor = smtplib.SMTP(smtp_server, smtp_port)
        servidor.starttls() # activamos tls
        servidor.login(smtp_username, smtp_password)

        # enviamos correo electronico
        servidor.sendmail(smtp_username, destinatario, correo.as_string())

        # cerramos servidor
        servidor.quit()
        return codigo_verificacion
    
    except Exception as e:
        print("No se pudo mandar el correo", str(e))
    


