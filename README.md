# -Snapshot

Generador de "Digital Presence Snapshot" — el reporte de auditoría gratuito (lead magnet)
que usamos con prospectos, con el mismo diseño y estructura que el reporte de Terra Klean
Solutions. Funciona con o sin sitio web del prospecto.

## Cómo usarlo

1. Corre el servidor local (una sola vez por sesión de trabajo):

   ```bash
   cd "/Users/babemacbookair/Documents/GitHub/-Snapshot"
   python3 server.py
   ```

2. Abre **http://localhost:8787** en el navegador.

3. Llena solo lo que tengas del prospecto — **nombre** (obligatorio), sitio web, Facebook,
   Instagram — y click en **Generate Snapshot**.

4. Espera (la investigación real toma unos minutos, hasta ~8). El servidor invoca a Claude
   Code en modo headless (`claude -p`) usando tu sesión/suscripción actual — sin API key
   separada ni costo por token. Investiga el sitio web (o confirma que no existe), el
   Google Business Profile y las redes/directorios, califica cada pilar (A–F) y redacta los
   hallazgos con evidencia real, siguiendo el playbook en
   [`.claude/skills/snapshot/SKILL.md`](.claude/skills/snapshot/SKILL.md).

5. El reporte se renderiza al instante con el diseño exacto de Terra Klean. Desde ahí:
   - **Descargar HTML** — guarda el archivo autocontenido.
   - **Descargar PDF** — abre el diálogo de impresión nativo del navegador (Guardar como
     PDF); el CSS de impresión ya pagina una sección por página.

Guarda lo descargado en `reports/<Prospecto>-Snapshot/` — convención de nombre: cada
carpeta de prospecto termina en `-Snapshot`.

### Si no quieres correr el servidor

Puedes abrir `index.html` directamente (doble clic, sin servidor) y usar el bloque
plegable **"Prefiero llenarlo manualmente"**: ahí pegas tú mismo cada dato (grados,
hallazgos, quick wins) que Claude te dé por chat. El botón "Generate Snapshot" automático
solo funciona con el servidor corriendo.

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
