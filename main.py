import pygame
import sys
from oyun.anaMenu import AnaMenu
from oyun.sahne import Sahne
from oyun.upgrade import UpgradeEkrani

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
}

# --- Ekran nesneleri ---
anaMenu = AnaMenu(pencere, GENISLIK, YUKSEKLIK, oyunVerileri)
sahne = Sahne(pencere, GENISLIK, YUKSEKLIK, oyunVerileri)
upgradeEkrani = UpgradeEkrani(pencere, GENISLIK, YUKSEKLIK, oyunVerileri)

aktifEkran = "anaMenu"  # Başlangıç ekranı

# --- Ana döngü ---
calisiyor = True
while calisiyor:
    events = pygame.event.get()

    for olay in events:
        if olay.type == pygame.QUIT:
            calisiyor = False

    yeniEkran = None

    # --- Ekran geçişleri ---
    if aktifEkran == "anaMenu":
        yeniEkran = anaMenu.guncelle(events)

    elif aktifEkran == "sahne":
        yeniEkran = sahne.guncelle(events)

    elif aktifEkran == "upgrade":
        yeniEkran = upgradeEkrani.guncelle(events)

    # --- Eğer yeni ekran döndüyse geçiş yap ---
    if yeniEkran:
        aktifEkran = yeniEkran

    # --- Güncelleme ---
    pygame.display.flip()
    saat.tick(FPS)

pygame.quit()
sys.exit()