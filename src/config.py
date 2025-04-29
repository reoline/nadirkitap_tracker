# src/config.py

# Pushcut Webhook URL’in:
PUSHCUT_URL = "https://api.pushcut.io/CLDonSTvi22mteRYjxTdI/notifications/Milli%20Emlak"

# NadirKitap arama URL’si (ilk baskı + imzalı filtreleri)
SOURCE_URL = (
    "https://www.nadirkitap.com/kitapara.php?"
    "ara=aramayap&imzali=1&birincibaski=1&tip=kitap"
)

# Karşılaştırma için kullanacağımız pazar siteleri
# {query} → ilan başlığıyla doldurulacak yer
MARKET_SITES = {
    "Kitantik":    "https://www.kitantik.com/arsiv/kitap/?search={query}",
    "AntikSanat":  "https://www.antiksanat.com/arsiv/kitap?search={query}",
    "Sahibinden":  "https://www.sahibinden.com/arama?query={query}&kategoriler[]=Antika+Kitap",
    "AbeBooks":    "https://www.abebooks.com/servlet/SearchResults?sts=t&kn={query}"
}

# İlânlarda arayacağımız ek filtre anahtar kelimeler
ANALYSIS_KEYWORDS = ["ilk baskı", "imzalı"]
