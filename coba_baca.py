from PIL import Image, ImageOps

# --- Pengaturan ---
LEBAR_BARU = 100

# --- Kamus Ubin (Character Ramp) ---
# Dari paling gelap (kepadatan tinggi) ke paling terang (kepadatan rendah)
# Kamu bisa ganti-ganti ini nanti untuk hasil yang berbeda.
# (Ada 10 karakter, termasuk spasi di akhir)
ASCII_CHARS = "@%#*+=-:. " 
# ------------------

try:
    img = Image.open("gambar.jpg")
    img_gray = ImageOps.grayscale(img)
    
    lebar_asli, tinggi_asli = img_gray.size
    aspect_ratio = tinggi_asli / lebar_asli
    tinggi_baru = int(aspect_ratio * LEBAR_BARU * 0.55)
    
    img_resized = img_gray.resize((LEBAR_BARU, tinggi_baru))

    print(f"Ukuran asli: ({lebar_asli}, {tinggi_asli})")
    print(f"Ukuran baru untuk ASCII: ({LEBAR_BARU}, {tinggi_baru})")
    
    # --- Langkah 3: Mapping Pixel ke Karakter ---
    
    # 1. Ambil semua data pixel dari gambar kecil itu
    # Ini akan jadi list panjang berisi angka (0-255)
    pixels = list(img_resized.getdata())
    
    # 2. Siapkan 'kanvas' kosong untuk string kita
    ascii_string = ""
    
    # 3. Hitung rentang untuk mapping
    # Kita punya 10 karakter di ASCII_CHARS
    # Rentang kecerahan adalah 0-255 (total 256 nilai)
    # Jadi 1 karakter mewakili: 256 / 10 = 25.6
    rentang_per_karakter = 256 / len(ASCII_CHARS)

    # 4. Loop (Iterasi) setiap pixel
    for index, pixel_value in enumerate(pixels):
        
        # Ini 'Seniman Mosaik'-nya:
        # (Misal: pixel_value = 150)
        # 150 / 25.6 = 5.85...
        # int(5.85) = 5
        # karakter = ASCII_CHARS[5] (yaitu '-')
        map_index = int(pixel_value / rentang_per_karakter)
        
        # Antisipasi jika pixel_value 255 (paling terang)
        if map_index == len(ASCII_CHARS):
            map_index = len(ASCII_CHARS) - 1
            
        ascii_string += ASCII_CHARS[map_index]
        
        # 5. Cek apakah sudah waktunya ganti baris?
        # Jika index+1 bisa dibagi habis oleh LEBAR_BARU,
        # berarti kita di akhir baris.
        if (index + 1) % LEBAR_BARU == 0:
            ascii_string += "\n" # Tambah 'Enter' (new line)

    # --- Selesai ---
    
    # Cetak hasilnya ke terminal
    print("\n--- HASIL ASCII ART ---")
    print(ascii_string)
    print("-------------------------")
    
    # (Opsional) Simpan ke file .txt biar lebih jelas
    with open("hasil_ascii.txt", "w") as f:
        f.write(ascii_string)
    print("Hasil juga disimpan di 'hasil_ascii.txt'")


except FileNotFoundError:
    print("...File tidak ditemukan.")
except Exception as e:
    print(f"Gagal. Error: {e}")