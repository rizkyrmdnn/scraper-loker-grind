import os
import requests

# === KONFIGURASI BOT TELEGRAM (KUNCI RAHASIA LO) ===
# Ganti dengan API Token dan Chat ID yang lo simpan di Notepad tadi
BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

def kirim_pesan_telegram(pesan):
    """Fungsi buat nyuruh bot ngirim pesan ke HP lo"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": pesan,
        "parse_mode": "Markdown" # Biar bisa pakai format tebal (*), miring (_), dll
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("✅ Pesan berhasil mendarat di Telegram lo!")
        else:
            print("❌ Gagal ngirim pesan, cek lagi token/chat ID:", response.text)
    except Exception as e:
        print("🚨 Error koneksi:", e)

def cari_loker():
    """
    Fungsi utama buat narik data loker.
    (Di sini gue pakai simulasi data dummy biar lo bisa tes bot-nya dulu).
    """
    print("🤖 Bot sedang mencari loker Data/Cloud Engineer...")
    
    # Nanti bagian ini bisa lo ganti pakai requests.get() ke API portal loker beneran, 
    # atau pakai BeautifulSoup buat scraping web HTML.
    
    # --- SIMULASI HASIL SCRAPING ---
    loker_ditemukan = [
        {"posisi": "Junior Data Engineer", "kantor": "Tokopedia", "link": "https://careers.tokopedia.com/"},
        {"posisi": "Cloud Engineer (Fresh Grad)", "kantor": "Gojek", "link": "https://gojek.com/careers/"}
    ]

    # Kalau ada loker yang match sama keyword lo
    if loker_ditemukan:
        pesan_wa = "🔥 *RADAR LOKER ON THE GRIND* 🔥\n\nBro, ada loker baru nih:\n\n"
        
        for loker in loker_ditemukan:
            pesan_wa += f"💼 *Posisi:* {loker['posisi']}\n"
            pesan_wa += f"🏢 *Perusahaan:* {loker['kantor']}\n"
            pesan_wa += f"🔗 *Apply di sini:* [Link Pendaftaran]({loker['link']})\n\n"
            
        pesan_wa += "Langsung sikat bro, jangan ditunda! 🚀"
        
        # Suruh bot kirim pesan
        kirim_pesan_telegram(pesan_wa)
    else:
        print("Belum ada loker baru yang cocok hari ini.")

if __name__ == "__main__":
    cari_loker()