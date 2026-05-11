import socket      # Para crear los sockets de red
import threading   # Para manejar múltiples clientes al mismo tiempo
import requests    # Para hacer peticiones HTTP a Supabase
import json        # Para convertir datos a formato JSON

# --- 1. CONFIGURACIÓN DE SUPABASE ---
# URL del proyecto en Supabase donde se guardarán los datos
SUPABASE_URL = "https://covankjypfgdvrjwugkk.supabase.co"
# Clave pública para autenticarnos con Supabase
SUPABASE_KEY = "sb_publishable_VerEA5mBgIjzociVcn_x2w_JjkRbBXa"

def guardar_en_db(ip, protocolo, mensaje):
    """Función que inserta un registro en la base de datos de Supabase"""
    
    # URL del endpoint REST de Supabase para la tabla registros_red
    url = f"{SUPABASE_URL}/rest/v1/registros_red"
    
    # Cabeceras necesarias para autenticación y formato de datos
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }
    
    # Datos que se insertarán en la base de datos
    payload = {
        "agente_ip": ip,        # IP del cliente que envió el dato
        "protocolo": protocolo,  # TCP o UDP
        "mensaje": mensaje       # Contenido del mensaje
    }
    
    try:
        # Enviamos el registro a Supabase mediante una petición POST
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        
        if response.status_code in [200, 201]:
            print(f"✅ [{protocolo}] Registro guardado en la nube: {mensaje[:30]}...")
        else:
            print(f"❌ Error API ({response.status_code}): {response.text}")
            
    except Exception as e:
        print(f"❌ Error de conexión con Supabase: {e}")

# --- 2. SERVIDOR TCP (Puerto 12000) ---
def servidor_tcp():
    """Función que escucha conexiones TCP en el puerto 12000"""
    
    # Creamos el socket TCP (SOCK_STREAM = orientado a conexión)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('0.0.0.0', 12000))  # Escucha en todas las interfaces
    sock.listen(5)                  # Acepta hasta 5 conexiones en cola
    print("🚀 Servidor TCP activo en puerto 12000 (CSV)")
    
    while True:
        try:
            # Esperamos una conexión entrante
            conn, addr = sock.accept()
            # Recibimos los datos del cliente
            data = conn.recv(2048).decode('utf-8')
            if data:
                # Guardamos el registro en Supabase
                guardar_en_db(str(addr[0]), 'TCP', data)
            conn.close()
        except Exception as e:
            print(f"⚠️ Error en flujo TCP: {e}")

# --- 3. SERVIDOR UDP (Puerto 12001) ---
def servidor_udp():
    """Función que escucha mensajes UDP en el puerto 12001"""
    
    # Creamos el socket UDP (SOCK_DGRAM = sin conexión)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', 12001))  # Escucha en todas las interfaces
    print("🚀 Servidor UDP activo en puerto 12001 (Sensores)")
    
    while True:
        try:
            # Recibimos el paquete UDP del cliente
            data, addr = sock.recvfrom(1024)
            mensaje = data.decode('utf-8')
            if mensaje:
                # Guardamos el registro en Supabase
                guardar_en_db(str(addr[0]), 'UDP', mensaje)
        except Exception as e:
            print(f"⚠️ Error en flujo UDP: {e}")

# --- 4. ARRANQUE DEL SISTEMA ---
if __name__ == "__main__":
    print("\n--- INICIANDO SISTEMA DE INGESTA DE DATOS ---")
    print("Conectando a:", SUPABASE_URL)
    
    # Creamos hilos separados para TCP y UDP funcionen al mismo tiempo (concurrencia)
    hilo_tcp = threading.Thread(target=servidor_tcp, daemon=True)
    hilo_udp = threading.Thread(target=servidor_udp, daemon=True)
    
    # Iniciamos ambos hilos
    hilo_tcp.start()
    hilo_udp.start()
    
    try:
        # Mantenemos el programa corriendo indefinidamente
        while True:
            pass
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido.")