import socket      # Para crear el socket de red
import time        # Para hacer pausas entre envíos
import os          # Para verificar si el archivo CSV existe

def iniciar_agente_tcp():
    """Agente que lee un CSV y envía cada línea al servidor via TCP"""
    
    # Dirección del servidor: IP local y puerto 12000
    server_address = ('127.0.0.1', 12000)
    
    # Nombre del archivo CSV con los datos de órdenes
    archivo_csv = "olist_orders_dataset.csv"

    # Verificamos que el archivo exista antes de continuar
    if not os.path.exists(archivo_csv):
        print(f"❌ Error: El archivo '{archivo_csv}' no existe en esta carpeta.")
        return

    try:
        print("📂 Abriendo CSV y preparando envío TCP...")
        with open(archivo_csv, 'r', encoding='utf-8') as file:
            
            # Saltamos la primera línea (encabezados del CSV)
            next(file)
            
            for linea in file:
                try:
                    # Creamos un nuevo socket TCP por cada registro enviado
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    
                    # Establecemos conexión con el servidor
                    sock.connect(server_address)
                    
                    # Limpiamos espacios y saltos de línea
                    mensaje = linea.strip()
                    
                    # Saltamos líneas vacías
                    if not mensaje:
                        continue
                    
                    # Enviamos el registro codificado en UTF-8
                    sock.sendall(mensaje.encode('utf-8'))
                    print(f"[TCP] Enviado registro a la base de datos")
                    
                    # Cerramos la conexión después de cada envío
                    sock.close()
                    
                    # Pausa de 1 segundo para simular tráfico real
                    time.sleep(1)
                    
                except ConnectionRefusedError:
                    print("❌ Error: No se pudo conectar al servidor. ¿Está encendido?")
                    break
                    
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

# Punto de entrada del programa
if __name__ == "__main__":
    iniciar_agente_tcp()