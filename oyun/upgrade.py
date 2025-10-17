import pygame
import sys

class UpgradeEkrani:
    def __init__(self, pencere, genislik, yukseklik, oyunVerileri):
        self.pencere = pencere
        self.genislik = genislik
        self.yukseklik = yukseklik
        self.oyunVerileri = oyunVerileri

        self.renkArkaPlan = (30, 35, 55)
        self.yaziTipi = pygame.font.SysFont("arial", 30)
        self.yaziKucuk = pygame.font.SysFont("arial", 22)

        # Upgrade listesi (örnek)
        self.upgradeListesi = [
            {"isim": "Gitar Capibara", "fiyat": 100, "artis": 1, "alindi": False, "kod": "gitar"},
            {"isim": "Davul Capibara", "fiyat": 300, "artis": 3, "alindi": False, "kod": "davul"},
            {"isim": "Tıklama Gücü +1", "fiyat": 50, "artis": 1, "tekrarAlinabilir": True, "kod": "tikGucu"},
            {"isim": "Sahne Dekor: Işık", "fiyat": 200, "artis": 10, "alindi": False, "kod": "dekorIsik"}  # örnek: dekorlar tıklama kazancına etki eder
        ]

        # Buton boyutu
        self.butongen = 600
        self.butonyuk = 60
        self.baslangicY = 180
        self.aralik = 80

        self.yaziKucuk2 = pygame.font.SysFont("arial", 18)

    def guncelle(self, events):
        for olay in events:
            if olay.type == pygame.KEYDOWN and olay.key == pygame.K_ESCAPE:
                return "sahne"  # geri dön

            if olay.type == pygame.MOUSEBUTTONDOWN and olay.button == 1:
                fare = pygame.mouse.get_pos()
                # Buton tıklamalarını kontrol et
                for upgrade in self.upgradeListesi:
                    if "rect" in upgrade and upgrade["rect"].collidepoint(fare):
                        self.satinAl(upgrade)

        # Çizimler
        self.pencere.fill(self.renkArkaPlan)
        baslik = self.yaziTipi.render("🎵 Upgrade Mağazası 🎵", True, (255, 255, 255))
        self.pencere.blit(baslik, (self.genislik // 2 - baslik.get_width() // 2, 80))

        notaYazi = self.yaziKucuk.render(f"Notalar: {self.oyunVerileri['notalar']}", True, (255, 255, 100))
        self.pencere.blit(notaYazi, (30, 30))

        # Butonları çiz
        for i, upgrade in enumerate(self.upgradeListesi):
            y = self.baslangicY + i * self.aralik
            self.cizUpgrade(upgrade, y)

        # Bilgi notu
        info = self.yaziKucuk2.render("ESC ile geri dön", True, (200, 200, 200))
        self.pencere.blit(info, (self.genislik - 180, self.yukseklik - 40))

        return None

    def cizUpgrade(self, upgrade, y):
        fare = pygame.mouse.get_pos()
        buton = pygame.Rect(self.genislik // 2 - self.butongen // 2, y, self.butongen, self.butonyuk)
        renk = (80, 80, 120) if buton.collidepoint(fare) else (60, 60, 90)
        pygame.draw.rect(self.pencere, renk, buton, border_radius=15)

        isim = upgrade["isim"]
        fiyat = upgrade["fiyat"]
        alindi = upgrade.get("alindi", False)
        yazi = f"{isim} - {fiyat} Nota"
        if alindi and not upgrade.get("tekrarAlinabilir", False):
            yazi += " ✅"

        metin = self.yaziKucuk.render(yazi, True, (255, 255, 255))
        self.pencere.blit(metin, (buton.x + 20, buton.y + 18))

        upgrade["rect"] = buton

    def satinAl(self, upgrade):
        # Para kontrolü
        if self.oyunVerileri["notalar"] < upgrade["fiyat"]:
            # yetersiz bakiye — istersen ses/effect ekle
            return

        # Tek seferlik alındıysa tekrar alınamaz
        if upgrade.get("alindi", False) and not upgrade.get("tekrarAlinabilir", False):
            return

        # Ödeme
        self.oyunVerileri["notalar"] -= upgrade["fiyat"]

        # Etki
        kod = upgrade.get("kod", "")
        if kod == "tikGucu":
            # tıklama gücünü arttır, fiyatı %30 artır
            self.oyunVerileri["tiklamaGucu"] += upgrade["artis"]
            upgrade["fiyat"] = int(upgrade["fiyat"] * 1.3)
        elif kod in ("gitar", "davul"):
            # tek seferlik capibara ekle ve tıklama gücünü arttır
            self.oyunVerileri["capibaraSayisi"] += 1
            self.oyunVerileri["tiklamaGucu"] += upgrade["artis"]
            upgrade["alindi"] = True
        elif kod.startswith("dekor"):
            # dekorlar tıklama kazancına etki edebilir
            self.oyunVerileri["tiklamaGucu"] += int(upgrade.get("artis", 0) / 10)  # örnek uygulama
            upgrade["alindi"] = True