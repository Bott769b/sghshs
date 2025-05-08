from flask import Flask, request, send_file
import datetime
import logging
import requests

app = Flask(__name__)

# Konfigurasi logging
logging.basicConfig(filename='log_pelacakan_email.log', level=logging.INFO)

# Fungsi untuk mendapatkan lokasi dari IP
def get_lokasi(ip):
    try:
        response = requests.get(f"https://ipapi.co/{ip}/json/")
        return response.json()
    except:
        return {"error": "Gagal mendapatkan lokasi"}

# Route untuk pixel pelacakan
@app.route('/track/<kode_unik>.png')
def track(kode_unik):
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    waktu_akses = datetime.datetime.now()
    lokasi = get_lokasi(ip)

    data_log = {
        'kode_unik': kode_unik,
        'waktu': str(waktu_akses),
        'ip': ip,
        'user_agent': user_agent,
        'lokasi': lokasi
    }

    logging.info(data_log)

    # Kirimkan gambar transparan 1x1
    return send_file('pixel.png', mimetype='image/png')

# Jalankan server lokal
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
