from flask import Flask, jsonify  # Flask para crear la API web
from flask_cors import CORS        # CORS para permitir conexiones desde React
import requests                    # Para hacer peticiones HTTP a Supabase

# Inicializamos la aplicación Flask
app = Flask(__name__)

# Habilitamos CORS para que React pueda conectarse sin bloqueos
CORS(app)

# --- CONFIGURACIÓN DE SUPABASE ---
# URL del proyecto en Supabase
SUPABASE_URL = "https://covankjypfgdvrjwugkk.supabase.co"
# Clave pública para autenticarnos con Supabase
SUPABASE_KEY = "sb_publishable_VerEA5mBgIjzociVcn_x2w_JjkRbBXa"

@app.route('/api/datos', methods=['GET'])
def obtener_datos():
    """Endpoint que consulta todos los registros de Supabase y los devuelve en JSON"""
    
    # URL del endpoint REST de Supabase para seleccionar todos los registros
    url = f"{SUPABASE_URL}/rest/v1/registros_red?select=*"
    
    # Cabeceras necesarias para autenticación
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}"
    }
    
    try:
        # Hacemos la petición GET a Supabase
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            # Si la petición fue exitosa, devolvemos los datos en formato JSON
            datos = response.json()
            return jsonify(datos), 200
        else:
            # Si hubo un error, devolvemos el código de error
            return jsonify({"error": "No se pudo obtener datos"}), response.status_code
            
    except Exception as e:
        # Si hubo un error de conexión, lo devolvemos
        return jsonify({"error": str(e)}), 500

# Punto de entrada del programa
if __name__ == "__main__":
    print("🌐 API corriendo en http://127.0.0.1:5000/api/datos")
    # Iniciamos el servidor Flask en modo debug en el puerto 5000
    app.run(debug=True, port=5000)