# Portfolio — Sabrina Romero

Portfolio de fotografía, contenido y dirección visual. Rosario, Argentina.

**En vivo:** https://sabrinapromero.github.io

---

## Cómo está armado

El sitio es **un solo archivo HTML autosuficiente**. Las imágenes, la tipografía de marca y los estilos van embebidos: no depende de ningún servidor, CDN ni base de datos. Se puede abrir con doble clic o servir desde cualquier hosting estático.

```
portfolio.tpl.html   plantilla con tokens {{IMG:...}} {{GFX:...}} {{FONT:...}}
scripts/construir.py inyecta imágenes, gráficos y fuentes como base64
index.html           resultado (lo que sirve GitHub Pages) — generado, no editar
assets/web/          imágenes optimizadas a 820 px
```

Para regenerar el sitio después de tocar la plantilla:

```bash
python scripts/construir.py
```

Editar `index.html` a mano no sirve: el próximo build lo pisa. Los cambios van siempre en `portfolio.tpl.html`.

## Identidad

Paleta y tipografías salen del manual de marca (crema `#F6F1E7`, tinta `#1C2452`, azul eléctrico `#2E45E0`, rosa chicle `#F276C8`). Titulares en Bricolage Grotesque, cuerpo en Work Sans, datos en Space Mono, y Bootzy como firma —una o dos palabras por pieza, nunca más.

El sitio es de un solo tema, en crema: el manual no admite fondo blanco ni negro puro, así que no hay variante oscura.

## Otros archivos

- `scripts/reel.py` — genera el reel de presentación en 1080×1920 con Pillow y ffmpeg
- `scripts/descargar.py` — baja de Instagram las publicaciones seleccionadas
- `reel-portfolio.md` — guión del reel: tiempos, planos y textos
