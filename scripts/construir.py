import base64, os, re

TPL = "portfolio.tpl.html"
# portfolio.html alimenta el artifact de Claude; index.html es el que sirve GitHub Pages.
OUTS = ["portfolio.html", "index.html"]
MARCA = r"C:\Users\Usuario\Documents\Diseños\Mi marca\Manual de Marca"


def b64(path):
    with open(path, "rb") as fh:
        return base64.b64encode(fh.read()).decode()


def img_uri(code):
    for f in os.listdir("assets/web"):
        if f.endswith(f"_{code}.jpg"):
            return "data:image/jpeg;base64," + b64(os.path.join("assets/web", f))
    raise SystemExit(f"FALTA imagen para {code}")


def gfx_uri(name):
    p = os.path.join(MARCA, "Elementos-Graficos-PNG", name + ".png")
    return "data:image/png;base64," + b64(p)


def font_b64(name):
    return b64(os.path.join(MARCA, "Fuentes", name + ".ttf"))


src = open(TPL, encoding="utf-8").read()

for kind, fn in (("IMG", img_uri), ("GFX", gfx_uri), ("FONT", font_b64)):
    for name in sorted(set(re.findall(r"\{\{%s:([A-Za-z0-9_.-]+)\}\}" % kind, src))):
        src = src.replace("{{%s:%s}}" % (kind, name), fn(name))

leftover = re.findall(r"\{\{[A-Z]+:[^}]+\}\}", src)
if leftover:
    raise SystemExit("tokens sin resolver: " + ", ".join(sorted(set(leftover))))

for out in OUTS:
    open(out, "w", encoding="utf-8").write(src)
print(f"{' + '.join(OUTS)}: {src.count('<img ')} imagenes, {os.path.getsize(OUTS[0])/1024:.0f} KB")
