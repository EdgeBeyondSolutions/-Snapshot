#!/bin/bash
# Doble clic: revisa/renueva el login de Claude Code, arranca el servidor de
# -Snapshot (si no está corriendo), y abre la app.
cd "$(dirname "$0")"

echo "Revisando sesión de Claude Code..."
if ! claude auth status >/dev/null 2>&1; then
  echo "Tu sesión expiró — abriendo el navegador para volver a iniciar sesión."
  echo "Completa el login en la ventana que se abrió, luego vuelve aquí."
  claude auth login
  if ! claude auth status >/dev/null 2>&1; then
    echo ""
    echo "El login no se completó. Cierra esta ventana e intenta de nuevo con doble clic."
    read -p "Presiona Enter para cerrar..."
    exit 1
  fi
  echo "Sesión iniciada correctamente."
fi

if ! lsof -ti:8787 >/dev/null 2>&1; then
  echo "Iniciando servidor..."
  nohup python3 server.py > .server.log 2>&1 &
  disown
  for i in 1 2 3 4 5 6 7 8 9 10; do
    curl -s -o /dev/null http://localhost:8787/index.html && break
    sleep 0.5
  done
else
  echo "El servidor ya estaba corriendo."
fi

open http://localhost:8787
