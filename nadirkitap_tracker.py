import requests
from bs4 import BeautifulSoup
import datetime

# ——————— Pushcut Webhook URL’iniz ———————
PUSHCUT_URL = "https://api.pushcut.io/CLDonSTvi22mteRYjxTdI/notifications/NadirKitap"
# —————————————————————————————————————————

def send_notification(title: str, message: str):
    """
    Pushcut’a bildirimi doğru JSON formatında gönderir.
    title   : Bildirim başlığı (Pushcut panelindeki notification adı)
    message : Bildirim içeriği
    """
    payload = {
        "input": {
            "text": f"{title}\n{message}"
        }
    }
    try:
        r = requests.post(PUSHCUT_URL, json=payload, timeout=10)
        r.raise_for_status()
        print(f"✔️ Bildirim gönderildi: {title}")
    except Exception as e:
        print(f"❌ Pushcut gönderilemedi: {e}")

def fetch_nadir_ilanlar():
    """
    NadirKitap’ta 'antika kitap' + 'imzalı' + 'ilk baskı' filtreli ilanları çeker.
    """
    url = (
      "https://www.nadirkitap.com/kitap-ara.html"
      "?kelime=antika+kitap"
      "&kitap_tipi=imzali"
      "&kitap_tipi=ilk%20baski"
    )
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "lxml")
    ilanlar = []
    for a in soup.select("a.baslik"):
        ilanlar.append({
            "title": a.get_text(strip=True),
            "href": "https://www.nadirkitap.com" + a["href"]
        })
    return ilanlar

def fetch_diger_site_fiyatlari(ilan):
    """
    Diğer sitelerde aynı başlıkla arama yapıp fiyat listesini döner.
    Buraya istediğiniz siteler için scraping veya API entegrasyonu yazabilirsiniz.
    Örnek stub:
    """
    # TODO: burayı kendi hedef sitelerinizle değiştirin
    return [
        {"site": "KitapXYZ",  "price": 50, "url": "https://kitapxyz.com/123"},
        {"site": "OtakKitap", "price": 75, "url": "https://otakkitap.com/456"},
    ]

def main():
    # 1) Nadirk itap’tan ilanları çek
    try:
        ilanlar = fetch_nadir_ilanlar()
    except Exception as e:
        send_notification("NadirKitap HATA", f"Liste çekilemedi: {e}")
        return

    if not ilanlar:
        print("🎈 Yeni ilan yok.")
        return

    # 2) Her ilanın piyasa fiyatını diğer sitelerden al, en ucuzu seç
    for ilan in ilanlar:
        diger_fiyatlar = fetch_diger_site_fiyatlari(ilan)
        if not diger_fiyatlar:
            send_notification(
                "Fiyat Karşılaştırma HATA",
                f"{ilan['title']}\nDiğer sitelerden fiyat alınamadı."
            )
            continue

        en_ucuz = min(diger_fiyatlar, key=lambda x: x["price"])
        # 3) Eğer NadirKitap fiyatı (manüel eklemediyseniz stub olduğundan hep bildirim atılacak)
        send_notification(
            "Ucuz Kitap Bulundu!",
            f"{ilan['title']}\n"
            f"NadirKitap: {ilan['href']}\n"
            f"En ucuz {en_ucuz['site']}: {en_ucuz['price']} TL\n"
            f"{en_ucuz['url']}"
        )

if __name__ == "__main__":
    main()
