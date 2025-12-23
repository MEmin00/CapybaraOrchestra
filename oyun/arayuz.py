import pygame

class Buton:
    def __init__(self, yazi, x, y, genislik, yukseklik, resim=None):
        self.yazi = yazi
        self.rect = pygame.Rect(x, y, genislik, yukseklik)
        self.renkNormal = (100, 100, 200)
        self.renkUzerinde = (150, 150, 250)
        self.yaziTipi = pygame.font.SysFont("Palatino Linotype", 32, bold=True)
        self.resim = None
        if resim:
            self.resim = pygame.transform.scale(resim, (genislik, yukseklik))

    def cizVeKontrol(self, pencere):
        farePos = pygame.mouse.get_pos()
        uzerinde = self.rect.collidepoint(farePos)
        
        if self.resim:
            pencere.blit(self.resim, self.rect)
            if uzerinde:
                overlay = pygame.Surface(self.rect.size, pygame.SRCALPHA)
                overlay.fill((255, 255, 255, 50))
                pencere.blit(overlay, self.rect)
        else:
            renk = self.renkUzerinde if uzerinde else self.renkNormal
            pygame.draw.rect(pencere, renk, self.rect, border_radius=12)

        
        renkYazi = (217, 12, 44)
        yaziRender = self.yaziTipi.render(self.yazi, True, renkYazi)
        pencere.blit(
            yaziRender,
            (self.rect.centerx - yaziRender.get_width() // 2, self.rect.centery - yaziRender.get_height() // 2)
        )
        return None
