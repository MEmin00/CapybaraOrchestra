import os
import sys
import pygame
import time
from oyun.kayanMetin import KayanMetin

class Sahne:
    def __init__(self, pencere, genislik, yukseklik, oyunVerileri, kayan_metinler):
        self.yaziBaslik = pygame.font.Font(None, 60)
        self.yaziButon = pygame.font.Font(None, 40)
        self.yaziKucuk = pygame.font.Font(None, 28)

        self.pencere = pencere
        self.genislik = genislik
        self.yukseklik = yukseklik
        self.oyunVerileri = oyunVerileri
        self.kayan_metinler = kayan_metinler  

        # Renkler
        self.arkaRenk = (15, 18, 45)
        self.upgradeRenk = (120, 120, 180)

        # Fontlar
        self.yaziFont = pygame.font.Font(None, 32)
        self.butonFont = pygame.font.Font(None, 36)
        self.baslikFont = pygame.font.Font(None, 48)

        # Görsel yollar
        base_path = os.path.dirname(os.path.dirname(__file__))
        self.capiNormalYolu = os.path.join(base_path, "varliklar", "capibaralar", "flute.png")
        self.capiTiklamaYolu = os.path.join(base_path, "varliklar", "capibaralar", "flute1.png")
        self.muzik_yolu = os.path.join(base_path, "varliklar", "ses", "flute.mp3")

        # Görseller
        self.capiResimNormal = pygame.image.load(self.capiNormalYolu).convert_alpha()
        self.capiResimTiklama = pygame.image.load(self.capiTiklamaYolu).convert_alpha()

        orijinal_boyut = self.capiResimNormal.get_size()
        yeni_boyut = (int(orijinal_boyut[0] * 0.2), int(orijinal_boyut[1] * 0.2))
        self.capiResimNormal = pygame.transform.scale(self.capiResimNormal, yeni_boyut)
        self.capiResimTiklama = pygame.transform.scale(self.capiResimTiklama, yeni_boyut)

        self.capiResim = self.capiResimNormal
        self.capiRect = self.capiResim.get_rect(center=(genislik // 2, yukseklik // 2 + 120))

        # Upgrade butonu
        self.upgradeRect = pygame.Rect(genislik - 170, 20, 150, 50)

        # Duraklatma
        self.duraklatildi = False
        self.sesSeviyesi = 0.5

        pygame.mixer.init()
        pygame.mixer.music.set_volume(self.sesSeviyesi)

        # Ses ve zaman yönetimi
        self.muzikCalıyor = False
        self.muzik_pozisyon = 0.0  # müzikteki kaldığı yer (saniye)
        self.sonTiklamaZamani = 0
        self.animasyonBaslamaZamani = 0
        self.animasyonSuresi = 0.3

        # Menü
        self.menu_genislik = int(genislik * 0.66)
        self.menu_yukseklik = int(yukseklik * 0.66)
        self.menuRect = pygame.Rect(
            genislik // 2 - self.menu_genislik // 2,
            yukseklik // 2 - self.menu_yukseklik // 2,
            self.menu_genislik,
            self.menu_yukseklik,
        )

        self.slider_genislik = 300
        self.sliderRect = pygame.Rect(
            self.menuRect.centerx - self.slider_genislik // 2,
            self.menuRect.y + 135,
            self.slider_genislik,
            10,
        )
        self.sliderTopRect = pygame.Rect(
            self.sliderRect.x + int(self.sesSeviyesi * self.slider_genislik) - 10,
            self.sliderRect.y - 5,
            20,
            20,
        )

        # Butonlar
        self.butDevam = pygame.Rect(self.menuRect.centerx - 150, self.menuRect.y + 190, 300, 50)
        self.butKaydet = pygame.Rect(self.menuRect.centerx - 150, self.menuRect.y + 260, 300, 50)
        self.butAnaMenu = pygame.Rect(self.menuRect.centerx - 150, self.menuRect.y + 330, 300, 50)
        self.butCikis = pygame.Rect(self.menuRect.centerx - 150, self.menuRect.y + 400, 300, 50)

    def muzik_baslat(self):
        pygame.mixer.music.load(self.muzik_yolu)
        pygame.mixer.music.play(-1, self.muzik_pozisyon)
        self.muzikCalıyor = True
        self.muzik_baslama_zamani = time.time()

    def muzik_durdur(self):
        if self.muzikCalıyor:
            self.muzik_pozisyon += time.time() - self.muzik_baslama_zamani
            pygame.mixer.music.stop()
            self.muzikCalıyor = False

    def guncelle(self, events):
        simdi = time.time()

        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.duraklatildi = not self.duraklatildi
                if self.duraklatildi:
                    self.muzik_durdur()  # ESC'ye basınca müzik dursun
                else:
                    if self.muzikCalıyor is False and self.muzik_pozisyon > 0:
                        self.muzik_baslat()

            if not self.duraklatildi:
                # Tıklama
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.upgradeRect.collidepoint(event.pos):
                        return "upgrade"

                    if self.capiRect.collidepoint(event.pos):
                        kazanc = self.oyunVerileri["tiklamaGucu"]
                        self.oyunVerileri["notalar"] += kazanc
                        self.sonTiklamaZamani = simdi
                        self.animasyonBaslamaZamani = simdi
                        self.capiResim = self.capiResimTiklama

                        self.kayan_metinler.append(KayanMetin(f"+{kazanc}", event.pos))

                        if not self.muzikCalıyor:
                            self.muzik_baslat()

            else:
                # Menüdeyken ses slider'ı
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.sliderTopRect.collidepoint(event.pos):
                        self.surukleniyor = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.surukleniyor = False
                elif event.type == pygame.MOUSEMOTION and getattr(self, "surukleniyor", False):
                    self.sesSeviyesi = max(0, min(1, (event.pos[0] - self.sliderRect.x) / self.sliderRect.width))
                    self.sliderTopRect.x = self.sliderRect.x + int(self.sesSeviyesi * self.sliderRect.width) - 10
                    pygame.mixer.music.set_volume(self.sesSeviyesi)

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.butDevam.collidepoint(event.pos):
                        self.duraklatildi = False
                        if self.muzikCalıyor is False and self.muzik_pozisyon > 0:
                            self.muzik_baslat()
                    elif self.butAnaMenu.collidepoint(event.pos):
                        self.muzik_durdur()
                        return "anaMenu"
                    elif self.butCikis.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

        # Müzik zamanlayıcı
        if self.muzikCalıyor and (simdi - self.sonTiklamaZamani > 1.5):
            self.muzik_durdur()

        # Capybara animasyonu
        if simdi - self.animasyonBaslamaZamani > self.animasyonSuresi:
            self.capiResim = self.capiResimNormal

        for metin in self.kayan_metinler[:]:
            metin.guncelle()
            if metin.bitti:
                self.kayan_metinler.remove(metin)

        self.ciz()
        if self.duraklatildi:
            self.cizDuraklatmaMenusu()
        return None

    def ciz(self):
        self.pencere.fill(self.arkaRenk)
        notYazi = self.yaziFont.render(f"Notalar: {self.oyunVerileri['notalar']}", True, (255, 255, 255))
        self.pencere.blit(notYazi, (20, 20))
        self.pencere.blit(self.capiResim, self.capiRect)
        pygame.draw.rect(self.pencere, self.upgradeRenk, self.upgradeRect, border_radius=10)
        yazi = self.butonFont.render("Upgrade", True, (255, 255, 255))
        self.pencere.blit(yazi, yazi.get_rect(center=self.upgradeRect.center))
        for metin in self.kayan_metinler:
            metin.ciz(self.pencere)

    def cizDuraklatmaMenusu(self):
        pygame.draw.rect(self.pencere, (25, 25, 40), self.menuRect, border_radius=20)
        pygame.draw.rect(self.pencere, (100, 100, 180), self.menuRect, width=3, border_radius=20)

        baslik = self.yaziBaslik.render("Oyun Duraklatıldı", True, (255, 255, 255))
        self.pencere.blit(baslik, (self.menuRect.centerx - baslik.get_width() // 2, self.menuRect.y + 30))

        topX = self.sliderRect.x + int(self.sesSeviyesi * self.sliderRect.width)
        topY = self.sliderRect.centery
        pygame.draw.rect(self.pencere, (90, 90, 160), self.sliderRect, border_radius=10)
        pygame.draw.circle(self.pencere, (200, 200, 255), (topX, topY), 9)

        sesYazi = self.yaziKucuk.render(f"Ses: %{int(self.sesSeviyesi * 100)}", True, (255, 255, 255))
        self.pencere.blit(sesYazi, (self.sliderRect.centerx - sesYazi.get_width() // 2, self.sliderRect.y - 35))

        for yazi, butonRect in [
            ("Devam Et", self.butDevam),
            ("Kaydet", self.butKaydet),
            ("Ana Menüye Dön", self.butAnaMenu),
            ("Çıkış", self.butCikis),
        ]:
            pygame.draw.rect(self.pencere, (100, 100, 200), butonRect, border_radius=10)
            pygame.draw.rect(self.pencere, (180, 180, 255), butonRect, 2, border_radius=10)
            yaziYuzeyi = self.yaziButon.render(yazi, True, (255, 255, 255))
            self.pencere.blit(
                yaziYuzeyi,
                (butonRect.centerx - yaziYuzeyi.get_width() // 2, butonRect.centery - yaziYuzeyi.get_height() // 2)
            )
