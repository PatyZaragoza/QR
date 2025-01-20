from flask import Flask, jsonify, request
import qrcode
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Configuración de la base de datos
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Tu usuario
        password="Zaragoza18",  # Tu contraseña
        database="axius"  # Tu base de datos
    )

@app.route('/generar_qr', methods=['POST'])
def generar_qr():
    try:
        data = request.get_json()
        email = data.get('email')

        if not email:
            return jsonify({'error': 'El email es obligatorio'}), 400

        # Generar el código QR
        qr = qrcode.make(email)
        qr_path = f"qr_codes/{email}_qr.png"
        qr.save(qr_path)

        # Guardar en la base de datos
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO qr_codes (email, qr_path) VALUES (%s, %s)", (email, qr_path))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'QR generado y guardado correctamente', 'qr_path': qr_path}), 201

    except Error as e:
        return jsonify({'error': f'Error en la base de datos: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
