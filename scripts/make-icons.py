# Draws the app icon (Kaaba with gold band on kiswa black) at every size the PWA needs.
# Run: python3 scripts/make-icons.py
from PIL import Image, ImageDraw
import math

def icon(size, maskable=False, out=None):
    S = 1024
    img = Image.new("RGB", (S, S), (13, 14, 15))
    d = ImageDraw.Draw(img)
    gold = (201, 165, 77)
    # faint 8-point star behind the Kaaba
    cx, cy, r = S/2, S/2, (300 if maskable else 400)
    for k in range(2):
        pts = [(cx + r*math.cos(k*math.pi/4 + j*math.pi/2), cy + r*math.sin(k*math.pi/4 + j*math.pi/2)) for j in range(4)]
        d.polygon(pts, outline=(70, 60, 35), width=10)
    # Kaaba
    w = 330 if maskable else 440
    h = int(w*1.05)
    x0, y0 = cx - w/2, cy - h/2 + 20
    d.rectangle([x0, y0, x0+w, y0+h], fill=(4, 4, 5), outline=(90, 75, 40), width=6)
    band = int(h*0.1)
    by = y0 + int(h*0.2)
    d.rectangle([x0, by, x0+w, by+band], fill=gold)
    # door
    dw, dh = int(w*0.18), int(h*0.42)
    dx = x0 + w*0.62
    d.rectangle([dx, y0+h-dh-int(h*0.08), dx+dw, y0+h-int(h*0.08)], outline=gold, width=8)
    img.resize((size, size), Image.LANCZOS).save(out)

icon(192, out="public/icons/icon-192.png")
icon(512, out="public/icons/icon-512.png")
icon(512, maskable=True, out="public/icons/maskable-512.png")
icon(180, out="public/icons/apple-touch-icon.png")
icon(32, out="public/icons/favicon-32.png")
print("icons done")
