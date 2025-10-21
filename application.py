from flask import Flask, render_template, jsonify, request
import os # Sigue siendo útil para otras configuraciones de entorno si las necesitas

# Elastic Beanstalk buscará este objeto llamado 'application'
application = Flask(__name__)

@application.route('/')
def dashboard():
    """
    Sirve la página principal del panel.
    """
    # Esta plantilla HTML (index.html) contendrá tu panel.
    # Puedes pasarle datos directamente si los tienes aquí,
    # o el HTML puede estar completamente autocontenido o llamar a /api/sample_data.
    return render_template('index.html', title="Mi Panel Personalizado")

@application.route('/api/sample_data')
def get_sample_data():
    """
    Endpoint de API de ejemplo para obtener algunos datos.
    El frontend podría llamar a este endpoint.
    """
    # Puedes obtener parámetros de la solicitud si es necesario
    # Por ejemplo, si el frontend envía un parámetro 'type':
    # data_type = request.args.get('type', 'default')

    # Datos de ejemplo que la API podría devolver
    sample_data = {
        "message": "Hola desde la API de mi aplicación!",
        "items": [
            {"id": 1, "name": "Elemento A", "value": 100},
            {"id": 2, "name": "Elemento B", "value": 200},
            {"id": 3, "name": "Elemento C", "value": 300}
        ],
        "timestamp": __import__('datetime').datetime.utcnow().isoformat() + "Z" # Ejemplo de marca de tiempo UTC
    }
    
    # Aquí podrías añadir lógica para generar o recuperar los datos que realmente quieres mostrar
    # Por ejemplo, leer de un archivo, calcular algo, etc.
    
    return jsonify(sample_data)

# --- Archivos de ejemplo que necesitarías (no generados aquí pero para tu referencia) ---

# templates/index.html:
#   Debería tener la estructura de tu panel.
#   Podría usar JavaScript para:
#   1. Llamar a `/api/sample_data`
#   2. Recibir el JSON y actualizar el DOM para mostrar los datos.
#   O simplemente mostrar contenido estático o datos pasados desde la función dashboard().

# static/css/style.css:
#   Tus estilos para el panel.

# static/js/dashboard.js:
#   (Opcional, puedes poner el JS en index.html) Tu lógica de frontend si es necesaria.

# ------------------------------------------------------------------------------------

if __name__ == '__main__':
    # Esto es solo para desarrollo local, Elastic Beanstalk usará un servidor WSGI como Gunicorn.
    application.run(debug=True, host='0.0.0.0', port=5000)