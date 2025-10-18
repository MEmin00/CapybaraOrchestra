import os
import sys
import pygame
import time

class Sahne:
    def __init__(self, pencere, genislik, yukseklik, oyunVerileri):

        self.yaziBaslik = pygame.font.Font(None, 60)   # Başlık fontu (ör: "Oyun Duraklatıldı")
        self.yaziButon = pygame.font.Font(None, 40)    # Buton yazıları için
        self.yaziKucuk = pygame.font.Font(None, 28)    # Küçük metinler (ör: "Ses: %50")

        self.pencere = pencere
        self.genislik = genislik
        self.yukseklik = yukseklik
        self.oyunVerileri = oyunVerileri

        # 🎨 Renkler
        self.arkaRenk = (15, 18, 45)
        self.butonRenk = (70, 70, 120)
        self.butonCerceve = (120, 120, 200)

        # 📝 Fontlar
        self.yaziFont = pygame.font.Font(None, 32)
        self.butonFont = pygame.font.Font(None, 36)
        self.baslikFont = pygame.font.Font(None, 48)

        # 🔹 Görsel yolları
        base_path = os.path.dirname(os.path.dirname(__file__))
        self.capiNormalYolu = os.path.join(base_path, "varliklar", "capibaralar", "flute.png")
        self.capiTiklamaYolu = os.path.join(base_path, "varliklar", "capibaralar", "flute1.png")
        self.muzik_yolu = os.path.join(base_path, "music", "flute.mp3")

        # 🔹 Görseller
        self.capiResimNormal = pygame.image.load(self.capiNormalYolu).convert_alpha()
        self.capiResimTiklama = pygame.image.load(self.capiTiklamaYolu).convert_alpha()

        # 🔹 Capybara boyutu yarıya düşürülüyor
        orijinal_boyut = self.capiResimNormal.get_size()
        yeni_boyut = (int(orijinal_boyut[0] * 0.2), int(orijinal_boyut[1] * 0.2))
        self.capiResimNormal = pygame.transform.scale(self.capiResimNormal, yeni_boyut)
        self.capiResimTiklama = pygame.transform.scale(self.capiResimTiklama, yeni_boyut)

        # 🔹 Başlangıç durumu
        self.capiResim = self.capiResimNormal
        self.capiRect = self.capiResim.get_rect(center=(genislik // 2, yukseklik // 2 + 120))

        # 🔹 Upgrade butonu (sağ üst)
        self.upgradeRect = pygame.Rect(genislik - 170, 20, 150, 50)
        self.upgradeRenk = (120, 120, 180)

        # 🔹 Duraklatma menüsü
        self.duraklatildi = False
        self.sesSeviyesi = 0.5

        # 🔹 Ses sistemi
        pygame.mixer.init()
        pygame.mixer.music.set_volume(self.sesSeviyesi)

        # 🔹 Zamanlayıcı değişkenleri
        self.sonTiklamaZamani = 0
        self.muzikCalıyor = False
        self.animasyonBaslamaZamani = 0
        self.animasyonSuresi = 0.3  # saniye

        # 🔹 Menü ve slider
        self.menu_genislik = int(genislik * 0.66)
        self.menu_yukseklik = int(yukseklik * 0.66)
        self.menuRect = pygame.Rect(
            genislik // 2 - self.menu_genislik // 2,
            yukseklik // 2 - self.menu_yukseklik // 2,
            self.menu_genislik,
            self.menu_yukseklik,
        )

        self.slider_genislik = 300
        self.slider_yukseklik = 10
        self.sliderRect = pygame.Rect(
            self.menuRect.centerx - self.slider_genislik // 2,
            self.menuRect.y + 135,
            self.slider_genislik,
            self.slider_yukseklik,
        )
        self.sliderTopRect = pygame.Rect(
            self.sliderRect.x + int(self.sesSeviyesi * self.slider_genislik) - 10,
            self.sliderRect.y - 5,
            20,
            20,
        )
        self.surukleniyor = False

        # 🔹 Butonlar
        self.butDevam = pygame.Rect(self.menuRect.centerx - 150, self.menuRect.y + 190, 300, 50)
        self.butKaydet = pygame.Rect(self.menuRect.centerx - 150, self.menuRect.y + 260, 300, 50)
        self.butAnaMenu = pygame.Rect(self.menuRect.centerx - 150, self.menuRect.y + 330, 300, 50)
        self.butCikis = pygame.Rect(self.menuRect.centerx - 150, self.menuRect.y + 400, 300, 50)

    def guncelle(self, events):
        simdi = time.time()

        for event in events:
            # ESC
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.duraklatildi = not self.duraklatildi

            if not self.duraklatildi:
                # 🖱️ Tıklama
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.upgradeRect.collidepoint(event.pos):
                        return "upgrade"

                    if self.capiRect.collidepoint(event.pos):
                        self.oyunVerileri["notalar"] += self.oyunVerileri["tiklamaGucu"]
                        self.sonTiklamaZamani = simdi
                        self.animasyonBaslamaZamani = simdi
                        self.capiResim = self.capiResimTiklama

                        # 🎵 Müzik başlat
                        if not self.muzikCalıyor:
                            pygame.mixer.music.load(self.muzik_yolu)
                            pygame.mixer.music.play(-1)
                            self.muzikCalıyor = True

            else:
                # 🎚️ Ses kaydırıcı
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.sliderTopRect.collidepoint(event.pos):
                        self.surukleniyor = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.surukleniyor = False
                elif event.type == pygame.MOUSEMOTION and self.surukleniyor:
                    self.sesSeviyesi = max(0, min(1, (event.pos[0] - self.sliderRect.x) / self.slider_genislik))
                    self.sliderTopRect.x = self.sliderRect.x + int(self.sesSeviyesi * self.slider_genislik) - 10
                    pygame.mixer.music.set_volume(self.sesSeviyesi)

                # Menü butonları
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.butDevam.collidepoint(event.pos):
                        self.duraklatildi = False
                    elif self.butKaydet.collidepoint(event.pos):
                        print("💾 Oyun kaydedildi (örnek).")
                    elif self.butAnaMenu.collidepoint(event.pos):
                        return "anaMenu"
                    elif self.butCikis.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

        # 🕒 1.5 sn tıklanmazsa müzik durdur
        if self.muzikCalıyor and (simdi - self.sonTiklamaZamani > 1.5):
            pygame.mixer.music.stop()
            self.muzikCalıyor = False

        # 🎬 0.3 sn sonra capybara'yı normale döndür
        if simdi - self.animasyonBaslamaZamani > self.animasyonSuresi:
            self.capiResim = self.capiResimNormal

        self.ciz()
        if self.duraklatildi:
            self.cizDuraklatmaMenusu()
        return None

    def ciz(self):
        self.pencere.fill(self.arkaRenk)

        # Notalar (sol üst)
        notYazi = self.yaziFont.render(f"Notalar: {self.oyunVerileri['notalar']}", True, (255, 255, 255))
        self.pencere.blit(notYazi, (20, 20))

        # Capybara
        self.pencere.blit(self.capiResim, self.capiRect)

        # Upgrade butonu (sağ üst)
        pygame.draw.rect(self.pencere, self.upgradeRenk, self.upgradeRect, border_radius=10)
        yazi = self.butonFont.render("Upgrade", True, (255, 255, 255))
        yazi_rect = yazi.get_rect(center=self.upgradeRect.center)
        self.pencere.blit(yazi, yazi_rect)

    def cizDuraklatmaMenusu(self):
        # --- Başlangıç ayarları ---
        if not hasattr(self, "fadeAlpha"):
            self.fadeAlpha = 0
            self.fadeIn = True
            self.fadeOut = False

        # Fade geçişi
        if self.fadeIn and self.fadeAlpha < 200:
            self.fadeAlpha += 10
        elif self.fadeOut and self.fadeAlpha > 0:
            self.fadeAlpha -= 10

        # --- Bulanık arka plan efekti ---
        # Ekran görüntüsü al
        ekran_kopya = pygame.Surface((self.genislik, self.yukseklik))
        ekran_kopya.blit(self.pencere, (0, 0))

        # Basit blur efekti (soft focus)
        blur_surface = pygame.transform.smoothscale(ekran_kopya, (self.genislik // 8, self.yukseklik // 8))
        blur_surface = pygame.transform.smoothscale(blur_surface, (self.genislik, self.yukseklik))

        # Karartma ve blur’u birleştir
        blur_surface.set_alpha(self.fadeAlpha)
        self.pencere.blit(blur_surface, (0, 0))

        # --- Menü paneli ---
        pygame.draw.rect(self.pencere, (25, 25, 40), self.menuRect, border_radius=20)
        pygame.draw.rect(self.pencere, (100, 100, 180), self.menuRect, width=3, border_radius=20)

        # --- Başlık (gölge + fade) ---
        baslikYazi = "Oyun Duraklatıldı"
        baslik = self.yaziBaslik.render(baslikYazi, True, (255, 255, 255))
        baslikGolge = self.yaziBaslik.render(baslikYazi, True, (60, 60, 100))
        baslikX = self.menuRect.centerx - baslik.get_width() // 2
        baslikY = self.menuRect.y + 30
        self.pencere.blit(baslikGolge, (baslikX + 3, baslikY + 3))
        self.pencere.blit(baslik, (baslikX, baslikY))

        # --- SLIDER bölümü ---
        mousePos = pygame.mouse.get_pos()
        mouseDown = pygame.mouse.get_pressed()[0]

        topX = self.sliderRect.x + int(self.sesSeviyesi * self.sliderRect.width)
        topY = self.sliderRect.centery
        topRadius = 9

        # Sürükleme algılama
        if mouseDown and self.sliderRect.collidepoint(mousePos):
            relX = mousePos[0] - self.sliderRect.x
            self.sesSeviyesi = max(0, min(1, relX / self.sliderRect.width))
            pygame.mixer.music.set_volume(self.sesSeviyesi)

        # Hover efekti
        if (mousePos[0] - topX) ** 2 + (mousePos[1] - topY) ** 2 <= topRadius ** 2 * 2:
            topRenk = (220, 220, 255)
            pygame.draw.circle(self.pencere, (160, 160, 255), (topX, topY), 13)
        else:
            topRenk = (180, 180, 255)

        # Slider çizimi
        pygame.draw.rect(self.pencere, (90, 90, 160), self.sliderRect, border_radius=10)
        pygame.draw.circle(self.pencere, topRenk, (topX, topY), topRadius)

        # Ses yüzdesi
        sesYazi = self.yaziKucuk.render(f"Ses: %{int(self.sesSeviyesi * 100)}", True, (255, 255, 255))
        self.pencere.blit(sesYazi, (self.sliderRect.centerx - sesYazi.get_width() // 2, self.sliderRect.y - 35))

        # --- BUTONLAR ---
        for yazi, butonRect in [
            ("Devam Et", self.butDevam),
            ("Kaydet", self.butKaydet),
            ("Ana Menüye Dön", self.butAnaMenu),
            ("Çıkış", self.butCikis),
        ]:
            hover = butonRect.collidepoint(mousePos)
            renk = (120, 120, 200) if hover else (90, 90, 160)
            if hover and mouseDown:
                renk = (160, 160, 240)

            pygame.draw.rect(self.pencere, renk, butonRect, border_radius=10)
            pygame.draw.rect(self.pencere, (180, 180, 255), butonRect, 2, border_radius=10)

            yaziYuzeyi = self.yaziButon.render(yazi, True, (255, 255, 255))
            self.pencere.blit(
                yaziYuzeyi,
                (butonRect.centerx - yaziYuzeyi.get_width() // 2, butonRect.centery - yaziYuzeyi.get_height() // 2)
            )



    def cizButon(self, rect, metin):
        pygame.draw.rect(self.pencere, self.butonRenk, rect, border_radius=10)
        pygame.draw.rect(self.pencere, self.butonCerceve, rect, width=2, border_radius=10)
        yazi = self.butonFont.render(metin, True, (255, 255, 255))
        self.pencere.blit(yazi, yazi.get_rect(center=rect.center))