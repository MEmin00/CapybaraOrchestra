import pygame
from oyun.arayuz import Buton

import os

class AnaMenu:
    def __init__(self, pencere, genislik, yukseklik, oyunVerileri):
        self.pencere = pencere
        self.genislik = genislik
        self.yukseklik = yukseklik
        self.oyunVerileri = oyunVerileri

        # Görsel yollar
        base_path = os.path.dirname(os.path.dirname(__file__))
        self.arkaplanYolu = os.path.join(base_path, "varliklar", "capibaralar", "giris.png")

        # Arkaplan Resmi
        try:
            self.arkaplanResmi = pygame.image.load(self.arkaplanYolu).convert()
            self.arkaplanResmi = pygame.transform.scale(self.arkaplanResmi, (genislik, yukseklik))
            print("AnaMenu: Arkaplan yüklendi.")
        except Exception as e:
            print("AnaMenu: Arkaplan yüklenemedi, renk kullanılacak:", e)
            self.arkaplanResmi = None

        # Renkler
        self.renkArkaPlan = (30, 30, 40)
        self.renkBaslik = (255, 255, 255)

        # Font
        self.yaziTipi = pygame.font.SysFont("arial", 64)
        self.baslikYazisi = self.yaziTipi.render("Capybara Orchestra", True, self.renkBaslik)

        # Buton Görsel
        self.butonResmi = None
        butonYolu = os.path.join(base_path, "varliklar", "capibaralar", "buton.png")
        if os.path.exists(butonYolu):
            try:
                self.butonResmi = pygame.image.load(butonYolu).convert_alpha()
            except Exception as e:
                print("AnaMenu: Buton görseli yüklenemedi:", e)

        # Buton
        self.butBasla = Buton("Başla", genislik // 2 - 100, 300, 200, 60, resim=self.butonResmi)
        self.butCikis = Buton("Çıkış", genislik // 2 - 100, 400, 200, 60, resim=self.butonResmi)

    def guncelle(self, events):
        # Çizim
        if self.arkaplanResmi:
            self.pencere.blit(self.arkaplanResmi, (0, 0))
        else:
            self.pencere.fill(self.renkArkaPlan)

        baslaTik = self.butBasla.cizVeKontrol(self.pencere)
        cikisTik = self.butCikis.cizVeKontrol(self.pencere)

        for olay in events:
            if olay.type == pygame.MOUSEBUTTONDOWN and olay.button == 1:
                fare = pygame.mouse.get_pos()
                if self.butBasla.rect.collidepoint(fare):
                    return "sahne"
                if self.butCikis.rect.collidepoint(fare):
                    pygame.quit()
                    return None

        return None