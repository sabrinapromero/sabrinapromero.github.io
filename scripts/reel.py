# Arma el reel de portfolio en 1080x1920 / 30 fps, con la misma identidad que la web.
# Los frames se generan con Pillow y se transmiten a ffmpeg por stdin (no tocan el disco).

import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
OUT = "reel-portfolio.mp4"
MARCA = r"C:\Users\Usuario\Documents\Diseños\Mi marca\Manual de Marca"

CREMA = (246, 241, 231)
TINTA = (28, 36, 82)
AZUL = (46, 69, 224)
ROSA = (242, 118, 200)
ROSA_CLARO = (248, 172, 221)
LINEA = (216, 208, 190)
MUTED = (88, 95, 134)

F = lambda n, s: ImageFont.truetype(os.path.join(MARCA, "Fuentes", n + ".ttf"), s)
DISPLAY = "BricolageGrotesque-ExtraBold"
MONO_B = "SpaceMono-Bold"
BODY = "WorkSans-Medium"
FIRMA = "BootzyTM"

gfx = lambda n: Image.open(os.path.join(MARCA, "Elementos-Graficos-PNG", n + ".png")).convert("RGBA")

# marca, rotulo, color, dos imagenes
BLOQUES = [
    ("Caso 01", "HORNEA \xb7 C\xc1LIDO",  (184, 135, 31), "hornea_DXCumKCmHEF",   "hornea_DcouoxbsTx4"),
    ("Caso 02", "LOYOLA \xb7 CERCANO",  (2, 133, 147),   "loyola_DYWzpM5A049",   "loyola_DZdphDhgMXU"),
    ("Caso 03", "VINCENZO \xb7 SOBRIO", (150, 17, 13),   "vincenzo_DXx7bmHjWBs", "vincenzo_DcgXyTACiMx"),
    ("Caso 04", "C\xc1PSULA \xb7 ALEGRE", (217, 83, 26),  "capsula_DM9AchXNRfm",  "capsula_DaZG2R2DeF2"),
    ("Caso 05", "BOSCHI \xb7 PRECISO",  (79, 112, 129),  "boschi_DZvXkcimN3M",   "boschi_DbZMK72GGue"),
]

PHOTO = (60, 260, 1020, 1560)          # marco de foto, igual que el encuadre de la web
MARGIN = 84


def load(name):
    return Image.open(f"assets/web/{name}.jpg").convert("RGB")


def cover(img, bw, bh, zoom=1.0, oy=0.5):
    """Recorta img al aspecto bw:bh con un zoom dado y devuelve bw x bh.
    oy posiciona el recorte vertical: 0 arriba, 0,5 centrado, 1 abajo."""
    sw, sh = img.size
    scale = max(bw / sw, bh / sh) * zoom
    cw, ch = min(bw / scale, sw), min(bh / scale, sh)
    left = max(0.0, min((sw - cw) / 2, sw - cw))
    top = max(0.0, min((sh - ch) * oy, sh - ch))
    return img.resize((bw, bh), Image.LANCZOS, box=(left, top, left + cw, top + ch))


def lines(d, txt, font, x, y, fill, lh):
    for i, ln in enumerate(txt):
        d.text((x, y + i * lh), ln, font=font, fill=fill)
    return y + len(txt) * lh


def paste(base, png, xy, width):
    w = width
    h = round(png.height * w / png.width)
    base.paste(png.resize((w, h), Image.LANCZOS), xy, png.resize((w, h), Image.LANCZOS))


# ---------------------------------------------------------------- placas fijas

def card_hook():
    im = Image.new("RGB", (W, H), TINTA)
    d = ImageDraw.Draw(im)
    f = F(DISPLAY, 100)
    fb = F(FIRMA, 146)
    y, lh = 700, 122
    d.text((MARGIN, y), "Cinco marcas", font=f, fill=CREMA)
    d.text((MARGIN, y + lh), "que no se ", font=f, fill=CREMA)
    # sobre fondo oscuro la firma va en rosa claro, no en rosa chicle (regla del manual)
    d.text((MARGIN + d.textlength("que no se ", font=f), y + lh - 24), "hablan", font=fb, fill=ROSA_CLARO)
    d.text((MARGIN, y + 2 * lh), "entre s\xed.", font=f, fill=CREMA)
    paste(im, gfx("destello-rosa"), (W - 250, 210), 180)
    return im


def card_reveal_b(retrato_sq):
    im = Image.new("RGB", (W, H), CREMA)
    d = ImageDraw.Draw(im)
    im.paste(retrato_sq, (MARGIN, 700))
    d.rectangle([MARGIN, 700, MARGIN + 220, 920], outline=LINEA)
    f = F(DISPLAY, 96)
    y = 1040
    y = lines(d, ["Cada una", "encontr\xf3"], f, MARGIN, y, TINTA, 116)
    lines(d, ["la suya."], f, MARGIN, y, AZUL, 116)
    paste(im, gfx("subrayado-ondulado"), (MARGIN, y + 112), 400)
    return im


def card_cierre(retrato_sq):
    im = Image.new("RGB", (W, H), CREMA)
    d = ImageDraw.Draw(im)
    paste(im, gfx("destello-rosa"), (W - 250, 250), 180)
    d.text((MARGIN, 700), "Sabrina", font=F(DISPLAY, 128), fill=TINTA)
    d.text((MARGIN, 836), "Romero", font=F(DISPLAY, 128), fill=TINTA)
    fb = F(BODY, 42)
    d.text((MARGIN, 1030), "Contenido, fotograf\xeda", font=fb, fill=MUTED)
    d.text((MARGIN, 1086), "y direcci\xf3n visual", font=fb, fill=MUTED)
    d.text((MARGIN, 1142), "Rosario, Argentina", font=fb, fill=MUTED)
    d.rectangle([MARGIN, 1270, MARGIN + 620, 1352], fill=AZUL)
    d.text((MARGIN + 28, 1294), "PORTFOLIO EN LA BIO", font=F(MONO_B, 34), fill=CREMA)
    return im


# ---------------------------------------------------------------- frames

def frame_bloque(img, caso, rotulo, color, t):
    im = Image.new("RGB", (W, H), CREMA)
    d = ImageDraw.Draw(im)
    x0, y0, x1, y1 = PHOTO
    im.paste(cover(img, x1 - x0, y1 - y0, 1.0 + 0.07 * t), (x0, y0))
    d.rectangle([x0 - 1, y0 - 1, x1, y1], outline=LINEA)
    d.text((MARGIN, 196), caso.upper(), font=F(MONO_B, 32), fill=AZUL)
    d.rectangle([x0, y1 + 46, x0 + 14, y1 + 96], fill=color)
    d.text((x0 + 36, y1 + 52), rotulo, font=F(MONO_B, 36), fill=color)
    return im


def frame_reveal_a(retrato, t):
    im = Image.new("RGB", (W, H), CREMA)
    im.paste(cover(retrato, W, H, 1.0 + 0.05 * t), (0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 1276, W, H], fill=TINTA)
    f = F(DISPLAY, 78)
    lines(d, ["Una marca no tiene voz", "hasta que alguien", "se la escribe."], f, MARGIN, 1364, CREMA, 94)
    return im


def main():
    retrato = Image.open("assets/reel_retrato.jpg").convert("RGB")
    retrato_sq = cover(retrato, 220, 220, oy=0.16)

    hook, rev_b, cierre = card_hook(), card_reveal_b(retrato_sq), card_cierre(retrato_sq)
    imgs = {n: load(n) for b in BLOQUES for n in b[3:]}

    plan = []                                            # (funcion_de_frame, cantidad)
    plan.append((lambda t: hook, 75))                    # 2,5 s
    for caso, rot, col, a, b in BLOQUES:                 # 5 x 2,4 s
        for name in (a, b):
            plan.append((lambda t, n=name, c=caso, r=rot, k=col: frame_bloque(imgs[n], c, r, k, t), 36))
    plan.append((lambda t: frame_reveal_a(retrato, t), 81))   # 2,7 s
    plan.append((lambda t: rev_b, 78))                        # 2,6 s
    plan.append((lambda t: cierre, 105))                      # 3,5 s

    total = sum(n for _, n in plan)
    print(f"generando {total} frames ({total/FPS:.1f} s)...")

    ff = subprocess.Popen([
        "ffmpeg", "-loglevel", "error", "-y",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart", OUT,
    ], stdin=subprocess.PIPE)

    done = 0
    for fn, n in plan:
        for i in range(n):
            ff.stdin.write(fn(i / max(n - 1, 1)).tobytes())
            done += 1
            if done % 120 == 0:
                print(f"  {done}/{total}")
    ff.stdin.close()
    if ff.wait() != 0:
        sys.exit("ffmpeg fallo")
    print(f"{OUT}: {os.path.getsize(OUT)/1024/1024:.1f} MB")


main()
