import mysql.connector
import os
import conexion_db
from inicio_sesion import pasar_password, pasar_identificador
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305



def guardar_paper(titulo, cuerpo):
    password_key, identificador = pasar_password(), pasar_identificador()
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=333333)

    key = kdf.derive(password_key.encode('utf-8'))

    data = cuerpo.encode('utf-8')
    aad = titulo.encode('utf-8')
    chacha = ChaCha20Poly1305(key)
    nonce = os.urandom(12)

    encrypted_data = chacha.encrypt(nonce, data, aad)

    try:
        insertar_datos = "INSERT INTO papers (dni, titulo, cuerpo, salt, nonce) VALUES (%s, %s, %s, %s, %s)"
        values = (identificador, titulo, encrypted_data, salt, nonce)
        conexion_db.cursor.execute(insertar_datos, values)
        conexion_db.conexion.commit()
        mensaje = "El paper ha sido almacenado correctamente"
        return mensaje, "acceso"

    except:
        mensaje = "No se pudo guardar el paper"
        return mensaje, "error"

def listar_papers():
    identificador = pasar_identificador()
    consulta = "SELECT titulo FROM papers WHERE dni = %s"
    values = (identificador,)
    conexion_db.cursor.execute(consulta, values)
    resultados = conexion_db.cursor.fetchall()

    return resultados