import pygame
import os

class UpgradeEkrani:
    def __init__(self, pencere, GENISLIK, YUKSEKLIK, oyunVerileri):
        self.pencere = pencere
        self.GENISLIK = GENISLIK
        self.YUKSEKLIK = YUKSEKLIK
        self.oyunVerileri = oyunVerileri

        self.alpha = 150

        # Fontlar
        self.fontBaslik = pygame.font.SysFont("Palatino Linotype", 48, bold=True)
        self.fontKucuk = pygame.font.SysFont("Palatino Linotype", 24, bold=True)

        # Görsel yolu
        base_path = os.path.dirname(os.path.dirname(__file__))

        # Menü arkaplanları
        self.pauseResmi = None
        pauseYolu = os.path.join(base_path, "varliklar", "kullaniciArayuzu", "pause.png")
        if os.path.exists(pauseYolu):
            try:
                self.pauseResmi = pygame.image.load(pauseYolu).convert_alpha()
            except Exception as e:
                print("Upgrade: Pause resmi yüklenemedi:", e)

        # Menü paneli
        self.menuGenislik = int(GENISLIK * 0.66)
        self.menuYukseklik = int(YUKSEKLIK * 0.66)
        self.menuRect = pygame.Rect(
            (GENISLIK - self.menuGenislik) // 2,
            (YUKSEKLIK - self.menuYukseklik) // 2,
            self.menuGenislik,
            self.menuYukseklik
        )

        
        self.gorseller = []
        self.gorseller = []
        for u in self.oyunVerileri["upgrades"]:
            try:
                img = pygame.image.load(u["resim"]).convert_alpha()
                img = pygame.transform.scale(img, (120, 120))
                self.gorseller.append(img)
            except Exception as e:
                print(f"Görsel yüklenemedi: {u['resim']}, hata: {e}")
                self.gorseller.append(pygame.Surface((120, 120)))

        # Tik işareti
        try:
            self.tik = pygame.image.load("varliklar/kullaniciArayuzu/tik.png").convert_alpha()
            self.tik = pygame.transform.scale(self.tik, (40, 40))
        except Exception as e:
            print("Tik resmi yüklenemedi:", e)
            self.tik = None

        # Satın alma sesi
        try:
            self.ses_satinal = pygame.mixer.Sound("varliklar/ses/upgrade.mp3")
            self.ses_satinal.set_volume(0.6)
        except Exception as e:
            print("Ses yüklenemedi:", e)
            self.ses_satinal = None

        # Kapat butonu
        self.kapat_buton = pygame.Rect(self.menuRect.right - 45, self.menuRect.y + 15, 30, 30)

        # Scroll
        self.scroll_offset = 0
        self.scroll_hiz = 40
        self.scroll_max = 0

    # --------------------------------------------------------
    def guncelle(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                return "sahne"

            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 4:
                    self.scroll_offset = min(self.scroll_offset + self.scroll_hiz, 0)
                elif e.button == 5:
                    self.scroll_offset = max(self.scroll_offset - self.scroll_hiz, -self.scroll_max)
                elif e.button == 1:
                    if self.kapat_buton.collidepoint(e.pos):
                        return "sahne"
                    self.upgradeTiklama(e.pos)

        self.ciz()
        return None

    # --------------------------------------------------------
    def ciz(self):

        # Menü paneli
        if self.pauseResmi:
            img_rect = self.pauseResmi.get_rect(center=self.menuRect.center)
            self.pencere.blit(self.pauseResmi, img_rect)
        else:
            pygame.draw.rect(self.pencere, (30, 30, 50), self.menuRect, border_radius=20)
            pygame.draw.rect(self.pencere, (120, 120, 200), self.menuRect, 3, border_radius=20)

        # Başlık
        baslik = self.fontBaslik.render("Yükseltmeler", True, (255, 255, 255))
        self.pencere.blit(baslik, (self.menuRect.centerx - baslik.get_width() // 2, self.menuRect.y + 30))

        # Notalar
        notaYazi = self.fontKucuk.render(f"Toplam Notalar: {self.oyunVerileri['notalar']}", True, (255, 255, 0))
        self.pencere.blit(notaYazi, (self.menuRect.centerx - notaYazi.get_width() // 2, self.menuRect.y + 100))

        # Görünebilir alan
        clip_rect = pygame.Rect(
            self.menuRect.x,
            self.menuRect.y + 150,
            self.menuRect.width - 20,
            self.menuRect.height - 170
        )
        self.pencere.set_clip(clip_rect)

        self.upgradeRectList = []
        start_y = self.menuRect.y + 160 + self.scroll_offset
        start_y = self.menuRect.y + 160 + self.scroll_offset
        toplam_icerik_yuksekligi = len(self.oyunVerileri["upgrades"]) * 160
        gorunen_alan = clip_rect.height
        self.scroll_max = max(0, toplam_icerik_yuksekligi - gorunen_alan)

        mouse_pos = pygame.mouse.get_pos()

        for i, u in enumerate(self.oyunVerileri["upgrades"]):
            rect = pygame.Rect(self.menuRect.x + 80, start_y, self.menuRect.width - 160, 120)
            start_y += 160
            if rect.bottom < clip_rect.top or rect.top > clip_rect.bottom:
                continue

            yetiyor_mu = self.oyunVerileri["notalar"] >= u["fiyat"]

            if u["alinan"]:
                renk = (203, 0, 53)  # Kırmızı
                cerceve = (255, 202, 43) # Altın
            elif yetiyor_mu:
                renk = (203, 0, 53)  
                cerceve = (255, 202, 43) 
            else:
                renk = (203, 0, 53)
                cerceve = (255, 202, 43)

            # Hover efekti
            scale = 1.05 if rect.collidepoint(mouse_pos) else 1.0
            scaled_rect = pygame.Rect(
                rect.x - (rect.width * (scale - 1)) / 2,
                rect.y - (rect.height * (scale - 1)) / 2,
                rect.width * scale,
                rect.height * scale
            )

            pygame.draw.rect(self.pencere, renk, scaled_rect, border_radius=10)
            pygame.draw.rect(self.pencere, cerceve, scaled_rect, 2, border_radius=10)

            # Görsel
            self.pencere.blit(self.gorseller[i], (scaled_rect.x + 15, scaled_rect.centery - 60))

            # Yazılar
            isimYazi = self.fontKucuk.render(u["isim"], True, (255, 255, 255))
            fiyatYazi = self.fontKucuk.render(f"{u['fiyat']} nota", True, (255, 255, 0))
            carpimYazi = self.fontKucuk.render(f"x{u['carpan']} üretim", True, (180, 255, 180))

            self.pencere.blit(isimYazi, (scaled_rect.x + 160, scaled_rect.y + 15))
            self.pencere.blit(fiyatYazi, (scaled_rect.x + 160, scaled_rect.y + 55))
            self.pencere.blit(carpimYazi, (scaled_rect.x + 160, scaled_rect.y + 90))

            #Alınan tikisii
            if u["alinan"] and self.tik:
                self.pencere.blit(self.tik, (scaled_rect.right - 50, scaled_rect.y + 10))
                alindi_yazi = self.fontKucuk.render("Alındı", True, (100, 255, 100))
                self.pencere.blit(alindi_yazi, (scaled_rect.right - 110, scaled_rect.y + 70))

            self.upgradeRectList.append((rect, u, yetiyor_mu))

        self.pencere.set_clip(None)

        # Scroll bar
        if self.scroll_max > 0:
            bar_alani = pygame.Rect(self.menuRect.right - 25, clip_rect.y, 8, clip_rect.height)
            pygame.draw.rect(self.pencere, (180, 140, 20), bar_alani, border_radius=4)
            oran = abs(self.scroll_offset) / self.scroll_max if self.scroll_max > 0 else 0
            yukseklik = max(40, clip_rect.height * (gorunen_alan / toplam_icerik_yuksekligi))
            top_y = clip_rect.y + (clip_rect.height - yukseklik) * oran
            pygame.draw.rect(self.pencere, (255, 202, 43),
                             (bar_alani.x, top_y, bar_alani.width, yukseklik),
                             border_radius=4)

     
        pygame.draw.rect(self.pencere, (203, 0, 53), self.kapat_buton, border_radius=6)
        pygame.draw.rect(self.pencere, (255, 202, 43), self.kapat_buton, 2, border_radius=6)
        x_yazi = self.fontKucuk.render("X", True, (255, 255, 255))
        self.pencere.blit(
            x_yazi,
            (self.kapat_buton.centerx - x_yazi.get_width() // 2,
             self.kapat_buton.centery - x_yazi.get_height() // 2)
        )

    # --------------------------------------------------------
    def upgradeTiklama(self, mousePos):
        for rect, upgrade, yetiyor_mu in self.upgradeRectList:
            if rect.collidepoint(mousePos) and yetiyor_mu and not upgrade["alinan"]:
                self.oyunVerileri["notalar"] -= upgrade["fiyat"]
                self.oyunVerileri["tiklamaGucu"] = max(self.oyunVerileri["tiklamaGucu"], upgrade["carpan"])
                
                upgrade["alinan"] = True
                if self.ses_satinal:
                    self.ses_satinal.play()
                print(f"{upgrade['isim']} satın alındı! Yeni güç: {self.oyunVerileri['tiklamaGucu']}")
