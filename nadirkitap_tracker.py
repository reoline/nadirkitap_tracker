import requests
from bs4 import BeautifulSoup
import datetime

#  ——————————————————————
#  Buraya kendi Pushcut Webhook URL'ini tam olarak yapıştırdık:
PUSHCUT_URL = "https://api.pushcut.io/CLDonSTvi22mteRYjxTdI/notifications/NadirKitap"
#  ——————————————————————

def send_notification(title, message):
    payload = {
        "title": title,
        "text": message
    }
    try:
        resp = requests.post(PUSHCUT_URL, json=payload, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        print(f"Pushcut gönderilemedi: {e}")

def fetch_nadir_ilanlar():
    # “antika kitap” + “imzalı” + “ilk baskı” filtreleri
    url = "https://www.nadirkitap.com/kitap-ara.html"
    params = {
        "kelime": "antika kitap",
        "kitap_tipi": ["imzali", "ilk%20baski"]
    }
    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "lxml")
    ilanlar = []
    for a in soup.select("a.baslik"):
        ilanlar.append({
            "title": a.get_text(strip=True),
            "href": "https://www.nadirkitap.com" + a["href"]
        })
    return ilanlar

def fetch_diger_site_fiyatlari(title):
    """
    Burada benzersiz bir başlık ile diğer sitelerde arama yapıp
    fiyatları döneceksin. Örnek siteler:
      - kitapantik.com
      - ekitap.com
      - kitapsec.com
      - dr.com.tr
    Şuanda stub olarak örnek döndürüyoruz.
    """
    return [
        {"site": "KitapAntik", "price": 120, "url": "https://kitapantik.com/örnek"},
        {"site": "EKitap",     "price": 140, "url": "https://ekitap.com/örnek"}
    ]

def main():
    try:
        ilanlar = fetch_nadir_ilanlar()
    except Exception as e:
        send_notification("NadirKitap HATA", f"Liste çekilemedi: {e}")
        return

    for ilan in ilanlar:
        diger = fetch_diger_site_fiyatlari(ilan["title"])
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
