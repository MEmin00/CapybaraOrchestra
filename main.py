import pygame
import sys
from oyun.anaMenu import AnaMenu
from oyun.sahne import Sahne
from oyun.upgrade import UpgradeEkrani

pygame.init()

# Pencere ayarları
GENISLIK, YUKSEKLIK = 1280, 720
pencere = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
pygame.display.set_caption("Capybara Konseri 🎶")

saat = pygame.time.Clock()
FPS = 60

# Oyun verileri (tek kaynak)
oyunVerileri = {
    "notalar": 0,
    "tiklamaGucu": 1,
    "capibaraSayisi": 1,
    # ileride eklenecekler: alinanCapibaralar, sahneDekor, sesSeviyesi, vs.
}

# Ekran nesneleri (oyunVerileri referansını geçiriyoruz)
anaMenu = AnaMenu(pencere, GENISLIK, YUKSEKLIK, oyunVerileri)
sahne = Sahne(pencere, GENISLIK, YUKSEKLIK, oyunVerileri)
upgradeEkrani = UpgradeEkrani(pencere, GENISLIK, YUKSEKLIK, oyunVerileri)

aktifEkran = "anaMenu"  # ana menüyü başlangıç yapıyoruz

calisiyor = True
while calisiyor:
    # Olayları sadece burada çekiyoruz
    events = pygame.event.get()

    # Global çıkış kontrolü
    for olay in events:
        if olay.type == pygame.QUIT:
            calisiyor = False

    # Ekranlara olay listesi vererek güncelle
    if aktifEkran == "anaMenu":
        yeniEkran = anaMenu.guncelle(events)
        if yeniEkran:
            aktifEkran = yeniEkran

    elif aktifEkran == "sahne":
        yeniEkran = sahne.guncelle(events)
        if yeniEkran:
            aktifEkran = yeniEkran

    elif aktifEkran == "upgrade":
        yeniEkran = upgradeEkrani.guncelle(events)
        if yeniEkran:
            aktifEkran = yeniEkran

    pygame.display.flip()
    saat.tick(FPS)

pygame.quit()
sys.exit()