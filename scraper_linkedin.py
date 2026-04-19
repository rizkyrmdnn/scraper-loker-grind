# Script web scrapping LinkedIn

import os
import requests
from bs4 import BeautifulSoup

# === KONFIGURASI BOT TELEGRAM ===
BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN'] 
CHAT_ID = os.environ['TELEGRAM_CHAT_ID']  

def kirim_pesan_telegram(pesan):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": pesan,
        "parse_mode": "HTML" 
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            print(f"❌ Telegram nolak pesannya: {response.text}")
    except Exception as e:
        print("🚨 Error koneksi Telegram:", e)

def scrape_linkedin_loker():
    print("Menyamar menjadi manusia dan membuka LinkedIn...")
    
    # Target URL: Loker Data Engineer di Indonesia (24 Jam Terakhir)
    url = "https://www.linkedin.com/jobs/search?keywords=Data%20Engineer&location=Indonesia&f_TPR=r86400"
    
    # Header manipulation agar tidak disangka bot
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }

    try:
        response = requests.get(url, headers=headers)
        
        # Cek apakah LinkedIn marah dan ngeblokir kita
        if response.status_code != 200:
            print(f"❌ Gagal akses LinkedIn. Status Code: {response.status_code}")
            return

        # Masukin HTML mentah ke mesin bedah BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Mencari semua elemen "Kartu Pekerjaan" berdasarkan class HTML-nya
        # (Class ini bisa berubah sewaktu-waktu kalau LinkedIn update webnya)
        job_cards = soup.find_all('div', class_='base-card')
        
        if job_cards:
            pesan_wa = "<b>RADAR LINKEDIN: DATA ENGINEER</b> \n\nIni loker fresh 24 jam terakhir dari LinkedIn:\n\n"
            
            # Ambil maksimal 5 loker teratas aja
            for card in job_cards[:5]:
                # Cari Judul
                title_tag = card.find('h3', class_='base-search-card__title')
                posisi = title_tag.text.strip() if title_tag else 'Posisi tidak diketahui'
                
                # Cari Nama Perusahaan
                company_tag = card.find('h4', class_='base-search-card__subtitle')
                perusahaan = company_tag.text.strip() if company_tag else 'Perusahaan tidak diketahui'
                
                # Cari Link Apply
                link_tag = card.find('a', class_='base-card__full-link')
                link = link_tag['href'] if link_tag else ''

                pesan_wa += f"💼 <b>Posisi:</b> {posisi}\n"
                pesan_wa += f"🏢 <b>Perusahaan:</b> {perusahaan}\n"
                pesan_wa += f"🔗 <b>Apply:</b> <a href='{link}'>Klik di Sini</a>\n\n"
                
            pesan_wa += "Sikat aja"
            
            kirim_pesan_telegram(pesan_wa)
            print("✅ Data dari LinkedIn sukses dikirim!")
        else:
            print("Belum ada loker baru atau LinkedIn memblokir parsing kita (HTML tidak sesuai).")

    except Exception as e:
        print("🚨 Error saat scraping:", e)

if __name__ == "__main__":

    scrape_linkedin_loker()