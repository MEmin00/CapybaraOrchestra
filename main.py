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
pygame.display.set_caption("Capybara Konseri 🎶")

saat = pygame.time.Clock()
FPS = 60

# --- Oyun verileri ---
oyunVerileri = {
    "notalar": 0,
    "tiklamaGucu": 1,
    "capibaraSayisi": 1,
    # sahne artık son tıklama zamanını tutacak:
    "sonTiklamaZamani": 0.0,
}

# --- Kayan metin listesi ---
kayan_metinler = []

# --- Ekran nesneleri ---
anaMenu = AnaMenu(pencere, GENISLIK, YUKSEKLIK, oyunVerileri)
sahne = Sahne(pencere, GENISLIK, YUKSEKLIK, oyunVerileri, kayan_metinler)
upgradeEkrani = UpgradeEkrani(pencere, GENISLIK, YUKSEKLIK, oyunVerileri)

aktifEkran = "anaMenu"  # Başlangıç ekranı

# --- Müzik güvenli başlatma (yükle ama çalma kontrolü main'de olacak) ---
muzikYolu = "varliklar/ses/flute.mp3"
muzikYuklu = False
try:
    pygame.mixer.init()
    if os.path.exists(muzikYolu):
        pygame.mixer.music.load(muzikYolu)
        pygame.mixer.music.set_volume(0.6)
        muzikYuklu = True
    else:
        print(f"⚠️ Müzik dosyası bulunamadı: {muzikYolu}")
except Exception as e:
    print("⚠️ Müzik sistemi başlatılamadı:", e)
    muzikYuklu = False

# kontrol flag'ları
muzikCaliyor = False  # main tarafında takip ederiz
MUSIC_TIMEOUT = 1.5   # tıklama sonrası müzik oynatma süresi (saniye)

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
        yeniEkran = upgradeEkrani.guncelle(events)

    # --- Eğer yeni ekran döndüyse geçiş yap ---
    if yeniEkran:
        # geçişten önce müziğe müdahale gerekiyorsa yap
        if muzikYuklu:
            # sahne -> upgrade: pause et
            if aktifEkran == "sahne" and yeniEkran == "upgrade":
                if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
                    pygame.mixer.music.pause()
            # upgrade -> sahne: unpause yerine main kontrolüyle başlat/ devam ettir
            if aktifEkran == "upgrade" and yeniEkran == "sahne":
                # eğer müzik halen çalıyor (pause durumundaysa) unpause yap,
                # ama eğer stoplandıysa main loop başlatma mantığı halleder.
                try:
                    if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
                        pygame.mixer.music.unpause()
                except:
                    pass
            # herhangi bir zamanda ana menüye döndüğünde müziği tamamen durdur
            if yeniEkran == "anaMenu":
                try:
                    if pygame.mixer.get_init():
                        pygame.mixer.music.stop()
                        muzikCaliyor = False
                except:
                    pass

        aktifEkran = yeniEkran

    # --- MÜZİK ZAMANSI KONTROLÜ (TEK MERKEZ) ---
    # Sahne aktifken, son tıklama zamanına göre müziği başlat/durdur
    if aktifEkran == "sahne" and muzikYuklu:
        simdi = time.time()
        sonTik = oyunVerileri.get("sonTiklamaZamani", 0.0)
        # eğer son tıklamaya 1.5 saniyeden az geçtiyse müziği oynat
        if simdi - sonTik < MUSIC_TIMEOUT:
            if not muzikCaliyor:
                try:
                    # Eğer müzik pause durumundaysa unpause et; değilse play
                    if pygame.mixer.music.get_pos() > -1 and pygame.mixer.music.get_busy() == False:
                        # muhtemelen pause edilmiş, unpause
                        pygame.mixer.music.unpause()
                    else:
                        pygame.mixer.music.play(-1)
                    muzikCaliyor = True
                except Exception as e:
                    print("⚠️ Müzik çalarken hata:", e)
        else:
            # zaman aşımı olduysa müziği durdur
            if muzikCaliyor:
                try:
                    pygame.mixer.music.stop()
                except:
                    pass
                muzikCaliyor = False

    # Eğer sahne değilsek (ör. anaMenu veya upgrade) ve müzik çalıyorsa,
    # main.py daha önceki geçiş mantığı ile pause/stop yapmış olmalı; 
    # ama ekstra güvenlik:
    if aktifEkran != "sahne" and muzikCaliyor:
        try:
            pygame.mixer.music.pause()
        except:
            pass
        muzikCaliyor = False

    # --- Çizimleri güncelleme (aktif ekranın kendisi çizer) ---
    pygame.display.flip()
    saat.tick(FPS)

pygame.quit()
sys.exit()
