import pygame
from oyun.arayuz import Buton

class AnaMenu:
    def __init__(self, pencere, genislik, yukseklik, oyunVerileri):
        self.pencere = pencere
        self.genislik = genislik
        self.yukseklik = yukseklik
        self.oyunVerileri = oyunVerileri

        # Renkler
        self.renkArkaPlan = (30, 30, 40)
        self.renkBaslik = (255, 255, 255)

        # Font
        self.yaziTipi = pygame.font.SysFont("arial", 64)
        self.baslikYazisi = self.yaziTipi.render("Capybara Konseri 🎶", True, self.renkBaslik)

        # Butonlar
        self.butBasla = Buton("Başla", genislik // 2 - 100, 300, 200, 60)
        self.butCikis = Buton("Çıkış", genislik // 2 - 100, 400, 200, 60)

    def guncelle(self, events):
        # Çizimler
        self.pencere.fill(self.renkArkaPlan)
        self.pencere.blit(self.baslikYazisi, (self.genislik // 2 - self.baslikYazisi.get_width() // 2, 150))

        # Buton kontrolü (arayuz.Butons kullanan cizVeKontrol artık sadece çiziyor, 
        # tıklamaları burada events ile kontrol ediyoruz)
        baslaTik = self.butBasla.cizVeKontrol(self.pencere)
        cikisTik = self.butCikis.cizVeKontrol(self.pencere)

        # events üzerinden tıklama kontrollerini yap (Buton içinde mouse pressed yerine)
        for olay in events:
            if olay.type == pygame.MOUSEBUTTONDOWN and olay.button == 1:
                fare = pygame.mouse.get_pos()
                if self.butBasla.rect.collidepoint(fare):
                    return "sahne"
                if self.butCikis.rect.collidepoint(fare):
                    pygame.quit()
                    return None  # main loop QUIT event ile çıkacak

        return None