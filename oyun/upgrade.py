import pygame

class UpgradeEkrani:
    def __init__(self, pencere, GENISLIK, YUKSEKLIK, oyunVerileri):
        self.pencere = pencere
        self.GENISLIK = GENISLIK
        self.YUKSEKLIK = YUKSEKLIK
        self.oyunVerileri = oyunVerileri

        self.alpha = 150

        # Fontlar
        self.fontBaslik = pygame.font.Font(None, 64)
        self.fontKucuk = pygame.font.Font(None, 36)

        # Menü paneli
        self.menuGenislik = int(GENISLIK * 0.66)
        self.menuYukseklik = int(YUKSEKLIK * 0.66)
        self.menuRect = pygame.Rect(
            (GENISLIK - self.menuGenislik) // 2,
            (YUKSEKLIK - self.menuYukseklik) // 2,
            self.menuGenislik,
            self.menuYukseklik
        )

        # Upgrade verileri
        self.upgrades = [
            {"isim": "Gitarcı Capibara", "fiyat": 1, "resim": "varliklar/capibaralar/gitar.png", "carpan": 2, "alinan": False},
            {"isim": "Davulcu Capibara", "fiyat": 300, "resim": "varliklar/capibaralar/davul.png", "carpan": 3, "alinan": False},
            {"isim": "Flütçü Capibara", "fiyat": 500, "resim": "varliklar/capibaralar/flute.png", "carpan": 5, "alinan": False},
            {"isim": "Kemanlı Capibara", "fiyat": 800, "resim": "varliklar/capibaralar/kemancı.png", "carpan": 8, "alinan": False},
            {"isim": "Trompetçi Capibara", "fiyat": 1200, "resim": "varliklar/capibaralar/trompet.png", "carpan": 10, "alinan": False},
            {"isim": "Saksafoncu Capibara", "fiyat": 1500, "resim": "varliklar/capibaralar/saksofon.png", "carpan": 15, "alinan": False},
            {"isim": "DJ Capibara", "fiyat": 2000, "resim": "varliklar/capibaralar/dj.png", "carpan": 25, "alinan": False},
        ]

        # Görselleri yükle
        self.gorseller = []
        for u in self.upgrades:
            try:
                img = pygame.image.load(u["resim"]).convert_alpha()
                img = pygame.transform.scale(img, (120, 120))
                self.gorseller.append(img)
            except Exception as e:
                print(f"Görsel yüklenemedi: {u['resim']}, hata: {e}")
                self.gorseller.append(pygame.Surface((120, 120)))

        # Ses efekti
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
        self.scroll_max = 0  # Dinamik hesaplanacak

    # --------------------------------------------------------
    # GÜNCELLE
    # --------------------------------------------------------
    def guncelle(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                return "sahne"

            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 4:  # Yukarı
                    self.scroll_offset = min(self.scroll_offset + self.scroll_hiz, 0)
                elif e.button == 5:  # Aşağı
                    self.scroll_offset = max(self.scroll_offset - self.scroll_hiz, -self.scroll_max)
                elif e.button == 1:
                    if self.kapat_buton.collidepoint(e.pos):
                        return "sahne"
                    self.upgradeTiklama(e.pos)

        self.ciz()
        return None

    # --------------------------------------------------------
    # ÇİZİM
    # --------------------------------------------------------
    def ciz(self):
        # Blur arka plan
        ekran_kopya = pygame.Surface((self.GENISLIK, self.YUKSEKLIK))
        ekran_kopya.blit(self.pencere, (0, 0))
        blur = pygame.transform.smoothscale(ekran_kopya, (self.GENISLIK // 8, self.YUKSEKLIK // 8))
        blur = pygame.transform.smoothscale(blur, (self.GENISLIK, self.YUKSEKLIK))
        blur.set_alpha(self.alpha)
        self.pencere.blit(blur, (0, 0))

        # Menü paneli
        pygame.draw.rect(self.pencere, (30, 30, 50), self.menuRect, border_radius=20)
        pygame.draw.rect(self.pencere, (120, 120, 200), self.menuRect, 3, border_radius=20)

        # Başlık
        baslik = self.fontBaslik.render("Yükseltmeler", True, (255, 255, 255))
        self.pencere.blit(baslik, (self.menuRect.centerx - baslik.get_width() // 2, self.menuRect.y + 30))

        # Notalar göstergesi
        notaYazi = self.fontKucuk.render(f"Toplam Notalar: {self.oyunVerileri['notalar']}", True, (255, 255, 0))
        self.pencere.blit(notaYazi, (self.menuRect.centerx - notaYazi.get_width() // 2, self.menuRect.y + 100))

        # İçerik alanı
        clip_rect = pygame.Rect(
            self.menuRect.x,
            self.menuRect.y + 150,
            self.menuRect.width - 20,
            self.menuRect.height - 170
        )
        self.pencere.set_clip(clip_rect)

        # Elemanları çiz
        self.upgradeRectList = []
        start_y = self.menuRect.y + 160 + self.scroll_offset

        toplam_icerik_yuksekligi = len(self.upgrades) * 160
        gorunen_alan = clip_rect.height
        self.scroll_max = max(0, toplam_icerik_yuksekligi - gorunen_alan)

        for i, u in enumerate(self.upgrades):
            if u["alinan"]:
                continue  # Satın alınanlar gizlenir

            rect = pygame.Rect(self.menuRect.x + 80, start_y, self.menuRect.width - 160, 120)
            start_y += 160

            if rect.bottom < clip_rect.top or rect.top > clip_rect.bottom:
                continue

            yetiyor_mu = self.oyunVerileri["notalar"] >= u["fiyat"]
            renk = (80, 120, 180) if yetiyor_mu else (50, 50, 70)

            pygame.draw.rect(self.pencere, renk, rect, border_radius=10)
            pygame.draw.rect(self.pencere, (150, 150, 220), rect, 2, border_radius=10)

            self.pencere.blit(self.gorseller[i], (rect.x + 15, rect.centery - 60))

            isimYazi = self.fontKucuk.render(u["isim"], True, (255, 255, 255))
            fiyatYazi = self.fontKucuk.render(f"{u['fiyat']} nota", True, (255, 255, 0))
            carpimYazi = self.fontKucuk.render(f"x{u['carpan']} üretim", True, (180, 255, 180))

            self.pencere.blit(isimYazi, (rect.x + 160, rect.y + 15))
            self.pencere.blit(fiyatYazi, (rect.x + 160, rect.y + 55))
            self.pencere.blit(carpimYazi, (rect.x + 160, rect.y + 90))

            self.upgradeRectList.append((rect, u, yetiyor_mu))

        self.pencere.set_clip(None)

        # Scroll bar
        if self.scroll_max > 0:
            bar_alani = pygame.Rect(self.menuRect.right - 25, clip_rect.y, 8, clip_rect.height)
            pygame.draw.rect(self.pencere, (70, 70, 100), bar_alani, border_radius=4)

            oran = abs(self.scroll_offset) / self.scroll_max if self.scroll_max > 0 else 0
            yukseklik = max(40, clip_rect.height * (gorunen_alan / toplam_icerik_yuksekligi))
            top_y = clip_rect.y + (clip_rect.height - yukseklik) * oran

            pygame.draw.rect(self.pencere, (160, 160, 240),
                             (bar_alani.x, top_y, bar_alani.width, yukseklik),
                             border_radius=4)

        # Kapat butonu
        pygame.draw.rect(self.pencere, (180, 80, 80), self.kapat_buton, border_radius=6)
        x_yazi = self.fontKucuk.render("X", True, (255, 255, 255))
        self.pencere.blit(
            x_yazi,
            (self.kapat_buton.centerx - x_yazi.get_width() // 2,
             self.kapat_buton.centery - x_yazi.get_height() // 2)
        )

    # --------------------------------------------------------
    # SATIN ALMA
    # --------------------------------------------------------
    def upgradeTiklama(self, mousePos):
        for rect, upgrade, yetiyor_mu in self.upgradeRectList:
            if rect.collidepoint(mousePos) and yetiyor_mu and not upgrade["alinan"]:
                self.oyunVerileri["notalar"] -= upgrade["fiyat"]
                self.oyunVerileri["tiklamaGucu"] *= upgrade["carpan"]
                upgrade["alinan"] = True
                if self.ses_satinal:
                    self.ses_satinal.play()
                print(f"{upgrade['isim']} satın alındı! Yeni güç: {self.oyunVerileri['tiklamaGucu']}")