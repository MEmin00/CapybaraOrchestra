import os
import pygame
import sys
import time
from oyun.anaMenu import AnaMenu
from oyun.sahne import Sahne
from oyun.upgrade import UpgradeEkrani
from oyun.kayanMetin import KayanMetin  # eğer kullanıyorsan

pygame.init()

# --- Pencere ayarları ---
GENISLIK, YUKSEKLIK = 1280, 720
pencere = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
pygame.display.set_caption("Capybara Orchestra")

saat = pygame.time.Clock()
FPS = 60

# --- Oyun verileri ---
oyunVerileri = {
    "notalar": 0,
    "tiklamaGucu": 1,
    "capibaraSayisi": 1,
    "sonTiklamaZamani": 0.0,
    "upgrades": [
        {"isim": "Crash Capibara", "fiyat": 1000, "resim": "varliklar/capibaralar/crash.png", "aktif_resim": "varliklar/capibaralar/crash1.png", "ses": "varliklar/ses/crash.mp3", "carpan": 4, "alinan": False},
        {"isim": "Orgcu Capibara", "fiyat": 5000, "resim": "varliklar/capibaralar/klavye.png", "aktif_resim": "varliklar/capibaralar/klavye1.png", "ses": "varliklar/ses/org.mp3", "carpan": 10, "alinan": False},
        {"isim": "Kemancı Capibara", "fiyat": 20000, "resim": "varliklar/capibaralar/keman.png", "aktif_resim": "varliklar/capibaralar/keman1.png", "ses": "varliklar/ses/keman.mp3", "carpan": 25, "alinan": False},
        {"isim": "Baterist Capibara", "fiyat": 75000, "resim": "varliklar/capibaralar/bateri.png", "aktif_resim": "varliklar/capibaralar/bateri1.png", "ses": "varliklar/ses/bateri.mp3", "carpan": 50, "alinan": False},
        {"isim": "Koro Capibara", "fiyat": 300000, "resim": "varliklar/capibaralar/koro.png", "aktif_resim": "varliklar/capibaralar/koro1.png", "ses": "varliklar/ses/koro.mp3", "carpan": 100, "alinan": False},
        {"isim": "Seyirci", "fiyat": 1000000, "resim": "varliklar/capibaralar/seyirci.png", "aktif_resim": "varliklar/capibaralar/seyirci.png", "ses": "varliklar/ses/hepsi.mp3", "carpan": 500, "alinan": False},
    ],
}

# --- Kayan metin listesi ---
kayan_metinler = []

# --- Ekran nesneleri ---
anaMenu = AnaMenu(pencere, GENISLIK, YUKSEKLIK, oyunVerileri)
sahne = Sahne(pencere, GENISLIK, YUKSEKLIK, oyunVerileri, kayan_metinler)
upgradeEkrani = UpgradeEkrani(pencere, GENISLIK, YUKSEKLIK, oyunVerileri)

aktifEkran = "anaMenu"  # Başlangıç ekranı

# --- Müzik güvenli başlatma (Main'de artık sadece genel mixer init kalsın, spesifik yükleme sahne'de) ---
pygame.mixer.init()

# kontrol flag'ları
muzikCaliyor = False  # Artık kullanılmıyor ama hata vermemesi için kalsın veya silinsin

calisiyor = True
while calisiyor:
    events = pygame.event.get()

    for olay in events:
        if olay.type == pygame.QUIT:
            calisiyor = False

    yeniEkran = None

    # --- Ekran güncellemeleri ---
    if aktifEkran == "anaMenu":
        yeniEkran = anaMenu.guncelle(events)

    elif aktifEkran == "sahne":
        yeniEkran = sahne.guncelle(events)

    elif aktifEkran == "upgrade":
        sahne.ciz()  # Arka planda sahne görünsün
        yeniEkran = upgradeEkrani.guncelle(events)

    # --- Eğer yeni ekran döndüyse geçiş yap ---
    if yeniEkran:
        # Ekran geçişlerinde müziği sahne üzerinden durdurabiliriz
        if aktifEkran == "sahne" and yeniEkran == "upgrade":
            # Sahne duraklatma mantığı: Sahne içindeki guncelle'de upgrade'e geçerken stoplanıyor zaten
            pass
            
        if yeniEkran == "anaMenu":
            sahne.muzik_durdur()

        aktifEkran = yeniEkran

    # --- ESKİ MÜZİK KODLARI SİLİNDİ (Artık Sahne sınıfı yönetiyor) ---

    # --- Çizimleri güncelleme (aktif ekranın kendisi çizer) ---

    # --- Çizimleri güncelleme (aktif ekranın kendisi çizer) ---
    pygame.display.flip()
    saat.tick(FPS)

pygame.quit()
sys.exit()
