import httplib
import urllib
import RPi.GPIO as GPIO
import Adafruit_DHT
import serial
import time
import datetime
arduino = serial.Serial("/dev/ttyACM0", 9600)
DHTSensor = Adafruit_DHT.DHT22
key = "9LXU79PY4TS2OPXX"
temp = 0
hum = 0
humid_rela = 0
time.sleep(2)
contador = 0
ki = 1.3
kp = 30
kd = 8
err = 0
err_1 = 0
ref = 37.5
Up = 0
Ui = 0
Ui_1 = 0
Ud = 0
U = 0
hora = 0
min = 0
sec = 0
GPIO_Pin = 4
Pin_bomba = 7
M2 = 8
VENT =5
GPIO.setmode(GPIO.BCM)
GPIO.setup(Pin_bomba, GPIO.OUT)
GPIO.setup(VENT, GPIO.OUT)
GPIO.setup(M2, GPIO.OUT)

while True:
    RR = datetime.datetime.now()
    hora = RR.hour
    min = RR.minute
    sec = RR.second
    humid, temper = Adafruit_DHT.read(DHTSensor, GPIO_Pin)
    if humid is not None and temper is not None:
        humid_rela = humid
        tempe_rela = temper
    temp = tempe_rela
    hum = humid_rela
    temp = float("{0:.2f}".format(temp))
    hum = float("{0:.2f}".format(hum))
    contador = contador + 1
#Control on-off Humedad
    if hum < 42:
        GPIO.output(Pin_bomba, GPIO.LOW)
        time.sleep(50)
        GPIO.output(Pin_bomba, GPIO.HIGH)
        time.sleep(200)
    else:
        GPIO.output(Pin_bomba, GPIO.HIGH)
#Control PID Temperatura
    err = ref - temp
    Up = kp * err
    Ui = (ki * err) + Ui_1
    if Ui > 128:
        Ui = 128
    if Ui < -128:
        Ui = -128
    Ud = kd * (err - err_1)
    U = Up + Ud + Ui
    Ui_1 = Ui
    if U > 128:
        U = 128
    if U < - 128:
        U = -128
    if U > 0:
        U = 128 - U
    if U < 0:
        U = U - 64
    U = abs(U)
    numero = U
    numero = str(int(numero))
#Configuracion de volteo
    if (hora == 15 or hora == 23 or hora == 7):
        if (min == 15 and sec < 12):
            GPIO.output(M2, GPIO.LOW)
            time.sleep(10)
            GPIO.output(M2, GPIO.HIGH)
        else:
            GPIO.output(M2, GPIO.HIGH)
    else:
        GPIO.output(M2, GPIO.HIGH)
    if contador == 1:
        arduino.write(numero)
    if contador == 2:
        h = str('2') + str(27.1)
        arduino.write(h)
        contador = 0
        print h
        err_1 = err
#Configuracion para la ventilacion
    if (min == 50 or min == 20):
        if sec < 10:
            GPIO.output(VENT, GPIO.LOW)
            time.sleep(5)
            GPIO.output(VENT, GPIO.HIGH)
        else:
            GPIO.output(VENT, GPIO.HIGH)
    elif (min == 5 or min == 35):
        if sec < 8:
            GPIO.output(VENT, GPIO.LOW)
            time.sleep(2)
            GPIO.output(VENT, GPIO.HIGH)
        else:
            GPIO.output(VENT, GPIO.HIGH)
    else:
        GPIO.output(VENT, GPIO.HIGH)
#Envio de datos a la aplicacion del thinkspeak
    params = urllib.urlencode({'field1': temp, 'key': key})
    headers = {"Content-typZZe": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    params2 = urllib.urlencode({'field2': hum, 'key': key})
    headers2 = {"Content-typZZe": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = httplib.HTTPConnection("api.thingspeak.com:80")
    conn2 = httplib.HTTPConnection("api.thingspeak.com:80")

    try:
        conn.request("POST", "/update", params, headers)
        conn2.request("POST", "/update", params2, headers2)
        response = conn.getresponse()
        response2 = conn2.getresponse()
        print response.status, response.reason
        data = response.read()
        conn.close()
        conn2.close()
    except:
        print "Fallo de conexion"
    temp=int(temp*10)
	hum=int(hum*10)
	print (temp,hum)
	print ('envio 1')
	arduino.write(str('a'))
	holaa=arduino.readline()
	print holaa
	print ('enviar AC')
	arduino.write(numero)
	holaa=arduino.readline()
	print holaa
	time.sleep(1)
	print ('envio 2')
	arduino.write(str('b'))
	holaa=arduino.readline()
	print holaa
	numero=str(hum)
	print ('enviar Humedad')
	arduino.write(numero)
	holaa=arduino.readline()
	print holaa
	print ('envio 3')
	arduino.write(str('c'))
	holaa=arduino.readline()
	print holaa
	numero=str(temp)
	print ('enviar Temperatura')
	arduino.write(numero)
	holaa=arduino.readline()
	print holaa
    time.sleep(1)
arduino.close()
