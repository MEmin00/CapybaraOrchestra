import pygame
import os
import sys

class Sahne:
    def __init__(self, pencere, genislik, yukseklik, oyunVerileri):
        self.pencere = pencere
        self.genislik = genislik
        self.yukseklik = yukseklik
        self.oyunVerileri = oyunVerileri

        # Görsel yollarını proje kökünden çöz
        projeKok = os.path.dirname(os.path.abspath(sys.argv[0]))
        self.yolNormal = os.path.join(projeKok, "varliklar", "capybaralar", "flute.png")
        self.yolTiklama = os.path.join(projeKok, "varliklar", "capybaralar", "flute1.png")

        # Yükleme güvenli
        self.capibaraGorselNormal = self.gorselYukle(self.yolNormal)
        self.capibaraGorselTiklama = self.gorselYukle(self.yolTiklama)
        self.capibaraGorselNormal = pygame.transform.scale(self.capibaraGorselNormal, (200, 200))
        self.capibaraGorselTiklama = pygame.transform.scale(self.capibaraGorselTiklama, (200, 200))

        self.aktifGorsel = self.capibaraGorselNormal
        self.capibaraRect = self.aktifGorsel.get_rect(center=(self.genislik // 2, self.yukseklik // 2))

        # Upgrade butonu sahnede
        self.upgradeButon = pygame.Rect(self.genislik - 200, 20, 160, 50)
        self.butunYaziTipi = pygame.font.SysFont("arial", 28)

        # Zamanlama
        self.tiklamaAktif = False
        self.tiklamaZaman = 0
        self.tiklamaSure = 100  # ms

        # Görsel
        self.renkArkaPlan = (40, 50, 70)
        self.yaziTipi = pygame.font.SysFont("arial", 36)

    def gorselYukle(self, yol):
        try:
            return pygame.image.load(yol).convert_alpha()
        except Exception as hata:
            print("⚠️ Görsel yüklenemedi:", yol, "→", hata)
            yuzey = pygame.Surface((200, 200), pygame.SRCALPHA)
            yuzey.fill((200, 50, 50))
            return yuzey

    def guncelle(self, events):
        # Olayları events listesi üzerinden işle
        for olay in events:
            if olay.type == pygame.KEYDOWN and olay.key == pygame.K_ESCAPE:
                return "anaMenu"  # ESC ile ana menüye dön

            if olay.type == pygame.MOUSEBUTTONDOWN and olay.button == 1:
                fare = pygame.mouse.get_pos()
                # Capibara tıklaması
                if self.capibaraRect.collidepoint(fare):
                    self.oyunVerileri["notalar"] += self.oyunVerileri["tiklamaGucu"]
                    # tıklama animasyonu
                    self.aktifGorsel = self.capibaraGorselTiklama
                    self.tiklamaAktif = True
                    self.tiklamaZaman = pygame.time.get_ticks()
                # Upgrade butonu tıklaması
                if self.upgradeButon.collidepoint(fare):
                    return "upgrade"

        # Zamanlama: animasyonu geri al
        if self.tiklamaAktif:
            simdi = pygame.time.get_ticks()
            if simdi - self.tiklamaZaman >= self.tiklamaSure:
                self.aktifGorsel = self.capibaraGorselNormal
                self.tiklamaAktif = False

        # Çizimler
        self.pencere.fill(self.renkArkaPlan)
        self.pencere.blit(self.aktifGorsel, self.capibaraRect)

        # Upgrade butonu çiz
        renkButon = (150, 150, 200) if self.upgradeButon.collidepoint(pygame.mouse.get_pos()) else (110, 110, 150)
        pygame.draw.rect(self.pencere, renkButon, self.upgradeButon, border_radius=10)
        self.pencere.blit(self.butunYaziTipi.render("Upgrade", True, (255, 255, 255)), (self.upgradeButon.x + 25, self.upgradeButon.y + 12))

        # Nota sayısı göster
        notaMetni = self.yaziTipi.render(f"Notalar: {self.oyunVerileri['notalar']}", True, (255, 255, 255))
        self.pencere.blit(notaMetni, (20, 20))

        return None
