from flask import Flask, request, render_template
from PIL import Image, ImageOps
import io # Diperlukan untuk membaca file dari memori

# --- Pengaturan ---
LEBAR_BARU = 100 
ASCII_CHARS = "@%#*+=-:. " 
# ------------------

# Buat instance 'Manajer Dapur'
app = Flask(__name__)

# --- Ini adalah 'Chef Ahli' (Logika dari script-mu) ---
# Kita bungkus dalam sebuah fungsi
def konversi_ke_ascii(image_stream):
    try:
        img = Image.open(image_stream)
        img_gray = ImageOps.grayscale(img)
        
        lebar_asli, tinggi_asli = img_gray.size
        aspect_ratio = tinggi_asli / lebar_asli
        tinggi_baru = int(aspect_ratio * LEBAR_BARU * 0.55)
        
        img_resized = img_gray.resize((LEBAR_BARU, tinggi_baru))

        pixels = list(img_resized.getdata())
        ascii_string = ""
        rentang_per_karakter = 256 / len(ASCII_CHARS)

        for index, pixel_value in enumerate(pixels):
            map_index = int(pixel_value / rentang_per_karakter)
            if map_index == len(ASCII_CHARS):
                map_index = len(ASCII_CHARS) - 1
                
            ascii_string += ASCII_CHARS[map_index]
            
            if (index + 1) % LEBAR_BARU == 0:
                ascii_string += "\n"
        
        return ascii_string

    except Exception as e:
        print(f"Error di konversi: {e}")
        return "Gagal memproses gambar."
# ----------------------------------------------------


# --- Rute untuk 'Etalase' (Halaman Awal) ---
# Saat orang buka http://127.0.0.1:5000/
# ... (Import-mu sudah benar) ...

@app.route('/')
def index():
    # Suruh Flask cari 'index.html' di folder 'templates' dan kirimkan
    return render_template('index.html')


# --- Rute untuk 'Menerima Pesanan' ---
# Saat form di-submit, datanya dikirim ke sini (/upload)
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'Tidak ada file... (¬_¬)'
    
    file = request.files['file']
    
    if file.filename == '':
        return 'File tidak dipilih.'
    
    if file:
        # Baca file sebagai 'stream' di memori, jangan simpan ke disk
        image_stream = io.BytesIO(file.read())
        
        # Berikan 'stream' itu ke 'Chef Ahli'
        ascii_result = konversi_ke_ascii(image_stream)

        # Kembalikan hasilnya KE DALAM BLOK IF INI
        return render_template('hasil.html', hasil_dari_python=ascii_result)
    
    # Tambahkan fallback jika 'if file:' gagal (meski tidak mungkin)
    return "Gagal upload."
# --- Perintah untuk menyalakan server ---
if __name__ == '__main__':
    # Jalankan di port selain 5000 karena pada beberapa mesin port 5000
    # mungkin sudah dipakai oleh proses sistem (lihat netstat). Menggunakan
    # port 5001 menghindari konflik ini.
    app.run(debug=True, host='127.0.0.1', port=5001)  # debug=True agar server auto-reload kalau kamu ubah kode