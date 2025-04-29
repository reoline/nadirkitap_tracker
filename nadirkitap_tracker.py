import requests
from bs4 import BeautifulSoup
import datetime

# Pushcut Webhook URL (senin verdiğin adres)
PUSHCUT_URL = "https://api.pushcut.io/CLDonSTvi22mteRYjxTdI/notifications/NadirKitap"

def send_notification(title, message):
    payload = {"text": message}
    try:
        r = requests.post(PUSHCUT_URL, json=payload)
        r.raise_for_status()
    except Exception as e:
        print(f"Pushcut gönderilemedi: {e}")

def fetch_nadir_ilanlar():
    url = "https://www.nadirkitap.com/kitap-ara.html?kelime=antika+kitap&kitap_tipi=imzali&kitap_tipi=ilk%20baski"
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "lxml")
    ilanlar = []
    for link in soup.select("a.baslik"):
        ilanlar.append({
            "title": link.get_text(strip=True),
            "href": "https://www.nadirkitap.com" + link["href"]
        })
    return ilanlar

def fetch_diger_site_fiyatlari(ilan):
    # Örnek stub: burada catawiki, ebay, letgo yerine kendi sitelerini sorgulayacaksın
    # Basitçe ilan["title"] anahtar kelimeyle arama isteği yollayıp fiyatları JSON veya HTML döndürebilirsin.
    return [  # örnek dönüş
        {"site": "KitapXYZ", "price": 50, "url": "https://kitapxyz.com/123"},
        {"site": "OtakKitap", "price": 75, "url": "https://otakkitap.com/456"}
    ]

def main():
    try:
        ilanlar = fetch_nadir_ilanlar()
    except Exception as e:
        send_notification("NadirKitap HATA", f"Liste çekilemedi: {e}")
        return

    for ilan in ilanlar:
        diger = fetch_diger_site_fiyatlari(ilan)
        if not diger:
            continue
        en_ucuz = min(diger, key=lambda x: x["price"])
        # Burada kendi fiyat karşılaştırmasını yap; 
        # diyelim ki nadirkitapta fiyatı otomatik alamıyorsun, stuba görə hep bildirim atıyoruz:
        send_notification("Ucuz Kitap Bulundu!",
                          f"{ilan['title']}\n"
                          f"NadirKitap link: {ilan['href']}\n"
                          f"En ucuz {en_ucuz['site']}: {en_ucuz['price']} TL\n"
                          f"{en_ucuz['url']}")

if __name__ == "__main__":
    main()
