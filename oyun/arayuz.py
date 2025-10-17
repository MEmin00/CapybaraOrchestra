import pygame

class Buton:
    def __init__(self, yazi, x, y, genislik, yukseklik):
        self.yazi = yazi
        self.rect = pygame.Rect(x, y, genislik, yukseklik)
        self.renkNormal = (100, 100, 200)
        self.renkUzerinde = (150, 150, 250)
        self.yaziTipi = pygame.font.SysFont("arial", 32)

    def cizVeKontrol(self, pencere):
        farePos = pygame.mouse.get_pos()
        # Buton rengi seçimi - sadece çizim yapar, tıklama kontrolü main loop'ta yapılır
        renk = self.renkUzerinde if self.rect.collidepoint(farePos) else self.renkNormal
        pygame.draw.rect(pencere, renk, self.rect, border_radius=12)

        # Yazı
        yaziRender = self.yaziTipi.render(self.yazi, True, (255, 255, 255))
        pencere.blit(
            yaziRender,
            (self.rect.centerx - yaziRender.get_width() // 2, self.rect.centery - yaziRender.get_height() // 2)
        )
        return None
