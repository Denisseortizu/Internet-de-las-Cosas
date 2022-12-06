
from datetime import datetime
from time import ctime
import time
import ntplib
import os
# AQUÍ VA EL CÓDIGO DE LA FUNCIÓN
# 1) Obtenemos el tiempo de un servidor
servidor_de_tiempo = "mx.pool.ntp.org"
cliente_ntp = ntplib.NTPClient()
respuesta = cliente_ntp.request(servidor_de_tiempo)
hora_Actual = datetime.strptime(time.ctime(respuesta.dest_time + respuesta.offset), "%a %b %d %H:%M:%S %Y")
#   Asignamos la hora actual al tiempo del Raspberry
comando_en_terminal = 'sudo date -s ' + '"' + str(hora_Actual) + '"'
os.system(comando_en_terminal)
