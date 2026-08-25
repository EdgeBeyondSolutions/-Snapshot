# -Snapshot

Generador de "Digital Presence Snapshot" — el reporte de auditoría gratuito (lead magnet)
que usamos con prospectos, con el mismo diseño y estructura que el reporte de Terra Klean
Solutions. Funciona con o sin sitio web del prospecto.

## Cómo usarlo

1. Doble clic en **`Abrir Snapshot.command`** (en esta carpeta). Arranca el servidor local
   solo si no está ya corriendo — no queda nada consumiendo recursos cuando no lo usas — y
   abre la app en `http://localhost:8787`.

2. Llena solo lo que tengas del prospecto — **nombre** (obligatorio), sitio web, Facebook,
   Instagram — y click en **Generate Snapshot**.

3. Espera (la investigación real toma unos minutos, hasta ~8). El servidor invoca a Claude
   Code en modo headless (`claude -p`) usando tu sesión/suscripción actual — sin API key
   separada ni costo por token. Investiga el sitio web (o confirma que no existe), el
   Google Business Profile y las redes/directorios, califica cada pilar (A–F) y redacta los
   hallazgos con evidencia real, siguiendo el playbook en
   [`.claude/skills/snapshot/SKILL.md`](.claude/skills/snapshot/SKILL.md).

4. El reporte se renderiza al instante con el diseño exacto de Terra Klean. Desde ahí:
   - **Descargar HTML** — guarda el archivo autocontenido.
   - **Descargar PDF** — abre el diálogo de impresión nativo del navegador (Guardar como
     PDF); el CSS de impresión ya pagina una sección por página.

Guarda lo descargado en `reports/<Prospecto>-Snapshot/` — convención de nombre: cada
carpeta de prospecto termina en `-Snapshot`.

**Importante:** no abras `index.html` con doble clic directamente — eso lo carga sin
servidor (`file://`) y el botón automático no funciona ahí (la app te lo advierte con un
banner si lo haces). Siempre entra por `Abrir Snapshot.command` o, si el servidor ya está
corriendo, por `http://localhost:8787`.

### Si no quieres correr el servidor

Puedes abrir `index.html` directamente y usar el bloque plegable **"Prefiero llenarlo
manualmente"**: ahí pegas tú mismo cada dato (grados, hallazgos, quick wins) que Claude te
dé por chat. Esa parte funciona 100% sin servidor.

## Estructura

- `index.html` — la app: formulario simple (auto) + formulario manual (fallback) + el
  generador/visor de reportes, todo en un solo archivo.
- `server.py` — servidor local (solo librería estándar de Python) que expone `POST
  /generate` e invoca `claude -p` en modo headless para investigar y redactar el reporte.
- `template.html` — referencia del diseño maestro (mismo HTML/CSS que usa `index.html`
  internamente para el formulario manual).
- `assets/logo-edgebeyond.svg` — logo de EdgeBeyond Solutions, usado en cada reporte.
- `.claude/skills/snapshot/SKILL.md` — el playbook que sigue el generador automático:
  rúbrica de calificación, tono de redacción, y reglas para el caso "sin sitio web".
- `reports/<Prospecto>-Snapshot/` — guarda aquí los HTML/PDF descargados por prospecto.
