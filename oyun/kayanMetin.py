import pygame
import time

class KayanMetin:
    def __init__(self, yazi, konum):
        self.yazi = yazi
        self.x, self.y = konum
        self.font = pygame.font.Font(None, 40)
        self.olusturma_zamani = time.time()
        self.sure = 1.5  # saniye
        self.opaklik = 255
        self.yukselme_hizi = 0.8
        self.bitti = False

    def guncelle(self):
        gecen = time.time() - self.olusturma_zamani
        if gecen > self.sure:
            self.bitti = True
        else:
            self.y -= self.yukselme_hizi
            self.opaklik = max(0, 255 * (1 - gecen / self.sure))

    def ciz(self, ekran):
        if self.bitti:
            return

        metin = self.font.render(self.yazi, True, (255, 255, 255))
        metin.set_alpha(int(self.opaklik))
        ekran.blit(metin, (self.x, self.y))