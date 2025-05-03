#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup

# —————— Pushcut Webhook URL ——————
# curl ile test ettiğiniz URL’i tam olarak buraya yapıştırın:
PUSHCUT_URL = "https://api.pushcut.io/CLDonSTvi22mteRYjxTdI/notifications/Kitap%20ilan%C4%B1"

def send_notification(title, message):
    """Pushcut’a başlık + metin gönderir."""
    payload = {"title": title, "text": message}
    try:
        r = requests.post(PUSHCUT_URL, json=payload, timeout=10)
        r.raise_for_status()
    except Exception as e:
        print(f"Pushcut gönderilemedi: {e}")

def fetch_nadir_ilanlar():
    """NadirKitap’tan ilan başlıklarını ve linklerini çeker."""
    url = (
        "https://www.nadirkitap.com/kitap-ara.html?"
        "kelime=antika+kitap&kitap_tipi=imzali&kitap_tipi=ilk%20baski"
    )
    headers = {"User-Agent": "Mozilla/5.0"}  # engel atmasın diye
    try:
        r = requests.get(url, headers=headers, timeout=15)
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
    """
    Stub: diğer sitelerde arama yapıp fiyat döndürür.
    Gerçek projede kendi API’lerinizi / scraping kodunuzu ekleyin.
    """
    return [
        {"site": "KitapXYZ", "price": 50, "url": "https://kitapxyz.com/123"},
        {"site": "OtakKitap", "price": 75, "url": "https://otakkitap.com/456"},
    ]

def main():
    # ———— 1) Debug bildirimi — çalışıyor mu kontrol edin ————
    send_notification("DEBUG", "Pushcut bildirim mekanizması çalışıyor ✅")

    # ———— 2) NadirKitap ilanları — çek ve sayısını bildir ————
    ilanlar = fetch_nadir_ilanlar()
    send_notification("İlan sayısı", str(len(ilanlar)))

    # ———— 3) Karşılaştır ve bildirim gönder ————
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
