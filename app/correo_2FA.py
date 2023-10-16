import smtplib
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def mandar_correo(destinatario): 
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'biolabuc3m@gmail.com'
    smtp_password = 'wwxmtwykanpxgewp'

    codigo_verificacion = random.randint(10000,99999)
    subject = f'Codigo de verificacion BioLab: {codigo_verificacion}'
    mensaje = f"Para terminar de iniciar sesión es necesario completar este 2FA (segundo factor de autentificación), para ello introduzca el siguiente código de verificación:\n\n\t Codigo verificación: {codigo_verificacion} \n\n\nEquipo de BioLab"
    
    # Creamos el objeto del correo

    correo = MIMEMultipart()
    correo['From'] = smtp_username
    correo['To'] = destinatario
    correo['Subject'] = subject
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
    except Exception as e:
        print("No se pudo mandar el correo", str(e))
    


