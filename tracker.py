#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import cloudscraper
from bs4 import BeautifulSoup

# Pushcut Webhook URL (senin verdiğin, tam URL)
PUSHCUT_URL = "https://api.pushcut.io/CLDonSTvi22mteRYjxTdI/notifications/Kitap%20ilan%C4%B1"

def send_notification(title: str, message: str):
    """
    Pushcut üzerinden bildirim gönderir.
    """
    payload = {
        "title": title,
        "text": message
    }
    try:
        r = requests.post(PUSHCUT_URL, json=payload, timeout=10)
        r.raise_for_status()
    except Exception as e:
        print(f"⚠️ Pushcut gönderilemedi: {e}")

def fetch_nadir_ilanlar():
    """
    NadirKitap arama sayfasından ilan başlıklarını ve linklerini çeker.
    """
    scraper = cloudscraper.create_scraper()  # 403 hatası almamak için cloudscraper kullanıyoruz
    url = (
        "https://www.nadirkitap.com/kitap-ara.html"
        "?kelime=antika+kitap"
        "&kitap_tipi=imzali"
        "&kitap_tipi=ilk%20baski"
    )
    r = scraper.get(url, timeout=15)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    ilanlar = []
    for link in soup.select("a.baslik"):
        ilanlar.append({
            "title": link.get_text(strip=True),
            "href": "https://www.nadirkitap.com" + link["href"]
        })
    return ilanlar

def fetch_diger_site_fiyatlari(ilan):
    """
    Diğer platformlardan (örnek: KitapXYZ, OtakKitap vb.) fiyatları çeker.
    Şu anda stub (yer tutucu) olarak sabit iki fiyat dönüyor.
    Gerçek entegrasyonda burayı kendi API/HTML parsing kodunla dolduracaksın.
    """
    return [
        {"site": "KitapXYZ",   "price": 50, "url": "https://kitapxyz.com/123"},
        {"site": "OtakKitap",  "price": 75, "url": "https://otakkitap.com/456"}
    ]

def main():
    # 1) NadirKitap ilanlarını çek
    try:
        ilanlar = fetch_nadir_ilanlar()
    except Exception as e:
        send_notification("NadirKitap HATA", f"Liste çekilemedi: {e}")
        return

    # 2) Her ilan için diğer sitelere bak, en ucuzu bildir
    for ilan in ilanlar:
        try:
            fiyat_listesi = fetch_diger_site_fiyatlari(ilan)
            if not fiyat_listesi:
                continue
            en_ucuz = min(fiyat_listesi, key=lambda x: x["price"])
            send_notification(
                "Ucuz Kitap Bulundu!",
                f"{ilan['title']}\n"
                f"NadirKitap: {ilan['href']}\n"
                f"En ucuz {en_ucuz['site']}: {en_ucuz['price']} ₺\n"
                f"{en_ucuz['url']}"
            )
        except Exception as e:
            send_notification("Karşılaştırma HATA", f"{ilan['title']} işlenemedi: {e}")

if __name__ == "__main__":
    main()
