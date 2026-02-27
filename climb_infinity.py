import pygame
import sys
import random

pygame.init()

ekran_genislik = 800
ekran_yukseklik = 700
ekran = pygame.display.set_mode((ekran_genislik, ekran_yukseklik))
pygame.display.set_caption("Sonsuz Tırmanış")

siyah_renk = (0, 0, 0)
beyaz_renk = (255, 255, 255)
mavi_renk = (50, 150, 255)
kirmizi_renk = (200, 0, 0)

font = pygame.font.SysFont("Arial", 30)
buton_font = pygame.font.SysFont("Arial", 25)

def oyunu_sifirla():
    global oyuncu_x, oyuncu_y, dikey_hiz, ziplama, platformlar, skor, oldun
    oyuncu_x = 400
    oyuncu_y = 500
    dikey_hiz = 0
    ziplama = False
    skor = 0
    oldun = False
    platformlar = []
    platformlar.append(pygame.Rect(350, 550, 100, 10))
    for i in range(15):
        p_x = random.randint(0, ekran_genislik - 50)
        p_y = 400 - (i * 130) 
        platformlar.append(pygame.Rect(p_x, p_y, 50, 10))

oyunu_sifirla()
saat_hizi = pygame.time.Clock()

while True:
    fare_pos = pygame.mouse.get_pos()
    #Yeniden başla butonu konumu
    buton_rect = pygame.Rect(300, 350, 200, 50)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        #Ölünce butona tıklanma kontrolü
        if event.type == pygame.MOUSEBUTTONDOWN and oldun:
            if buton_rect.collidepoint(fare_pos):
                oyunu_sifirla()
    
    tuslar = pygame.key.get_pressed()
    if not oldun:
        if tuslar[pygame.K_LEFT]:
            oyuncu_x -= 6
        if tuslar[pygame.K_RIGHT]:
            oyuncu_x += 6
        
        if tuslar[pygame.K_UP] and not ziplama:
            dikey_hiz = -16
            ziplama = True

    dikey_hiz += 0.5
    oyuncu_y += dikey_hiz

    if oyuncu_y < 350 and not oldun:
        fark = 350 - oyuncu_y
        oyuncu_y = 350
        for p in platformlar:
            p.y += fark
        skor += int(fark / 10) 

    if not oldun:
        for p in platformlar[:]:
            if p.y > ekran_yukseklik:
                platformlar.remove(p)
                yeni_x = random.randint(0, ekran_genislik - 50)
                yeni_y = random.randint(-140, -70) 
                platformlar.append(pygame.Rect(yeni_x, yeni_y, 50, 10))

    if oyuncu_x < -30: oyuncu_x = ekran_genislik
    elif oyuncu_x > ekran_genislik: oyuncu_x = -30

    if oyuncu_y > ekran_yukseklik:
        oldun = True

    ekran.fill(siyah_renk)
    
    oyuncu_rect = pygame.Rect(oyuncu_x, oyuncu_y, 30, 30)

    for p in platformlar:
        pygame.draw.rect(ekran, beyaz_renk, p)
        if oyuncu_rect.colliderect(p) and dikey_hiz > 0 and not oldun:
            if oyuncu_y + 30 < p.bottom + 10:
                oyuncu_y = p.top - 30
                dikey_hiz = 0
                ziplama = False

    if not oldun:
        pygame.draw.rect(ekran, beyaz_renk, oyuncu_rect)
    
    # Skor Çizimi
    skor_yuzeyi = font.render(f"Skor: {skor}", True, beyaz_renk)
    ekran.blit(skor_yuzeyi, (20, 20))

    # Ölünce Buton Çizimi
    if oldun:
        pygame.draw.rect(ekran, beyaz_renk, buton_rect)
        yazi = buton_font.render("Yeniden Başla", True, siyah_renk)
        ekran.blit(yazi, (buton_rect.x + 35, buton_rect.y + 10))

    pygame.display.flip()
    saat_hizi.tick(60)