import socket
import threading
import requests
import json

# --- 1. CONFIGURACIÓN DE SUPABASE (VÍA HTTP) ---
SUPABASE_URL = "https://covankjypfgdvrjwugkk.supabase.co"
# Pega aquí tu clave public/anon
SUPABASE_KEY = "sb_publishable_VerEA5mBgIjzociVcn_x2w_JjkRbBXa"

def guardar_en_db(ip, protocolo, mensaje):
    """Envía los datos a Supabase usando peticiones web (Puerto 443)"""
    url = f"{SUPABASE_URL}/rest/v1/registros_red"
    
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }
    
    payload = {
        "agente_ip": ip,
        "protocolo": protocolo,
        "mensaje": mensaje
    }
    
    try:
        # Usamos POST para insertar el nuevo registro
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        
        if response.status_code in [200, 201]:
            print(f"✅ [{protocolo}] Registro guardado en la nube: {mensaje[:30]}...")
        else:
            print(f"❌ Error API ({response.status_code}): {response.text}")
            
    except Exception as e:
        print(f"❌ Error de conexión con Supabase: {e}")

# --- 2. SERVIDOR TCP (Puerto 12000) ---
def servidor_tcp():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('0.0.0.0', 12000))
    sock.listen(5)
    print("🚀 Servidor TCP activo en puerto 12000 (CSV)")
    
    while True:
        try:
            conn, addr = sock.accept()
            data = conn.recv(2048).decode('utf-8')
            if data:
                guardar_en_db(str(addr[0]), 'TCP', data)
            conn.close()
        except Exception as e:
            print(f"⚠️ Error en flujo TCP: {e}")

# --- 3. SERVIDOR UDP (Puerto 12001) ---
def servidor_udp():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', 12001))
    print("🚀 Servidor UDP activo en puerto 12001 (Sensores)")
    
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            mensaje = data.decode('utf-8')
            if mensaje:
                guardar_en_db(str(addr[0]), 'UDP', mensaje)
        except Exception as e:
            print(f"⚠️ Error en flujo UDP: {e}")

# --- 4. ARRANQUE ---
if __name__ == "__main__":
    print("\n--- INICIANDO SISTEMA DE INGESTA DE DATOS ---")
    print("Conectando a:", SUPABASE_URL)
    
    # Iniciamos los hilos para que TCP y UDP funcionen al mismo tiempo
    hilo_tcp = threading.Thread(target=servidor_tcp, daemon=True)
    hilo_udp = threading.Thread(target=servidor_udp, daemon=True)
    
    hilo_tcp.start()
    hilo_udp.start()
    
    try:
        # Mantiene el script corriendo
        while True:
            pass
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido.")