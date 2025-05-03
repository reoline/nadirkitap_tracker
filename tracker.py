def fetch_nadir_ilanlar():
    """
    NadirKitap arama sayfasından ilan başlıklarını ve linklerini döner.
    (User-Agent eklenerek 403 Forbidden hatası aşılır)
    """
    url = (
        "https://www.nadirkitap.com/kitap-ara.html"
        "?kelime=antika+kitap&kitap_tipi=imzali&kitap_tipi=ilk%20baski"
    )
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/115.0.0.0 Safari/537.36"
        )
    }
    try:
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()
    except Exception as e:
        send_notification("NadirKitap HATA", f"Liste çekilemedi: {e}")
        return []

    soup = BeautifulSoup(r.text, "html.parser")
    ilanlar = []
    for a in soup.select("a.baslik"):
        ilanlar.append({
            "title": a.get_text(strip=True),
            "href": "https://www.nadirkitap.com" + a["href"]
        })
    return ilanlar
