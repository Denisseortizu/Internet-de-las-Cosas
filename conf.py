from ast import Str
from calendar import prmonth
from datetime import datetime
from time import ctime
import ntplib


## Obtenemos el tiempo de un servidor
servidor_de_tiempo = "mx.pool.ntp.org"
now = datetime.now()

print("\nObteniendo la hora del servidor NTP:")

cliente_ntp = ntplib.NTPClient()
respuesta = cliente_ntp.request(servidor_de_tiempo)
hora_Servidor = datetime.strptime(ctime(respuesta.tx_time), "%a %b %d %H:%M:%S %Y")
#print("EL tiempo del detino es "+ str(respuesta.dest_time) +", el tiempo de diferencia es "+ str(respuesta.offset) +", Si lo sumamos es : "+ str(respuesta.offset+respuesta.dest_time))
#print("El tiempo del servidor es ="+ str(respuesta.tx_time) +" y el tiempo de retraso es ="+ str(respuesta.delay) +"Si lo sumamos y dividimos será= "+ str(respuesta.tx_time + (respuesta.delay)/2))
hora_Actual = datetime.strptime(ctime(respuesta.dest_time + respuesta.offset), "%a %b %d %H:%M:%S %Y")
print("Respuesta de " + servidor_de_tiempo +  ": " + str(hora_Servidor) + "\n")
print("Respuesta de tiempo actual: " + str(hora_Actual) + "\n")
#El programa cliente deberá imprimir en pantalla lo siguiente:

#    Tiempo actual de la computadora antes del ajuste (Reloj Cliente).
print("El tiempo actual(antes del ajuste):  " + datetime.now().strftime( "%a %b %d %H:%M:%S %Y") )

#    Tiempo de inicio antes de la petición (t1).
print("Tiempo Inicial de la petición:  " + str(datetime.strptime(ctime(respuesta.orig_time), "%a %b %d %H:%M:%S %Y")))

#    Tiempo que envió el servidor (Reloj Servidor).
print("Tiempo del servidor:  " + str(hora_Servidor) )

#    Tiempo de llegada de la petición (t2).
print("Tiempo de llegada de la petición (t2):  "+  str(datetime.strptime(ctime(respuesta.recv_time ), "%a %b %d %H:%M:%S %Y")))

#    Tiempo de atraso ( ( t2 - t1 ) / 2 )
print("Tiempo de atraso ( ( t2 - t1 ) / 2 ):  "+ str(respuesta.offset))

#    Tiempo actual de la computadora después del ajuste (Reloj Cliente = Reloj Servidor + ( ( t2 - t1 ) / 2 )).
print("El tiempo actual(despues del ajuste):  "+ str(hora_Actual) )



