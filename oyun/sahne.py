import os
import sys
import pygame
import time
from oyun.kayanMetin import KayanMetin
from oyun.arayuz import Buton

class Sahne:
    def __init__(self, pencere, genislik, yukseklik, oyunVerileri, kayan_metinler):
        self.yaziBaslik = pygame.font.SysFont("Palatino Linotype", 48, bold=True)
        self.yaziButon = pygame.font.SysFont("Palatino Linotype", 32, bold=True)
        self.yaziKucuk = pygame.font.Font(None, 28)

        # Görsel yollar
        base_path = os.path.dirname(os.path.dirname(__file__))

        self.pencere = pencere
        self.genislik = genislik
        self.yukseklik = yukseklik
        self.oyunVerileri = oyunVerileri
        self.kayan_metinler = kayan_metinler  

        # Renkler
        self.arkaRenk = (15, 18, 45)
        self.upgradeRenk = (120, 120, 180)

        # Arkaplan Resmi
        self.arkaplanYolu = os.path.join(base_path, "varliklar", "capibaralar", "sahne.png")
        try:
            self.arkaplanResmi = pygame.image.load(self.arkaplanYolu).convert()
            self.arkaplanResmi = pygame.transform.scale(self.arkaplanResmi, (genislik, yukseklik))
            print("Sahne: Arkaplan yüklendi.")
        except Exception as e:
            print("Sahne: Arkaplan yüklenemedi, renk kullanılacak:", e)
            self.arkaplanResmi = None


        # Fontlar
        self.yaziFont = pygame.font.Font(None, 32)
        self.butonFont = pygame.font.Font(None, 36)
        # --- MANUEL YAPILANDIRMA (BURAYI DÜZENLEYİN) ---
        # Her karakterin (X, Y) konumu ve (Genislilik, Yukseklik) boyutu burada belirlenir.
        # Ekran Boyutu: 1280 x 720
        self.sahne_ayarlari = {
            "ana_piyano": {"pos": (559, 346), "size": (220, 238)}, # Siz (Merkez)
            "orkestra": [
                {"isim": "Flüt",   "pos": (768, 398),  "size": (197, 201)}, # Sağ Ön
                {"isim": "Org",    "pos": (985, 425), "size": (180, 163)}, # Sağ Köşe
                {"isim": "Bateri", "pos": (180, 409),  "size": (172, 169)}, # Sol Köşe
                {"isim": "Crash",  "pos": (390, 428),  "size": (172, 169)}, # Sol Ön
                {"isim": "Koro",   "pos": (422, 275),  "size": (431, 262)}, # Arka Orta
            ]
        }
        # -------------------------------------------------

        self.baslikFont = pygame.font.Font(None, 48)

        self.capiNormalYolu = os.path.join(base_path, "varliklar", "capibaralar", "piyano.png")
        self.capiTiklamaYolu = os.path.join(base_path, "varliklar", "capibaralar", "piyano1.png")
        # Eski müzik yolu (artık kullanılmıyor ama referans kalsın derseniz)
        self.muzik_yolu = os.path.join(base_path, "varliklar", "ses", "piyano.mp3")

        # Görseller
        self.capiResimNormal = pygame.image.load(self.capiNormalYolu).convert_alpha()
        self.capiResimTiklama = pygame.image.load(self.capiTiklamaYolu).convert_alpha()

        # Ana Capybara Ayarları
        ana_config = self.sahne_ayarlari["ana_piyano"]
        self.capiResimNormal = pygame.transform.scale(self.capiResimNormal, ana_config["size"])
        self.capiResimTiklama = pygame.transform.scale(self.capiResimTiklama, ana_config["size"])

        self.capiResim = self.capiResimNormal
        # Manuel ayar kolaylığı için 'topleft' kullanıyoruz.
        self.capiRect = self.capiResim.get_rect(topleft=ana_config["pos"]) 

        # Orchestra visuals & Audio
        self.upgradeAssets = {}
        for index, u in enumerate(self.oyunVerileri["upgrades"]):
            asset_data = {"img": None, "active_img": None, "sound": None}
            
            # İlgili konfigürasyonu bul (Sırayla eşleşiyor varsayıyoruz)
            # Not: main.py listesindeki sıraya göre eşleşir.
            # 0: Flüt, 1: Org, 2: Bateri...
            config = {"size": (150, 150)} # Varsayılan
            if index < len(self.sahne_ayarlari["orkestra"]):
                config = self.sahne_ayarlari["orkestra"][index]

            # Görsel
            try:
                img = pygame.image.load(u["resim"]).convert_alpha()
                img = pygame.transform.scale(img, config["size"])
                asset_data["img"] = img
            except Exception as e:
                print(f"Sahne: Görsel yüklenemedi {u['resim']}: {e}")
            
            # Aktif Resim (Söyler hal)
            if "aktif_resim" in u:
                try:
                    img_active = pygame.image.load(u["aktif_resim"]).convert_alpha()
                    img_active = pygame.transform.scale(img_active, config["size"])
                    asset_data["active_img"] = img_active
                except Exception as e:
                    print(f"Sahne: Aktif görsel yüklenemedi {u['aktif_resim']}: {e}")

            
            # Ses
            if "ses" in u:
                ses_yolu = os.path.join(base_path, u["ses"])
                if os.path.exists(ses_yolu):
                    try:
                        snd = pygame.mixer.Sound(ses_yolu)
                        snd.set_volume(0.5)
                        asset_data["sound"] = snd
                    except Exception as e:
                        print(f"Sahne: Ses yüklenemedi {ses_yolu}: {e}")
                else:
                    # Dosya yoksa sessizce geç
                    pass
            
            self.upgradeAssets[u["isim"]] = asset_data

        # Tıklanabilir alanlar listesi (Orkestra üyeleri için)
        self.orkestraRects = []

        # Sahne Pozisyonları (Konfigürasyondan al)
        self.sahne_pozisyonlari = [item["pos"] for item in self.sahne_ayarlari["orkestra"]]

        # Upgrade butonu
        self.butonResmi = None
        butonYolu = os.path.join(base_path, "varliklar", "capibaralar", "buton.png")
        if os.path.exists(butonYolu):
            try:
                self.butonResmi = pygame.image.load(butonYolu).convert_alpha()
            except Exception as e:
                print("Sahne: Buton görseli yüklenemedi:", e)

        # self.upgradeRect referansını korumak için butButton.rect kullanacağız ama
        # eski kodda self.upgradeRect direkt kullanılıyordu.
        # Kolaylık olsun diye upgrade butonunu oluşturup rect'i ona eşitleyelim.
        self.butUpgrade = Buton("Upgrade", genislik - 170, 20, 150, 50, resim=self.butonResmi)
        self.upgradeRect = self.butUpgrade.rect

        # Duraklatma ve Ses
        self.duraklatildi = False
        self.sesSeviyesi = 0.5
        
        # Müzik init
        pygame.mixer.init()
        # mixer.music yerine mixer.Channel kullanabiliriz veya doğrudan Sound.play()
        
        self.muzikCalıyor = False
        self.sonTiklamaZamani = 0
        self.animasyonBaslamaZamani = 0
        self.animasyonSuresi = 0.3

        # Menü Tanımları
        self.pauseResmi = None
        pauseYolu = os.path.join(base_path, "varliklar", "kullaniciArayuzu", "pause.png")
        if os.path.exists(pauseYolu):
            try:
                self.pauseResmi = pygame.image.load(pauseYolu).convert_alpha()
                # Orijinal boyut kalsın
            except Exception as e:
                print("Sahne: Pause resmi yüklenemedi:", e)

        # Orijinal menü boyutları (Buton konumları bozulmasın diye)
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
        self.butKaydet = pygame.Rect(self.menuRect.centerx - 150, self.menuRect.y + 260, 300, 50) # Kaydet butonu geri geldi
        self.butAnaMenu = pygame.Rect(self.menuRect.centerx - 150, self.menuRect.y + 330, 300, 50)
        self.butCikis = pygame.Rect(self.menuRect.centerx - 150, self.menuRect.y + 400, 300, 50)




    def muzik_baslat(self):
        # Tüm alınan upgradelerin seslerini çal
        # Senkronizasyon için hepsini durdurup tekrar baslat
        self.muzik_durdur()
        
        for u in self.oyunVerileri["upgrades"]:
            if u["alinan"]:
                asset = self.upgradeAssets.get(u["isim"])
                if asset and asset["sound"]:
                    # Looplu çal
                    asset["sound"].play(loops=-1)
        
        self.muzikCalıyor = True

    def muzik_durdur(self):
        # Tüm sesleri durdur
        pygame.mixer.stop() 
        self.muzikCalıyor = False

    def guncelle(self, events):
        simdi = time.time()

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.duraklatildi = not self.duraklatildi
                    if self.duraklatildi:
                        self.muzik_durdur()  
                    else:
                        pass
                elif event.key == pygame.K_m:
                    self.oyunVerileri["notalar"] += 10000
                    self.kayan_metinler.append(KayanMetin("+10000 (Hile)", (self.genislik // 2, self.yukseklik // 2)))

            if not self.duraklatildi:
                # Tıklama
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.upgradeRect.collidepoint(event.pos):
                        self.muzik_durdur() # Upgrade ekranına geçerken durdur
                        return "upgrade"

                    # Ana Capybara Tıklama
                    tiklanan_orkestra = False
                    
                    # Orkestra üyelerine tıklama kontrolü
                    for rect, upgrade_isim in self.orkestraRects:
                        if rect.collidepoint(event.pos):
                            tiklanan_orkestra = True
                            break
                    
                    if self.capiRect.collidepoint(event.pos) or tiklanan_orkestra:
                        kazanc = self.oyunVerileri["tiklamaGucu"]
                        self.oyunVerileri["notalar"] += kazanc
                        self.sonTiklamaZamani = simdi
                        self.animasyonBaslamaZamani = simdi
                        
                        # Ana capybara animasyonu
                        if self.capiRect.collidepoint(event.pos):
                            self.capiResim = self.capiResimTiklama
                        
                        self.kayan_metinler.append(KayanMetin(f"+{kazanc}", event.pos))

                        if not self.muzikCalıyor:
                            self.muzik_baslat()
                        
            else:
                # Menü mantığı
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.sliderTopRect.collidepoint(event.pos):
                        self.surukleniyor = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.surukleniyor = False
                elif event.type == pygame.MOUSEMOTION and getattr(self, "surukleniyor", False):
                    self.sesSeviyesi = max(0, min(1, (event.pos[0] - self.sliderRect.x) / self.sliderRect.width))
                    self.sliderTopRect.x = self.sliderRect.x + int(self.sesSeviyesi * self.sliderRect.width) - 10
                    # Tüm seslerin volume'unu güncelle
                    for asset in self.upgradeAssets.values():
                        if asset["sound"]:
                            asset["sound"].set_volume(self.sesSeviyesi) # type: ignore

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.butDevam.collidepoint(event.pos):
                        self.duraklatildi = False
                    elif self.butAnaMenu.collidepoint(event.pos):
                        self.muzik_durdur()
                        return "anaMenu"
                    elif self.butCikis.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

        # Müzik zamanlayıcı (Oto durdurma)
        if self.muzikCalıyor and (simdi - self.sonTiklamaZamani > 1.5):
            self.muzik_durdur()

        # Capybara animasyonu reset
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
        if self.arkaplanResmi:
            self.pencere.blit(self.arkaplanResmi, (0, 0))
        else:
            self.pencere.fill(self.arkaRenk)

        
        # Notalar
        notYazi = self.yaziFont.render(f"Notalar: {self.oyunVerileri['notalar']}", True, (255, 255, 255))
        self.pencere.blit(notYazi, (20, 20))
        
        # --- Orkestra Çizimi (Z-Order Düzenlemesi) ---
        self.orkestraRects = [] 

        # 1. KATMAN: Arka Plandakiler (Örn: Koro)
        # Ana karakterin arkasında kalması gerekenler
        for i, u in enumerate(self.oyunVerileri["upgrades"]):
            if u["alinan"] and "Koro" in u["isim"]:
                self._upgrade_ciz(i, u)
        
        # 2. KATMAN: Ana Karakter (Piyano)
        self.pencere.blit(self.capiResim, self.capiRect)
        # Hata Ayıklama (İsteğe bağlı)
        # pygame.draw.rect(self.pencere, (255, 0, 0), self.capiRect, 1)
        
        # 3. KATMAN: Ön Plandakiler (Diğerleri)
        for i, u in enumerate(self.oyunVerileri["upgrades"]):
            if u["alinan"] and "Koro" not in u["isim"]:
                self._upgrade_ciz(i, u)
        
        # Upgrade butonu
        self.butUpgrade.cizVeKontrol(self.pencere)

        # Kayan metinler - En üstte
        for metin in self.kayan_metinler:
            metin.ciz(self.pencere)

    def _upgrade_ciz(self, i, u):
        # Yardımcı fonksiyon: Tek bir upgrade'i çizer
        pos_index = i % len(self.sahne_pozisyonlari)
        target_pos = self.sahne_pozisyonlari[pos_index]
        
        asset = self.upgradeAssets.get(u["isim"])
        if asset and asset["img"]:
            draw_img = asset["img"]
            # Animasyon hızı ana karakterle eşitlensin (Sadece animasyon süresi kadar)
            if self.muzikCalıyor and asset["active_img"]:
                 if time.time() - self.animasyonBaslamaZamani < self.animasyonSuresi:
                    draw_img = asset["active_img"]
            
            # Sol üst köşeye göre çiz
            r = draw_img.get_rect(topleft=target_pos)
            
            # Hover efekti KALDIRILDI (İstek üzerine)
            # mouse_pos = pygame.mouse.get_pos()
            # if r.collidepoint(mouse_pos):
            #    r.y -= 5
            
            self.pencere.blit(draw_img, r)
            self.orkestraRects.append((r, u["isim"]))



    def cizDuraklatmaMenusu(self):
        if self.pauseResmi:
            # Resmi merkeze hizala
            img_rect = self.pauseResmi.get_rect(center=self.menuRect.center)
            self.pencere.blit(self.pauseResmi, img_rect)
        else:
            pygame.draw.rect(self.pencere, (25, 25, 40), self.menuRect, border_radius=20)
            pygame.draw.rect(self.pencere, (100, 100, 180), self.menuRect, width=3, border_radius=20)

        baslik = self.yaziBaslik.render("Oyun Duraklatıldı", True, (255, 255, 255))
        self.pencere.blit(baslik, (self.menuRect.centerx - baslik.get_width() // 2, self.menuRect.y + 30))

        # Slider
        topX = self.sliderRect.x + int(self.sesSeviyesi * self.sliderRect.width)
        topY = self.sliderRect.centery
        # Slider Arkaplanı (Koyu Sarı/Altın)
        pygame.draw.rect(self.pencere, (180, 140, 20), self.sliderRect, border_radius=10)
        # Slider Topu (Parlak Sarı #ffca2b)
        pygame.draw.circle(self.pencere, (255, 202, 43), (topX, topY), 9)

        sesYazi = self.yaziKucuk.render(f"Ses: %{int(self.sesSeviyesi * 100)}", True, (255, 255, 255))
        self.pencere.blit(sesYazi, (self.sliderRect.centerx - sesYazi.get_width() // 2, self.sliderRect.y - 35))

        for yazi, butonRect in [
            ("Devam Et", self.butDevam),
            ("Kaydet", self.butKaydet),
            ("Ana Menüye Dön", self.butAnaMenu),
            ("Çıkış", self.butCikis),
        ]:
            # İstenen renkler: Arkaplan #cb0035 (203, 0, 53), Çerçeve #ffca2b (255, 202, 43)
            pygame.draw.rect(self.pencere, (203, 0, 53), butonRect, border_radius=10)
            pygame.draw.rect(self.pencere, (255, 202, 43), butonRect, 2, border_radius=10)
            yaziYuzeyi = self.yaziButon.render(yazi, True, (255, 255, 255))
            self.pencere.blit(
                yaziYuzeyi,
                (butonRect.centerx - yaziYuzeyi.get_width() // 2, butonRect.centery - yaziYuzeyi.get_height() // 2)
            )
