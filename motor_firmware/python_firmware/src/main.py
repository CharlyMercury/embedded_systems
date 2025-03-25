"""

    Programa para el control en lazo abierto de un motor DC con un driver L298N.

"""
import json
import socket
import network
from machine import Pin, PWM
import time

# Configuración de los pines para la dirección del motor
motor_in1 = Pin(26, Pin.OUT)
motor_in2 = Pin(27, Pin.OUT)

# Configuración del PWM para el control de velocidad
motor_pwm = PWM(Pin(14), freq=1000, duty=0)


def stop_motor():
    """
        Función para detener el motor
        desativando el pwm y los pines de dirección.
    """
    motor_pwm.duty(0)
    motor_in1.off()
    motor_in2.off()


def cw_motor(velocidad=512):
    """
        Función para mover el motor en sentido horario
        con una velocidad dada.
    """
    motor_in1.on()
    motor_in2.off()
    motor_pwm.duty(velocidad)


def ccw_motor(velocidad=512):
    """
        Función para mover el motor en sentido antihorario
        con una velocidad dada.
    """
    motor_in1.off()
    motor_in2.on()
    motor_pwm.duty(velocidad)


def setup_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Conectando a red...')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
    print('Conectado:', wlan.ifconfig())


setup_wifi('Totalplay-2.4G-fee0', 'UUuQkjdK56LGPyjX')

# Configuración del socket
addr = socket.getaddrinfo('0.0.0.0', 8080)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

print("Esperando conexiones en puerto 8080...")

while True:
    cl, addr = s.accept()
    print('Cliente conectado desde', addr)
    try:
        data = cl.recv(1024)
        if data:
            print("Recibido:", data)
            try:
                comando = json.loads(data.decode('utf-8'))
                direction = comando.get("direction")
                velocidad = int(comando.get("velocity", 512))

                if direction == "cw":
                    print("Motor horario")
                    cw_motor(velocidad)
                elif direction == "ccw":
                    print("Motor antihorario")
                    ccw_motor(velocidad)
                elif direction == "stop":
                    print("Deteniendo motor")
                    stop_motor()
                else:
                    print("Comando no reconocido:", direction)
            except Exception as e:
                print("Error al procesar el comando:", e)
            cl.send("Comando ejecutado correctamente".encode('utf-8'))
    finally:
        cl.close()