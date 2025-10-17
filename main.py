# main.py
# Capybara Orkestrası - Animasyonlu final sürüm
# - Flüt sabit
# - Gitar: sağ-sol sallanma (sinüs)
# - Davul: iki-frame vuruş animasyonu (1s per frame)
# - Save / Load / Reset
# - ESC pause menu with only slider
# - Safe image loading
# Gereksinim: pygame

import pygame
import sys
import os
import json
import math
from typing import List, Dict

# -------- INIT ----------
pygame.init()
try:
    pygame.mixer.init()
except Exception:
    pass

# -------- SCREEN & CLOCK ----------
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Capybara Orkestrası - Animasyonlu")
clock = pygame.time.Clock()

# -------- COLORS & FONTS ----------
WHITE = (255, 255, 255)
RED   = (200, 50, 50)
PANEL_BG = (40, 40, 40)
GRAY = (120, 120, 120)
BLACK = (0,0,0)
GREEN = (80, 200, 120)

FONT = pygame.font.Font(None, 36)
SMALL = pygame.font.Font(None, 24)
MINI = pygame.font.Font(None, 20)

# -------- SAVE / LOAD ----------
SAVE_FILE = "save.json"
def default_state():
    return {
        "notes": 0,
        "click_power": 1,
        "idle_per_sec": 0,
        "level": 1,
        "purchased_names": [],
        "click_multiplier": 1.0
    }

def save_game(state: Dict):
    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
        print("[SAVE] Kaydedildi.")
    except Exception as e:
        print("[SAVE ERROR]", e)

def load_game():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            base = default_state()
            for k,v in base.items():
                if k not in data:
                    data[k] = v
            print("[LOAD] Yüklendi.")
            return data
        except Exception as e:
            print("[LOAD ERROR]", e)
            return default_state()
    else:
        print("[LOAD] Kayıt yok, varsayılan.")
        return default_state()

def reset_save():
    try:
        if os.path.exists(SAVE_FILE):
            os.remove(SAVE_FILE)
            print("[RESET] Save silindi.")
        else:
            print("[RESET] Save yok.")
    except Exception as e:
        print("[RESET ERROR]", e)

# -------- SAFE IMAGE LOADER ----------
def safe_load(path: str, size=None, alpha=True, fallback_color=(120,120,120)):
    try:
        surf = pygame.image.load(path)
        surf = surf.convert_alpha() if alpha else surf.convert()
        if size:
            surf = pygame.transform.scale(surf, size)
        # print(f"[OK] Loaded: {path}")
        return surf
    except Exception as e:
        print(f"[WARN] Could not load '{path}': {e}")
        surf = pygame.Surface(size if size else (100,100), pygame.SRCALPHA)
        surf.fill(fallback_color)
        return surf

# -------- LOAD GLOBAL STATE ----------
state = load_game()
notes = state["notes"]
click_power = state["click_power"]
idle_per_sec = state["idle_per_sec"]
level = state["level"]
purchased_names: List[str] = state["purchased_names"]
click_multiplier = state.get("click_multiplier", 1.0)

# -------- ASSETS ----------
# background
background = safe_load("images/scane.png", (WIDTH, HEIGHT), alpha=False, fallback_color=(20,20,40))

# flute (sabit)
flute_img = safe_load("images/characters/flute.png", (200,150), alpha=True, fallback_color=(150,150,200))
flute_pressed_img = safe_load("images/characters/flute1.png", (200,150), alpha=True, fallback_color=(180,150,200))
flute_rect = flute_img.get_rect(center=(WIDTH//2 - 100, int(HEIGHT/1.4)))

# guitar (single sprite)
guitar_img = safe_load("images/characters/gitar.png", (160,140), alpha=True, fallback_color=(140,120,80))
# drum frames
davul_frame_1 = safe_load("images/characters/davul.png", (160,140), alpha=True, fallback_color=(120,80,140))
davul_frame_2 = safe_load("images/characters/davul_2.png", (160,140), alpha=True, fallback_color=(120,80,140))

# music (safe)
try:
    pygame.mixer.music.load("music/flute.mp3")
    try:
        if pygame.mixer.get_init():
            pygame.mixer.music.set_volume(pygame.mixer.music.get_volume())
    except Exception:
        pass
except Exception:
    print("[WARN] music/flute.mp3 yüklenemedi.")

# -------- UPGRADES DATA ----------
upgrades = [
    {"name":"Flüt Capy", "price":50,  "mult":1.0, "idle_bonus":0, "id":"flute"},
    {"name":"Gitar Capy", "price":150, "mult":2.0, "idle_bonus":0, "id":"guitar"},
    {"name":"Davul Capy", "price":300, "mult":3.0, "idle_bonus":3, "id":"drum"},  # davul +3 idle
]

# purchased objects
purchased_objs: List[Dict] = []
def load_purchased_objs():
    purchased_objs.clear()
    for name in purchased_names:
        for u in upgrades:
            if u["name"] == name:
                new = dict(u)
                if u["id"] == "guitar":
                    new["surf"] = guitar_img
                elif u["id"] == "drum":
                    # for draw we will use davul frames instead (we store id)
                    new["surf"] = None
                else:
                    new["surf"] = None
                purchased_objs.append(new)
                break

load_purchased_objs()

# -------- UI RECTS ----------
start_btn = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 - 50, 200, 60)
exit_btn  = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 30, 200, 60)
master_slider_rect = pygame.Rect(WIDTH//2 - 200, HEIGHT//2 + 120, 400, 30)
upgrade_btn = pygame.Rect(WIDTH - 140, 10, 130, 40)
level_box  = pygame.Rect(WIDTH - 140, 60, 130, 30)
panel_x = WIDTH - 320; panel_y = 60; panel_w = 300; panel_item_h = 60
buy_btn = pygame.Rect(WIDTH - 140, 60 + 180 + 50, 120, 40)
resume_btn = pygame.Rect(WIDTH//2 - 120, HEIGHT//2 - 90, 240, 50)
reset_btn  = pygame.Rect(WIDTH//2 - 120, HEIGHT//2 - 20, 240, 50)
mainmenu_btn = pygame.Rect(WIDTH//2 - 120, HEIGHT//2 + 50, 240, 50)
pause_slider_rect = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 + 120, 300, 24)

# slider class (visual)
class Slider:
    def __init__(self, rect, start=0.8, fill=(200,50,50), bg=(60,60,60)):
        self.rect = pygame.Rect(rect)
        self.value = start
        self.fill = fill
        self.bg = bg
        self.drag = False
    def handle(self, ev):
        if ev.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(ev.pos):
            self.drag = True
            self._set(ev.pos[0])
        elif ev.type == pygame.MOUSEBUTTONUP:
            self.drag = False
        elif ev.type == pygame.MOUSEMOTION and self.drag:
            self._set(ev.pos[0])
    def _set(self, x):
        rel = (x - self.rect.x) / self.rect.w
        self.value = max(0.0, min(1.0, rel))
    def draw(self, surf):
        pygame.draw.rect(surf, self.bg, self.rect, border_radius=8)
        fill_w = int(self.rect.w * self.value)
        if fill_w > 0:
            alt = pygame.Rect(self.rect.x, self.rect.y, fill_w, self.rect.h)
            ust = pygame.Rect(self.rect.x, self.rect.y, fill_w, int(self.rect.h*0.6))
            pygame.draw.rect(surf, self.fill, alt, border_radius=8)
            pygame.draw.rect(surf, (min(self.fill[0]+30,255),min(self.fill[1]+30,255),min(self.fill[2]+30,255)), ust, border_radius=8)
        top_x = self.rect.x + fill_w
        top_y = self.rect.centery
        pygame.draw.circle(surf, (230,230,230), (top_x, top_y), int(self.rect.h*0.9))
        pygame.draw.circle(surf, BLACK, (top_x, top_y), int(self.rect.h*0.9), 2)

try:
    mixer_ok = pygame.mixer.get_init() is not None
except Exception:
    mixer_ok = False

master_slider = Slider(master_slider_rect, start=pygame.mixer.music.get_volume() if mixer_ok else 0.8)
pause_slider  = Slider(pause_slider_rect, start=master_slider.value)

# -------- POPUPS ----------
popups: List[Dict] = []
def add_popup_local(msg: str, dur=1600):
    popups.append({"msg":msg, "start":pygame.time.get_ticks(), "dur":dur})
def draw_popups(surface):
    if not popups:
        return
    now = pygame.time.get_ticks()
    popups[:] = [p for p in popups if now - p["start"] <= p["dur"] + 600]
    if not popups:
        return
    p = popups[-1]
    elapsed = now - p["start"]
    dur = p["dur"]
    alpha = 255
    if elapsed > dur:
        fade = min(600, elapsed - dur)
        alpha = max(0, 255 - int(255 * (fade / 600.0)))
    t = min(1.0, elapsed / 300.0)
    base_y = 80
    y = int(base_y - (1.0 - t) * 20)
    w = 520; h = 52
    x = (WIDTH - w) // 2
    box = pygame.Surface((w,h), pygame.SRCALPHA)
    box.fill((30,30,30, int(200 * (alpha/255))))
    txt = MINI.render(p["msg"], True, (255,255,255))
    box.blit(txt, (20, (h - txt.get_height())//2))
    surface.blit(box, (x,y))

# -------- HELPERS ----------
def center_text(s: str, font, color, surf, x, y):
    txt = font.render(s, True, color)
    rect = txt.get_rect(center=(x,y))
    surf.blit(txt, rect)

# stage positions (flute left, guitar middle-right, drum right)
stage_flute_pos = (flute_rect.centerx, flute_rect.centery)
stage_guitar_pos = (flute_rect.centerx + 140, flute_rect.centery)
stage_drum_pos   = (flute_rect.centerx + 280, flute_rect.centery)

def is_purchased(name: str) -> bool:
    return name in purchased_names

# -------- ANIMATIONS SETUP ----------
# Guitar swing (sinusoidal)
guitar_base_x = stage_guitar_pos[0]
guitar_base_y = stage_guitar_pos[1]
guitar_swing_amplitude = 10   # px
guitar_swing_speed = 0.003    # controls speed (smaller = slower)
guitar_angle = 0.0            # for sin wave

# Drum frames
davul_frames = [davul_frame_1, davul_frame_2]
davul_frame_index = 0
davul_last_change = pygame.time.get_ticks()
davul_frame_duration = 1000  # ms (1s per frame)

# -------- DRAW FUNCTIONS ----------
def draw_main_menu():
    screen.blit(background, (0,0))
    center_text("Capybara Orkestrası", FONT, WHITE, screen, WIDTH//2, HEIGHT//3)
    pygame.draw.rect(screen, RED, start_btn); center_text("Başlat", FONT, WHITE, screen, start_btn.centerx, start_btn.centery)
    pygame.draw.rect(screen, RED, exit_btn); center_text("Çıkış", FONT, WHITE, screen, exit_btn.centerx, exit_btn.centery)
    master_slider.draw(screen); center_text("Genel Ses", SMALL, WHITE, screen, master_slider.rect.centerx, master_slider.rect.y - 16)
    pygame.draw.rect(screen, PANEL_BG, upgrade_btn); center_text("Yükseltmeler", MINI, WHITE, screen, upgrade_btn.centerx, upgrade_btn.centery)
    pygame.draw.rect(screen, PANEL_BG, level_box); screen.blit(MINI.render(f"Seviye: {level}", True, WHITE), (level_box.x+8, level_box.y+4))

def draw_game_ui(mouse_pressed_flag):
    screen.blit(background, (0,0))
    # flute
    screen.blit(flute_pressed_img if mouse_pressed_flag else flute_img, flute_rect)

    # guitar (if purchased) — swing + slight rotation
    if is_purchased("Gitar Capy"):
        # calculate swing offset (sinus)
        t = pygame.time.get_ticks()
        swing = math.sin(t * guitar_swing_speed) * guitar_swing_amplitude
        # small rotation angle proportional to swing
        angle = -swing * 0.6  # negative for aesthetic
        rotated = pygame.transform.rotozoom(guitar_img, angle, 1.0)
        r = rotated.get_rect(center=(guitar_base_x + swing, guitar_base_y))
        screen.blit(rotated, r)

    # drum (if purchased) — frame swap
    if is_purchased("Davul Capy"):
        frame = davul_frames[davul_frame_index]
        r = frame.get_rect(center=stage_drum_pos)
        screen.blit(frame, r)

    # UI
    pygame.draw.rect(screen, RED, upgrade_btn); center_text("Yükseltmeler", MINI, WHITE, screen, upgrade_btn.centerx, upgrade_btn.centery)
    pygame.draw.rect(screen, PANEL_BG, level_box); screen.blit(MINI.render(f"Seviye: {level}", True, WHITE), (level_box.x+8, level_box.y+4))
    # left stats
    screen.blit(FONT.render(f"Notlar: {notes}", True, WHITE), (30,30))
    screen.blit(FONT.render(f"Tıklama Gücü: {click_power}", True, WHITE), (30,70))
    screen.blit(FONT.render(f"Saniyelik Üretim: {idle_per_sec}", True, WHITE), (30,110))

def draw_purchase_panel(selected_idx):
    ph = len(upgrades) * panel_item_h + 120
    pygame.draw.rect(screen, PANEL_BG, (panel_x, panel_y, panel_w, ph), border_radius=8)
    screen.blit(FONT.render("Yükseltmeler", True, WHITE), (panel_x + 12, panel_y + 8))
    yoff = panel_y + 50
    for i, u in enumerate(upgrades):
        bought = is_purchased(u["name"])
        kutu = pygame.Rect(panel_x + 10, yoff - 6, panel_w - 20, 48)
        color = (70,70,70) if bought else ((55,55,90) if i == selected_idx else (60,60,60))
        pygame.draw.rect(screen, color, kutu, border_radius=6)
        text_color = GRAY if bought else WHITE
        screen.blit(MINI.render(f"{u['name']} - {u['price']} not", True, text_color), (panel_x + 18, yoff))
        if bought:
            tag = MINI.render("Alındı", True, GREEN)
            screen.blit(tag, (panel_x + panel_w - tag.get_width() - 14, yoff))
        yoff += panel_item_h

    buy_disabled = (selected_idx is None) or is_purchased(upgrades[selected_idx]["name"])
    btn_color = (120,120,120) if buy_disabled else RED
    pygame.draw.rect(screen, btn_color, buy_btn); center_text("Satın Al", MINI, WHITE, screen, buy_btn.centerx, buy_btn.centery)
    info_y = panel_y + ph - 40
    if selected_idx is not None:
        su = upgrades[selected_idx]; screen.blit(MINI.render(f"Seçili: {su['name']} ({su['price']} not)", True, WHITE), (panel_x + 12, info_y))
    else:
        screen.blit(MINI.render("Seçili: -", True, WHITE), (panel_x + 12, info_y))

def draw_pause_menu():
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA); overlay.fill((0,0,0,180)); screen.blit(overlay, (0,0))
    box = pygame.Rect(WIDTH//2 - 220, HEIGHT//2 - 160, 440, 360); pygame.draw.rect(screen, PANEL_BG, box, border_radius=10)
    center_text("Duraklatıldı", FONT, WHITE, screen, box.centerx, box.y + 30)
    pygame.draw.rect(screen, RED, resume_btn); center_text("Devam Et", MINI, WHITE, screen, resume_btn.centerx, resume_btn.centery)
    pygame.draw.rect(screen, RED, reset_btn); center_text("Kaydı Sıfırla", MINI, WHITE, screen, reset_btn.centerx, reset_btn.centery)
    pygame.draw.rect(screen, RED, mainmenu_btn); center_text("Ana Menüye Dön (Kaydet)", MINI, WHITE, screen, mainmenu_btn.centerx, mainmenu_btn.centery)
    # only slider (no on/off buttons)
    screen.blit(MINI.render("Ses Seviyesi", True, WHITE), (pause_slider.rect.x, pause_slider.rect.y - 20)); pause_slider.draw(screen)

# -------- MUSIC / INTERACTION LOGIC ----------
music_started = False
last_click_time = 0
pause_delay_ms = 2000
mouse_pressed = False

# -------- OTHER STATE ----------
running = True
IN_MENU = True
show_purchase_panel = False
selected_upgrade_idx = None
show_pause = False
last_idle_tick = pygame.time.get_ticks()

# music toggle rect (not shown in pause now but kept)
music_toggle_btn = pygame.Rect(WIDTH//2 - 120, HEIGHT//2 + 100, 240, 40)

# -------- HELPERS / PURCHASE HANDLING ----------
def add_purchase(name):
    global click_multiplier, idle_per_sec, purchased_names
    for u in upgrades:
        if u["name"] == name:
            purchased_names.append(name)
            new = dict(u)
            if u["id"] == "guitar":
                new["surf"] = guitar_img
            elif u["id"] == "drum":
                new["surf"] = None
            else:
                new["surf"] = None
            purchased_objs.append(new)
            click_multiplier = max(click_multiplier, u["mult"])
            idle_per_sec += u.get("idle_bonus", 0)
            add_popup_local(f"Satın alındı! - {u['name']}: {u['mult']}x, idle+{u.get('idle_bonus',0)}")
            print(f"[PURCHASE] {name} alındı.")
            break

def add_popup(msg, dur=1600):
    add_popup_local(msg, dur)

# -------- MAIN LOOP ----------
while running:
    now = pygame.time.get_ticks()
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            to_save = {
                "notes": notes,
                "click_power": click_power,
                "idle_per_sec": idle_per_sec,
                "level": level,
                "purchased_names": purchased_names,
                "click_multiplier": click_multiplier
            }
            save_game(to_save)
            running = False

        # ESC toggles pause (in game)
        if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
            if not IN_MENU:
                show_pause = not show_pause
                pause_slider.value = master_slider.value
            else:
                pass

        # sliders
        master_slider.handle(ev)
        pause_slider.handle(ev)

        # mouse handling
        if ev.type == pygame.MOUSEBUTTONDOWN:
            last_click_time = pygame.time.get_ticks()
            mouse_pressed = True

            if IN_MENU:
                if start_btn.collidepoint(ev.pos):
                    IN_MENU = False
                elif exit_btn.collidepoint(ev.pos):
                    to_save = {
                        "notes": notes,
                        "click_power": click_power,
                        "idle_per_sec": idle_per_sec,
                        "level": level,
                        "purchased_names": purchased_names,
                        "click_multiplier": click_multiplier
                    }
                    save_game(to_save); running = False
                elif upgrade_btn.collidepoint(ev.pos):
                    show_purchase_panel = not show_purchase_panel
            else:
                if show_pause:
                    if resume_btn.collidepoint(ev.pos):
                        show_pause = False
                    elif reset_btn.collidepoint(ev.pos):
                        reset_save()
                        # clear local
                        notes = 0; click_power = 1; idle_per_sec = 0; level = 1
                        purchased_names.clear(); purchased_objs.clear(); click_multiplier = 1.0
                        add_popup_local("Kayıt sıfırlandı!", 1400)
                    elif mainmenu_btn.collidepoint(ev.pos):
                        to_save = {
                            "notes": notes,
                            "click_power": click_power,
                            "idle_per_sec": idle_per_sec,
                            "level": level,
                            "purchased_names": purchased_names,
                            "click_multiplier": click_multiplier
                        }
                        save_game(to_save)
                        IN_MENU = True; show_pause = False; show_purchase_panel = False
                        try:
                            pygame.mixer.music.pause()
                        except:
                            pass
                else:
                    # not paused
                    if upgrade_btn.collidepoint(ev.pos):
                        show_purchase_panel = not show_purchase_panel

                    if show_purchase_panel:
                        ybase = panel_y + 50
                        for i,u in enumerate(upgrades):
                            rect = pygame.Rect(panel_x + 10, ybase + i*panel_item_h - 6, panel_w - 20, 48)
                            if rect.collidepoint(ev.pos):
                                selected_upgrade_idx = i
                                break
                        if buy_btn.collidepoint(ev.pos) and selected_upgrade_idx is not None:
                            u = upgrades[selected_upgrade_idx]
                            if not is_purchased(u["name"]):
                                if notes >= u["price"]:
                                    notes -= u["price"]
                                    purchased_names.append(u["name"])
                                    add_purchase(u["name"])
                                else:
                                    add_popup_local("Yeterli nota yok!", 1200)
                    # click flute to get notes & control music
                    if flute_rect.collidepoint(ev.pos):
                        gained = int(click_power * click_multiplier)
                        notes += gained
                        try:
                            if not music_started:
                                pygame.mixer.music.play(-1)
                                music_started = True
                            else:
                                pygame.mixer.music.unpause()
                        except:
                            pass

        elif ev.type == pygame.MOUSEBUTTONUP:
            mouse_pressed = False

    # --- Frame updates ---
    # volume
    try:
        pygame.mixer.music.set_volume(master_slider.value)
    except:
        pass
    if show_pause:
        try:
            pygame.mixer.music.set_volume(pause_slider.value)
            master_slider.value = pause_slider.value
        except:
            pass

    # auto-pause music if no clicks for pause_delay_ms and not pressing
    if music_started:
        if (now - last_click_time) > pause_delay_ms and (not mouse_pressed):
            try:
                pygame.mixer.music.pause()
            except:
                pass

    # update idle generation
    if not IN_MENU and not show_pause:
        if now - last_idle_tick >= 1000:
            notes += idle_per_sec
            last_idle_tick = now

    # ---------- Animation updates ----------
    # Guitar swing: we use time-based sin -> no state change necessary except base parameters (done in draw)
    # Davul frame switching when purchased
    if is_purchased("Davul Capy"):
        if now - davul_last_change >= davul_frame_duration:
            davul_frame_index = (davul_frame_index + 1) % len(davul_frames)
            davul_last_change = now

    # ---------- Drawing ----------
    if IN_MENU:
        draw_main_menu()
        if show_purchase_panel:
            draw_purchase_panel(selected_upgrade_idx)
    else:
        draw_game_ui(mouse_pressed)
        if show_purchase_panel:
            draw_purchase_panel(selected_upgrade_idx)
        if show_pause:
            draw_pause_menu()

    draw_popups(screen)

    pygame.display.flip()
    clock.tick(60)

# exit save
final_state = {
    "notes": notes,
    "click_power": click_power,
    "idle_per_sec": idle_per_sec,
    "level": level,
    "purchased_names": purchased_names,
    "click_multiplier": click_multiplier
}
save_game(final_state)
pygame.quit()
sys.exit()