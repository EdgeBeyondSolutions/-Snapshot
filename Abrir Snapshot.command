#!/bin/bash
# Doble clic: arranca el servidor de -Snapshot (si no está corriendo) y abre la app.
cd "$(dirname "$0")"

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
