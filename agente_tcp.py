import socket
import time
import os

def iniciar_agente_tcp():
    server_address = ('127.0.0.1', 12000)
    # Asegúrate de que el archivo esté en la misma carpeta que este script
    archivo_csv = "olist_orders_dataset.csv" 

    if not os.path.exists(archivo_csv):
        print(f"❌ Error: El archivo '{archivo_csv}' no existe en esta carpeta.")
        return

    try:
        print("📂 Abriendo CSV y preparando envío TCP...")
        with open(archivo_csv, 'r', encoding='utf-8') as file:
            # Saltamos la primera línea (los encabezados: order_id, customer_id, etc.)
            next(file) 
            
            for linea in file:
                try:
                    # Creamos el socket dentro del loop para abrir/cerrar conexión por cada envío
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.connect(server_address)
                    
                    mensaje = linea.strip()
                    if not mensaje:
                        continue # Salta líneas vacías
                        
                    sock.sendall(mensaje.encode('utf-8'))
                    print(f"[TCP] Enviado registro a la base de datos")
                    
                    sock.close()
                    # Tiempo de espera según la rúbrica para no saturar
                    time.sleep(1) 
                    
                except ConnectionRefusedError:
                    print("❌ Error: No se pudo conectar al servidor. ¿Está encendido?")
                    break # Detenemos si el servidor no responde
                    
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    iniciar_agente_tcp()