import socket
import time
import random

def iniciar_agente_udp():
    # Asegúrate de que el puerto sea el 12001 para que coincida con el servidor
    server_address = ('127.0.0.1', 12001)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    print("📡 Agente UDP: Enviando telemetría a Supabase...")
    
    try:
        while True:
            # Simulamos datos de un sensor (Temperatura entre 20.0 y 35.0)
            valor = random.uniform(20.0, 35.0)
            mensaje = f"Sensor_Data: {valor:.2f}°C"
            
            # UDP envía el paquete sin necesidad de establecer una conexión previa
            sock.sendto(mensaje.encode('utf-8'), server_address)
            
            print(f"[UDP] Enviado al servidor: {mensaje}")
            
            # Esperamos 2 segundos para no saturar la base de datos (puedes bajarlo si quieres)
            time.sleep(2) 
            
    except KeyboardInterrupt:
        print("\n🛑 Agente UDP detenido por el usuario.")
    finally:
        sock.close()

if __name__ == "__main__":
    iniciar_agente_udp()