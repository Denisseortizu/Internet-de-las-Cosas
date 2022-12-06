"""
Internet de las Cosas

William Alejandro González Pérez 
Denisse Ortiz Ordaz
Diego Sisternes Duarte

Equipo 3
25/09/2022

Descripcion  : Programa que permite obtener la hora actual, la lectura de un sensor DHTxx y escribe los datos en un archivo log
Lenguaje     : Python version 3

Para que sea posible, tenemos una base de datos "datos", con una tabla "clima", con los siguientes datos:
    1.id            VARCHAR
    2.firma         VARCHAR
    3.latitud       DOUBLE
    4.longitud      DOUBLE
    5.fecha         DATE
    6.hora          TIME
    7.utc           VARCHAR
    8.variable      VARCHAR
    9.valor         FLOAT

Usuario de BD: mysql
Contraseña: 123

Falta agarrar variables hora y fecha del sistema operativo
"""

# Bibliotecas a utilizar
from ast import Str
from calendar import prmonth
from datetime import datetime
from time import ctime
import hashlib
import json
import ntplib
import os
import random
import sys
import time
import requests     # Manejo de tiempo
import mysql.connector as mysql
#Imports de Reconocimiento de Voz
import speech_recognition as sr
import pyaudio
import os
from gtts import gTTS
from playsound import playsound
import cv2
#Similarity

import csv
import random
#from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
#from nltk.stem.porter import PorterStemmer
caracteres = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890#$%&?¡"
#Wake-up word
wake= "cari"
#Preguntas parecidas
respuestas_predeterminadas = {
'qué debo hacer': 'Nada.',
'qué tengo que hacer': 'Nada.',
'qué debería de ver': 'Nada.',
'qué debería comer': 'Nada. ',
'qué hago': 'Nada. ',
'que como': 'Nada. ',
'qué veo': 'Nada.',
'debería estudiar para el examen': 'No me importa.',
'debería hacer la tarea o dormir en la pony': 'No me importa.',
'pasaré el examen': 'Si es con Mora, no lo creo.',
'podré pasar mis materias': 'Creo que no.',
'aprobaré el semestre': 'No lo creo.',
'pasaré la materia': 'Si es con Mora, no lo creo.',
'me casaré': 'No lo creo.',
'algún día me casaré': 'No.',
'me voy a graduar este año': 'Creo que no.',
'me podré graduar': 'No lo creo. ',
'me voy a graduar': 'Probablemente.',
'termino a mi novio': 'Sí.',
'termino a mi novia': 'Sí. ',
'lo perdono': 'Amiga date cuenta.',
'soy intolerante a la lactosa': 'No lo creo.',
'debería cerrar mis redes sociales': 'Si.',
'puedo dormir ahora': 'No.',
'debería tomarme una chela': 'Probablemente.',
}

#Definir respuestas random
respuestas_random = [
    "Tal vez algún día.",
    "Nada.",
    "Tampoco.",
    "Probablemente.",
    "No lo creo.",
    "Ninguno.",
    "Creo que no.",
    "No.",
    "Sí.",
    "Intenta preguntar de nuevo.",
]
respuestas = respuestas_predeterminadas.values()
respuestas = [str (item) for item in respuestas]

def algo(doc, texto):
    texto =[texto]
    tf = TfidfVectorizer(use_idf=True, sublinear_tf=True)
    tf_doc = tf.fit_transform(doc)
    tf_texto = tf.transform(texto)
    cosineSimilarities = cosine_similarity(tf_doc,tf_texto).flatten()
    related_docs_indices = cosineSimilarities.argsort()[:-2:-1]
    if (cosineSimilarities[related_docs_indices] > 0.7):
        ans = [respuestas[i] for i in related_docs_indices[:1]]
        return ans[0]
    else:
        print("Cari: ", random.choice(respuestas_random))

def speakText(text):
    if(text==None):
        tts= gTTS('No te escucho.', lang='es')
    
    else:
        tts= gTTS(text, lang='es')
    #n=random.randint(0, 100)
    #nombre =  'voz'+str(n)+'.mp3' 
    #playsound(nombre)
    tts.save("voz.mp3")
    os.system("mpg123 " + "voz.mp3")
    
def generar_cadena():
    cadena = ""
    for ciclo in range(1,10):
        cadena += random.choice(caracteres)
    return cadena

def sincronizacion_de_tiempo(): # Función para sincronización de tiempo
    fecha = datetime.date()
    hora = datetime.strftime("%H:%M:%S")
    return fecha, hora

def leer_posicion():    # Función para leer la posición
    # Valores fijos temporales (Sala "O")
    latitud = 19.721821
    longitud = -101.185778
    return latitud, longitud


def crear_firma():
    #Aplicamos un algoritmo de cifrado
    cadena = generar_cadena()
    firma = (hashlib.sha512(cadena.encode())).hexdigest()
    return firma

def crear_certificado(firma, hora): # Función para crear el certificado
    #Aplicamos un algoritmo de cifrado
    certificado = (hashlib.md5((firma + hora ).encode())).hexdigest()
    return certificado

def almacenamiento_local(id, firma, latitud, longitud, fecha, hora, utc, variable, valor): # Función para el Almacenamiento Local
    try: #Intentamos la conexión 
        conn = mysql.connect(
        host='127.0.0.1',
        user='mysql',
        passwd='123',
        db='datos'
        )
        print("Se connecto a la base de datos")
    except mysql.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
    # Get Cursor
    cur = conn.cursor()
    #6)Guardar los datos
    sql= 'INSERT INTO clima (id, firma, latitud, longitud, fecha, hora, utc, variable, valor) VALUES ("'+id+'", "'+ firma +'", "'+ str(latitud) +'", "'+ str(longitud) +'", "'+str(fecha)+'", "'+str(hora)+'", "'+utc+'", "'+variable+'", "'+ str(valor)+'" )'
    print("Sentencia de SQL: \n" + sql)
    cur.execute(sql)
    print("Objeto guardadooooo :)))))))))))))))))))))")
    conn.commit()
    conn.close()
    return True

def almacenamiento_remoto(id, certificado, latitud, longitud, fecha, hora, utc, variable, valor):    # Función para el Almacenamiento Remoto
    #login = "pedro"
    #password = "123"
    url_servidor = "http://10.27.34.104/clima_formulario/formulario2.php"
    print("\nEnviar los datos de un formulario:")
    print("Dirección y página que reciben los datos: "+ url_servidor)
    parametros = {'id': id, 'latitud': latitud, 'longitud': longitud, 'fecha': fecha, 'hora': hora, 'utc':utc, 'variable':variable, 'valor':valor, 'certificado': certificado}
    try:
        respuesta = requests.post(url_servidor, data = parametros)
    except requests.exceptions.RequestException as e:  
        raise SystemExit(e)
    
    return True 

def guardar(valor):
    # PROGRAMA PRINCIPAL
    print("\nINICIANDO SERVIDOR:")
    print("\nSincronización inicial de tiempo del dispositivo:")
    id = "microfono_01"
    variable = "voz"
    utc= "-5"
    fecha, hora = sincronizacion_de_tiempo()
    print("Fecha: ", fecha, " Hora: ", hora, " UTC: ", utc)
    registro = 0
    while True:
        registro+= 1
        print("\nRegistro: ", registro)
        #hora = leer_hora()
        latitud, longitud = leer_posicion()
        print("\tLeyendo Posición: Latitud = ", latitud, " Longitud: ", longitud)
        print("\tLeyendo Microfono = ", valor)
        firma = '4eae862335cd191d7115fc20d8c9da5291d9388bdf619e039827014355d7348acf9c009a8f15009b636ebd8b8de67dd754cb3b5bd82716717815065c1e2551c8'
        print("\tCreando Firma: ", firma)
        certificado = crear_certificado(firma, hora)
        print("\tCreando Certificado: ", certificado)
        if (almacenamiento_local(id, firma, latitud, longitud, fecha, hora, utc, variable, valor)):
            print("\tAlmacenamiento Local Exitoso!")
        else:
            print("\tFalló el Almacenamiento Local!")
        if (almacenamiento_remoto(id, certificado, latitud, longitud, fecha, hora, utc, variable, valor)):
            print("\tAlmacenamiento Remoto Exitoso!")
        else:
            print("\tFalló el Almacenamiento Remoto!")
        print("Esperando un tiempo...")
        time.sleep(10)      
    
    
#Reconocemos respuestas
voz= sr.Recognizer()
while True:
    
    print("\nEscuchando...")
    saludo = ""
    
    with sr.Microphone() as fuente:
        voz.adjust_for_ambient_noise(fuente)
        try:
            audio = voz.listen(fuente)
            saludo = voz.recognize_google(audio, language="es-MX")
            
        except sr.UnknownValueError:
            pass
        except sr.RequestError:
            pass
        except sr.WaitTimeoutError:
            pass
    print("\nUsuario : ", saludo)    
    if(wake in saludo):
        speakText('Dime.')
        texto=""
        respuesta=""
        with sr.Microphone() as fuente:
            voz.adjust_for_ambient_noise(fuente)
            try:
                audio = voz.listen(fuente)
                texto = voz.recognize_google(audio, language="es-MX")
                
            except sr.UnknownValueError:
                pass
            except sr.RequestError:
                pass
            except sr.WaitTimeoutError:
                pass
        print("\nUsuario : ", texto)
        if(texto==""):
            respuesta='No te escucho.'
        else:
            respuesta = algo(respuestas_predeterminadas, texto)
            guardar(texto)
        print("\nCari : ", respuesta)
        speakText(respuesta)    
   
    if saludo == "adiós" :
        speakText("Adiós.")
        break
