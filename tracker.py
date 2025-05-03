def main():
    # — Test bildirimi: her çalıştığında devrede olduğunu gösterir
    send_notification("Bot Çalıştı", "NadirKitap tracker devrede 🎉")

    # — Yeni eklenen debug bildirimi ve konsol çıktısı
    ilanlar = fetch_nadir_ilanlar()
    print(f"[DEBUG] ilan sayısı: {len(ilanlar)}")
    send_notification("Debug", f"İlan sayısı: {len(ilanlar)}")

    # — Eğer hiç ilan yoksa devam etme
    if not ilanlar:
        return

    # — İlanlar varsa stub fiyatlarla karşılaştırıp bildirim gönder
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
