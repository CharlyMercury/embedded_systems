import re  
import socket
import json
import sys  # Para salir del programa con sys.exit()

velocidad = re.compile(r"^-?\d+(\.\d+)?$")  
WELCOME_MESSAGE = """
     BIENVENIDO AL SISTEMA 'CONTROL DE MOTOR'
       Para detener el motor en cualquier momento del sistema, escribe STOP o stop.
       Para salir del programa completamente, escribe EXIT o exit.
"""

TURNING_DDIRECTION_MESSAGE = """
        Introduzca el sentido de giro del motor:
         1) CW o cw para giro sentido horario.
         2) CCW o ccw para giro sentido antihorario.
         3) STOP o stop para detener el motor.
         4) EXIT o exit para salir del programa.
""" 

print(WELCOME_MESSAGE)

def run_interface(): 
    
    while True: 
        while True:
            turning_direction = input(TURNING_DDIRECTION_MESSAGE) 
            if turning_direction.lower() == 'exit':
                print("Saliendo del programa...")
                sys.exit()
            if turning_direction.lower() in ['cw', 'ccw', 'stop']:
                break
            else:
                print('Introduzca un sentido de giro válido') 

        while True:
            if turning_direction.lower() == 'stop':
                user_velocity = 0
                break
            
            user_velocity = input("Introduce una velocidad válida [0, 1023] o escribe EXIT para salir: ")

            if user_velocity.lower() == 'exit':
                print("Saliendo del programa...")
                sys.exit()

            if user_velocity.lower() == 'stop':
                turning_direction = 'stop'
                user_velocity = 0
                break

            if velocidad.match(user_velocity):  
                user_velocity = float(user_velocity) 

                if 0 <= user_velocity <= 1024:
                    break  
                else:
                    print("Error: La velocidad no está dentro del rango permitido.")
            else:
                print("Error: Debes ingresar un número entero o decimal válido.")

        activation_commands_motor = {
            'direction': turning_direction.lower(),
            'velocity': user_velocity
        }

        print("Comando enviado:", activation_commands_motor)

        HOST = '192.168.18.182'  # IP del ESP32 o ESP8266
        PORT = 8080              # Puerto del servidor socket

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                s.send(json.dumps(activation_commands_motor).encode('utf-8'))

                # Respuesta del servidor
                response = s.recv(1024)
                print("Respuesta del servidor:", response.decode('utf-8'))

        except Exception as e:
            print("Error al conectar o enviar datos:", e)
