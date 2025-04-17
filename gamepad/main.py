import pygame
import serial
import time
from pygame.locals import *

# Inicializar pygame
pygame.init()

# Inicializar el joystick
pygame.joystick.init()

arduino_port = 'COM5' 
baud_rate = 115200

serial_connection = serial.Serial(arduino_port, baud_rate, timeout=1)

# Comprobar si hay joysticks conectados
if pygame.joystick.get_count() == 0:
    print("No se detectaron joysticks.")
else:
    # Conectar al primer joystick
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Joystick conectado: {joystick.get_name()}")

    # Bucle principal
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == JOYBUTTONDOWN:
                print(f"Botón {event.button} presionado.")
            elif event.type == JOYBUTTONUP:
                print(f"Botón {event.button} liberado.")
            elif event.type == JOYAXISMOTION:
                if event.axis == 0:
                    angle = (event.value+1)*45
                    serial_connection.write(angle.encode())
                    time.sleep(0.1)  # Give some time for Arduino to process
                    response = serial_connection.readline().decode('utf-8').strip()
                    print(angle)
                #print(f"Eje {event.axis} movido a {event.value:.2f}")

# Salir de pygame
pygame.quit()
