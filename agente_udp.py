import socket      # Para crear el socket de red
import time        # Para hacer pausas entre envíos
import random      # Para generar datos aleatorios de sensores

def iniciar_agente_udp():
    """Agente que simula un sensor enviando datos de temperatura via UDP"""
    
    # Dirección del servidor: IP local y puerto 12001
    server_address = ('127.0.0.1', 12001)
    
    # Creamos el socket UDP (SOCK_DGRAM = sin conexión, más rápido)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    print("📡 Agente UDP: Enviando telemetría a Supabase...")
    
    try:
        while True:
            # Generamos un valor aleatorio de temperatura entre 20.0 y 35.0 grados
            valor = random.uniform(20.0, 35.0)
            
            # Formateamos el mensaje con 2 decimales
            mensaje = f"Sensor_Data: {valor:.2f}°C"
            
            # Enviamos el paquete UDP sin necesidad de establecer conexión previa
            sock.sendto(mensaje.encode('utf-8'), server_address)
            
            print(f"[UDP] Enviado al servidor: {mensaje}")
            
            # Pausa de 2 segundos entre envíos para no saturar la base de datos
            time.sleep(2)
            
    except KeyboardInterrupt:
        # Si el usuario presiona Ctrl+C, detenemos el agente
        print("\n🛑 Agente UDP detenido por el usuario.")
    finally:
        # Cerramos el socket al terminar
        sock.close()

# Punto de entrada del programa
if __name__ == "__main__":
    iniciar_agente_udp()