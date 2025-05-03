#!/usr/bin/env python3
# tracker.py

import cloudscraper
from bs4 import BeautifulSoup
import datetime
import requests

# —————— CONFIG ——————
# Pushcut Webhook URL’in:
PUSHCUT_URL = "https://api.pushcut.io/CLDonSTvi22mteRYjxTdI/notifications/Kitap%20ilan%C4%B1"

# Anahtar kelimeler:
SEARCH_KEYWORD = "antika kitap"
# Kitap tipleri parametresi:
BOOK_TYPES = ["imzali", "ilk baski"]
# ————————————————————

def send_notification(title, message):
    payload = {"text": message}
    try:
        resp = requests.post(PUSHCUT_URL, json=payload, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        print(f"Pushcut gönderilemedi: {e}")

def fetch_nadir_ilAnlar():
    # cloudscraper ile oturum aç
    scraper = cloudscraper.create_scraper()
    # URL’yi oluştur
    types_param = "&".join(f"kitap_tipi={t.replace(' ', '%20')}" for t in BOOK_TYPES)
    url = f"https://www.nadirkitap.com/kitap-ara.html?kelime={SEARCH_KEYWORD.replace(' ', '+')}&{types_param}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/115.0.0.0 Safari/537.36"
    }

    try:
        r = scraper.get(url, headers=headers, timeout=15)
        r.raise_for_status()
    except Exception as e:
        send_notification("NadirKitap HATA", f"Liste çekilemedi: {e}")
        return []

    soup = BeautifulSoup(r.text, "html.parser")
    ilanlar = []
    for link in soup.select("a.baslik"):
        ilanlar.append({
            "title": link.get_text(strip=True),
            "href": "https://www.nadirkitap.com" + link["href"]
        })
    return ilanlar

def fetch_diger_site_fiyatlari(ilan):
    # Henüz stub: buraya diğer sitelerden gerçek fiyatları almak için kod ekleceksin.
    return [
        {"site": "KitapXYZ",  "price": 50, "url": "https://kitapxyz.com/123"},
        {"site": "OtakKitap", "price": 75, "url": "https://otakkitap.com/456"},
    ]

def main():
    # Test bildirim (en başta gönderelim)
    send_notification("Bot Çalıştı", "NadirKitap tracker devrede 🎉")

    ilanlar = fetch_nadir_ilAnlar()
    if not ilanlar:
        return

    for ilan in ilanlar:
        diger = fetch_diger_site_fiyatlari(ilan)
        if not diger:
            continue
        en_ucuz = min(diger, key=lambda x: x["price"])
        # Fiyat karşılaştırması
        send_notification(
            "Ucuz Kitap Bulundu!",
            f"{ilan['title']}\n"
            f"NadirKitap: {ilan['href']}\n"
            f"En ucuz {en_ucuz['site']}: {en_ucuz['price']} TL\n"
            f"{en_ucuz['url']}"
        )

if __name__ == "__main__":
    main()
