# src/tracker.py

import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from config import PUSHCUT_URL, SOURCE_URL, MARKET_SITES, ANALYSIS_KEYWORDS

def send_notification(title: str, text: str):
    payload = {
        "notification": {"title": title, "text": text}
    }
    try:
        r = requests.post(PUSHCUT_URL, json=payload)
        r.raise_for_status()
    except Exception as e:
        print(f"Bildirimi gönderirken hata: {e}")

def fetch_nadirkitap_listings():
    """NadirKitap'tan en son ilanları çek"""
    r = requests.get(SOURCE_URL)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    # TODO: sayfadaki ilan kapsayıcısını uygun selector ile bulun
    items = soup.select(".listing-item")  
    listings = []
    for it in items:
        title = it.select_one(".title").get_text(strip=True)
        price = it.select_one(".price").get_text(strip=True)
        # sadece “ilk baskı” ve “imzalı” içerenler
        if all(k.lower() in title.lower() for k in ANALYSIS_KEYWORDS):
            listings.append((title, price))
    return listings

def fetch_market_price(site_name: str, query: str):
    """Tek bir pazaryerinde query ile fiyat sorgula, en düşük fiyatı dön"""
    url = MARKET_SITES[site_name].format(query=quote_plus(query))
    r = requests.get(url)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    # TODO: her pazar yeri için ilanların fiyatını çıkaracak selector'ü ayarla
    price_tags = soup.select(".item-price")
    prices = []
    for pt in price_tags:
        txt = pt.get_text(strip=True).replace(".", "").replace(",", ".")
        try:
            prices.append(float(txt.strip("TL ")))
        except:
            continue
    return min(prices) if prices else None

def compare_and_notify():
    listings = fetch_nadirkitap_listings()
    if not listings:
        send_notification("Takip Botu", "NadirKitap’ta yeni ilan bulunamadı.")
        return

    for title, nk_price in listings:
        # sayıyı float’a çevir
        nk_val = float(nk_price.replace(".", "").replace(",", ".").strip("TL "))
        market_prices = {}
        for site in MARKET_SITES:
            try:
                mp = fetch_market_price(site, title)
                if mp:
                    market_prices[site] = mp
            except:
                print(f"{site} sorgusunda hata")
        if not market_prices:
            send_notification("Fiyat Karşılaştırma", f"“{title}” için diğer sitelerde veri yok.")
            continue

        best_site, best_price = min(market_prices.items(), key=lambda x: x[1])
        if nk_val < best_price:
            msg = (f"NadirKitap’ta “{title}”\n"
                   f"{nk_price} TL ile diğer sitelerin ({best_site}) "
                   f"{best_price} TL piyasa fiyatının altında!")
            send_notification("Fırsat Bulundu!", msg)

if __name__ == "__main__":
    compare_and_notify()
