from flask import Flask, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Esto permite que React se conecte sin bloqueos

# --- CONFIGURACIÓN (Usa las mismas que en servidor.py) ---
SUPABASE_URL = "https://covankjypfgdvrjwugkk.supabase.co"
SUPABASE_KEY = "sb_publishable_VerEA5mBgIjzociVcn_x2w_JjkRbBXa"

@app.route('/api/datos', methods=['GET'])
def obtener_datos():
    """Endpoint que consulta Supabase y devuelve JSON"""
    url = f"{SUPABASE_URL}/rest/v1/registros_red?select=*"
    
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            datos = response.json()
            return jsonify(datos), 200
        else:
            return jsonify({"error": "No se pudo obtener datos"}), response.status_code
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Correrá en el puerto 5000 por defecto
    print("🌐 API corriendo en http://127.0.0.1:5000/api/datos")
    app.run(debug=True, port=5000)