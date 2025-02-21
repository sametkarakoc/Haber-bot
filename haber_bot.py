import requests
import feedparser
import time

# Telegram API bilgileri
TELEGRAM_BOT_TOKEN = "7567881808:AAF46-Wwa99scQ3P_T-8RDxROqFsIvxF5Og"
TELEGRAM_CHAT_ID = "-1002410148553"

# Takip edilecek RSS kaynakları
RSS_FEEDS = [
    "https://cyprus-mail.com/feed/",
    "https://www.kibrisgenctv.com/rss",
    "https://www.yeniduzen.com/rss/",
    "https://www.kanalt.com/rss",
    "https://www.gundemkibris.com/rss/",
    "https://haberkibris.com/rss.php",
    "https://ahbapgazetesi.com/feed/",
    "https://guneskibris.com/feed/",
    "https://rss.app/feeds/lR0LlUmrtsgaIsgj.xml",
    "https://www.kibrisgercek.com/rss",
    "https://giynikgazetesi.com/feed/",
    "https://www.diyaloggazetesi.com/rss",
    "https://www.bagimsiz.com/rss",
    "https://www.kibrisligazetesi.com/feed/",
    "https://www.kibristurk.com/rss",
    "https://bugunkibris.com/feed/",
    "https://kibrisgazetesi.com/feed/",
    "https://ozgurgazetekibris.com/feed",
    "https://www.kibrismanset.com/rss"
]

# Daha önce gönderilen haberleri saklamak için
gonderilen_haberler = set()

def telegrama_mesaj_gonder(mesaj):
    """Telegram grubuna mesaj gönderir."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mesaj,
        "parse_mode": "HTML"
    }
    requests.post(url, data=payload)

def haberleri_kontrol_et():
    """RSS kaynaklarını tarar ve yeni haberleri Telegram grubuna gönderir."""
    global gonderilen_haberler
    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:5]:  # Her kaynaktan en yeni 5 haberi al
            haber_baslik = entry.title
            haber_link = entry.link
            haber_id = f"{haber_baslik}-{haber_link}"  # Haberi eşsiz yapan kimlik

            if haber_id not in gonderilen_haberler:
                mesaj = f"📰 <b>{haber_baslik}</b>\n\n🔗 {haber_link}"
                telegrama_mesaj_gonder(mesaj)
                gonderilen_haberler.add(haber_id)  # Haberi gönderilenler listesine ekle

if __name__ == "__main__":
    while True:
        haberleri_kontrol_et()
        print("✅ Haberler kontrol edildi. 10 dakika sonra tekrar kontrol edilecek...")
        time.sleep(600)  # 10 dakika bekle (600 saniye)
