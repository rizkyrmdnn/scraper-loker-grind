import os
import requests

# === KONFIGURASI BOT TELEGRAM ===
BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

def kirim_pesan_telegram(pesan):
    """Fungsi buat nyuruh bot ngirim pesan ke HP lo"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": pesan,
        # PRO TIP: Pake HTML lebih aman dari Markdown di Telegram biar nggak error 
        # kalau ketemu karakter aneh kayak kurung () atau strip - di judul loker
        "parse_mode": "HTML" 
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("✅ Pesan berhasil mendarat di Telegram lo!")
        else:
            print("❌ Gagal ngirim pesan, cek lagi token/chat ID:", response.text)
    except Exception as e:
        print("🚨 Error koneksi Telegram:", e)

def cari_loker_beneran():
    """Fungsi utama buat hit API loker dan ngolah JSON-nya"""
    print("🤖 Menarik data loker Data Engineer beneran dari API...")
    
    # Endpoint API gratis dari Remotive khusus keyword "data engineer"
    # Lo bisa ganti parameter search-nya nanti (misal: cloud%20engineer)
    api_url = "https://remotive.com/api/remote-jobs?search=data%20engineer&limit=10"

    try:
        response = requests.get(api_url)
        data = response.json() # Ekstrak response jadi bentuk JSON (Dictionary Python)
        jobs = data.get('jobs', [])

        if jobs:
            pesan_wa = "🔥 <b>RADAR LOKER TECH (REAL DATA)</b> 🔥\n\nBro, ini loker Data Engineer terbaru yang gue tarik dari API:\n\n"
            
            # Kita ambil 3 loker teratas aja biar pesan Telegram lo nggak nyepam kepanjangan
            for job in jobs[:3]:
                posisi = job.get('title', 'Posisi tidak diketahui')
                perusahaan = job.get('company_name', 'Perusahaan tidak diketahui')
                lokasi = job.get('candidate_required_location', 'Global/Remote')
                link = job.get('url', '')

                pesan_wa += f"💼 <b>Posisi:</b> {posisi}\n"
                pesan_wa += f"🏢 <b>Perusahaan:</b> {perusahaan}\n"
                pesan_wa += f"🌍 <b>Syarat Lokasi:</b> {lokasi}\n"
                pesan_wa += f"🔗 <b>Apply:</b> <a href='{link}'>Klik di Sini</a>\n\n"
                
            pesan_wa += "Sikat bro, ON THE GRIND! 🚀"
            
            # Eksekusi kirim pesan
            kirim_pesan_telegram(pesan_wa)
            print("✅ Data loker sukses ditarik dan dikirim!")
            
        else:
            print("Belum ada loker baru yang cocok dari API hari ini.")
            
    except Exception as e:
        print("🚨 Gagal hit API loker:", e)

if __name__ == "__main__":
    cari_loker_beneran()