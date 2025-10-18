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
        self.kayan_metinler = kayan_metinler  # 🌟

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
        # müzik yolu sadece bilgi amaçlı tutulabilir
        self.muzik_yolu = os.path.join(base_path, "varliklar", "ses", "flute.mp3")

        # 🔹 Görseller
        self.capiResimNormal = pygame.image.load(self.capiNormalYolu).convert_alpha()
        self.capiResimTiklama = pygame.image.load(self.capiTiklamaYolu).convert_alpha()

        # 🔹 Capybara boyutu
        orijinal_boyut = self.capiResimNormal.get_size()
        yeni_boyut = (int(orijinal_boyut[0] * 0.2), int(orijinal_boyut[1] * 0.2))
        self.capiResimNormal = pygame.transform.scale(self.capiResimNormal, yeni_boyut)
        self.capiResimTiklama = pygame.transform.scale(self.capiResimTiklama, yeni_boyut)

        # 🔹 Başlangıç durumu
        self.capiResim = self.capiResimNormal
        self.capiRect = self.capiResim.get_rect(center=(genislik // 2, yukseklik // 2 + 120))

        # 🔹 Upgrade butonu
        self.upgradeRect = pygame.Rect(genislik - 170, 20, 150, 50)
        self.upgradeRenk = (120, 120, 180)

        # 🔹 Duraklatma menüsü
        self.duraklatildi = False
        self.sesSeviyesi = 0.5

        # 🔹 Zamanlayıcı değişkenleri
        self.sonTiklamaZamani = 0.0
        self.animasyonBaslamaZamani = 0.0
        self.animasyonSuresi = 0.3

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
                        kazanc = self.oyunVerileri["tiklamaGucu"]
                        self.oyunVerileri["notalar"] += kazanc
                        # son tıklama zamanı burada global oyunVerileri'ye yazılsın
                        self.oyunVerileri["sonTiklamaZamani"] = simdi
                        self.sonTiklamaZamani = simdi
                        self.animasyonBaslamaZamani = simdi
                        self.capiResim = self.capiResimTiklama

                        # 🌟 Kayan yazı ekle
                        self.kayan_metinler.append(KayanMetin(f"+{kazanc}", event.pos))

            else:
                # Slider ve menü butonları (aynı kaldı)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.sliderTopRect.collidepoint(event.pos):
                        self.surukleniyor = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.surukleniyor = False
                elif event.type == pygame.MOUSEMOTION and self.surukleniyor:
                    self.sesSeviyesi = max(0, min(1, (event.pos[0] - self.sliderRect.x) / self.slider_genislik))
                    self.sliderTopRect.x = self.sliderRect.x + int(self.sesSeviyesi * self.slider_genislik) - 10
                    # dikkat: müziği main.py kontrol ettiğinden mixer çağrıları burada yapılmasın
                    try:
                        if pygame.mixer.get_init():
                            pygame.mixer.music.set_volume(self.sesSeviyesi)
                    except:
                        pass

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

        # 🎬 0.3 sn sonra capybara'yı normale döndür
        if simdi - self.animasyonBaslamaZamani > self.animasyonSuresi:
            self.capiResim = self.capiResimNormal

        # Kayan yazıları güncelle
        for metin in self.kayan_metinler[:]:
            metin.guncelle()
            if metin.bitti:
                self.kayan_metinler.remove(metin)

        # çizimler
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

        # Upgrade butonu
        pygame.draw.rect(self.pencere, self.upgradeRenk, self.upgradeRect, border_radius=10)
        yazi = self.butonFont.render("Upgrade", True, (255, 255, 255))
        yazi_rect = yazi.get_rect(center=self.upgradeRect.center)
        self.pencere.blit(yazi, yazi_rect)

        # Kayan metinler
        for metin in self.kayan_metinler:
            metin.ciz(self.pencere)

    def cizDuraklatmaMenusu(self):
        ekran_kopya = pygame.Surface((self.genislik, self.yukseklik))
        ekran_kopya.blit(self.pencere, (0, 0))
        blur_surface = pygame.transform.smoothscale(ekran_kopya, (self.genislik // 8, self.yukseklik // 8))
        blur_surface = pygame.transform.smoothscale(blur_surface, (self.genislik, self.yukseklik))
        blur_surface.set_alpha(180)
        self.pencere.blit(blur_surface, (0, 0))

        pygame.draw.rect(self.pencere, (25, 25, 40), self.menuRect, border_radius=20)
        pygame.draw.rect(self.pencere, (100, 100, 180), self.menuRect, width=3, border_radius=20)

        baslikYazi = "Oyun Duraklatıldı"
        baslik = self.yaziBaslik.render(baslikYazi, True, (255, 255, 255))
        self.pencere.blit(baslik, (self.menuRect.centerx - baslik.get_width() // 2, self.menuRect.y + 30))

        mousePos = pygame.mouse.get_pos()
        mouseDown = pygame.mouse.get_pressed()[0]

        # Slider çizimi
        topX = self.sliderRect.x + int(self.sesSeviyesi * self.sliderRect.width)
        topY = self.sliderRect.centery
        pygame.draw.rect(self.pencere, (90, 90, 160), self.sliderRect, border_radius=10)
        pygame.draw.circle(self.pencere, (180, 180, 255), (topX, topY), 9)

        sesYazi = self.yaziKucuk.render(f"Ses: %{int(self.sesSeviyesi * 100)}", True, (255, 255, 255))
        self.pencere.blit(sesYazi, (self.sliderRect.centerx - sesYazi.get_width() // 2, self.sliderRect.y - 35))

        # Butonlar
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
