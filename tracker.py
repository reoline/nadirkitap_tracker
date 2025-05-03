#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup

# 1) Buraya kendi Pushcut URL'inizi tam yapıştırın:
PUSHCUT_URL = "https://api.pushcut.io/CLDonSTvi22mteRYjxTdI/notifications/Kitap%20ilan%C4%B1"

def send_notification(title, message):
    payload = {"title": title, "text": message}
    try:
        r = requests.post(PUSHCUT_URL, json=payload, timeout=10)
        r.raise_for_status()
    except Exception as e:
        print(f"❌ Pushcut gönderilemedi: {e}")

def fetch_nadir_ilanlar():
    url = "https://www.nadirkitap.com/kitap-ara.html?kelime=antika+kitap&kitap_tipi=imzali&kitap_tipi=ilk%20baski"
    try:
        r = requests.get(url, timeout=15)
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
    # Stub: örnek olarak sabit veri dönüyor.
    return [
        {"site": "KitapXYZ", "price": 50, "url": "https://kitapxyz.com/123"},
        {"site": "OtakKitap", "price": 75, "url": "https://otakkitap.com/456"}
    ]

def main():
    # **Test bildirimi**: bot her çalıştığında size test bildirimi gönderelim
    send_notification("Bot Çalıştı", "NadirKitap tracker devrede 🎉")

    ilanlar = fetch_nadir_ilanlar()
    for ilan in ilanlar:
        diger = fetch_diger_site_fiyatlari(ilan)
        if not diger:
            continue
        en_ucuz = min(diger, key=lambda x: x["price"])
        send_notification(
            "Ucuz Kitap Bulundu!",
            f"{ilan['title']}\n"
            f"NadirKitap: {ilan['href']}\n"
            f"En ucuz {en_ucuz['site']}: {en_ucuz['price']} TL\n"
            f"{en_ucuz['url']}"
        )

if __name__ == "__main__":
    main()
