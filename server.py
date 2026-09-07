#!/usr/bin/env python3
"""
Local server for the -Snapshot app.

Serves index.html/template.html/assets, and exposes POST /generate which
shells out to the Claude Code CLI in headless mode (`claude -p ...`) to
research a prospect and produce the finished Digital Presence Snapshot
report as a single HTML string. Uses the machine's existing Claude Code
login — no separate Anthropic API key, no per-token billing.

Run:
    python3 server.py
Then open:
    http://localhost:8787
"""
import base64
import http.server
import json
import re
import subprocess
import sys
from pathlib import Path

PORT = 8787
ROOT = Path(__file__).resolve().parent
SKILL_PROMPT_PATH = ROOT / ".claude" / "skills" / "snapshot" / "SKILL.md"
CLAUDE_TIMEOUT_SECONDS = 600

FENCE_RE = re.compile(r"^```(?:html)?\s*\n|\n```\s*$", re.MULTILINE)


def strip_fences(text: str) -> str:
    text = text.strip()
    text = FENCE_RE.sub("", text).strip()
    return text


LANGUAGE_NAMES = {"en": "English (US)", "es": "Spanish (Mexico — natural business Spanish, tú/informal but professional, as EdgeBeyond Solutions would write it for a Mexican prospect)"}


def build_prompt(name: str, website: str, facebook: str, instagram: str, city: str, lang: str) -> str:
    website_line = website or "none provided — search for one; if you can't confidently find one, treat this prospect as having no website"
    facebook_line = facebook or "not provided — search for one; if none found, treat as absent"
    instagram_line = instagram or "not provided — search for one; if none found, treat as absent"
    city_line = city or "not provided"
    language_name = LANGUAGE_NAMES.get(lang, LANGUAGE_NAMES["en"])
    return f"""Follow the playbook in .claude/skills/snapshot/SKILL.md in this directory exactly.

Generate a "Digital Presence Snapshot" report for this prospect:
- Business name: {name}
- City/region: {city_line}
- Website: {website_line}
- Facebook: {facebook_line}
- Instagram: {instagram_line}

This is a non-interactive, single-shot run — there is no human available to answer
clarifying questions, so you must NEVER stop to ask one. If the business name is ambiguous
(multiple unrelated businesses share it) and no city/region was given, use the strongest
available signal to pick the single most likely match (the website/socials provided, or
otherwise the most established/highest-review-count candidate) and proceed. In that case,
add one explicit sentence near the top of the report (in the hero lede or overall summary)
stating the assumption plainly, e.g. "Multiple businesses share this name; this snapshot
assumes '<name>' in <city> is the target" — written in {language_name} like the rest of the
report. Do not leave the report unfinished and do not output anything other than the final
HTML document under any circumstance.

Write the ENTIRE report — every heading, label, finding, quick win, and CTA — in
{language_name}. Translate the fixed chrome text too (e.g. "Free Snapshot Report", "Grade",
"Download PDF", pillar names, footer disclaimer) into that language; don't leave any of it
in English if the target language isn't English. Keep the prospect's own business name and
any verbatim evidence quotes (like a footer copyright line) exactly as found, untranslated.

Use WebSearch and WebFetch to actually research this business — its website (if any),
Google Business Profile, and social/directory presence. Do not invent facts; only include
things you found or verified. Grade each pillar honestly per the rubric in SKILL.md.

Read template.html in this directory (read-only, for the design/HTML structure) and fill
it with your researched content, following every rule in SKILL.md (including the
no-website case if this prospect turns out to have no live site). Wherever the logo image
src is needed, use the literal placeholder text `{{{{LOGO_DATA_URI_PLACEHOLDER}}}}` verbatim
— do not generate, encode, or embed any image data yourself.

Do not write, edit, or execute any files or scripts, and do not use the Bash, Write, or
Edit tools. This is not a task to automate — your ENTIRE final response must be nothing but
the finished HTML document itself: starting with <!DOCTYPE html> and ending with </html>,
with no markdown code fences, no commentary, and no explanation before or after it."""


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def log_message(self, fmt, *args):
        sys.stderr.write("[server] " + (fmt % args) + "\n")

    def do_POST(self):
        if self.path != "/generate":
            self.send_error(404)
            return

        length = int(self.headers.get("Content-Length", 0))
        try:
            payload = json.loads(self.rfile.read(length) or b"{}")
        except json.JSONDecodeError:
            self.send_json(400, {"error": "Invalid JSON body"})
            return

        name = (payload.get("name") or "").strip()
        if not name:
            self.send_json(400, {"error": "El nombre del prospecto es requerido"})
            return
        website = (payload.get("website") or "").strip()
        facebook = (payload.get("facebook") or "").strip()
        instagram = (payload.get("instagram") or "").strip()
        city = (payload.get("city") or "").strip()
        lang = (payload.get("lang") or "en").strip()
        if lang not in LANGUAGE_NAMES:
            lang = "en"

        prompt = build_prompt(name, website, facebook, instagram, city, lang)

        try:
            result = subprocess.run(
                [
                    "claude", "-p", prompt,
                    "--output-format", "text",
                    "--allowedTools", "WebSearch WebFetch Read",
                    "--disallowedTools", "Bash Write Edit",
                    "--effort", "medium",
                ],
                cwd=str(ROOT),
                capture_output=True,
                text=True,
                timeout=CLAUDE_TIMEOUT_SECONDS,
            )
        except subprocess.TimeoutExpired:
            self.send_json(504, {"error": f"La investigación tardó más de {CLAUDE_TIMEOUT_SECONDS}s. Intenta de nuevo."})
            return
        except FileNotFoundError:
            self.send_json(500, {"error": "No se encontró el comando 'claude' en PATH."})
            return

        debug_path = ROOT / ".last_generate_debug.txt"
        debug_path.write_text(
            f"RETURNCODE: {result.returncode}\n\n--- STDOUT ---\n{result.stdout}\n\n--- STDERR ---\n{result.stderr}\n"
        )

        if result.returncode != 0:
            detail = (result.stderr or result.stdout or "").strip()[-2000:] or "(sin detalle)"
            if "OAuth session expired" in detail or "Failed to authenticate" in detail:
                self.send_json(500, {"error": "Tu sesión de Claude Code expiró. Abre Terminal, corre \"claude auth\" para volver a iniciar sesión, y vuelve a intentar."})
                return
            self.send_json(500, {"error": f"Claude CLI falló: {detail}"})
            return

        html = strip_fences(result.stdout)
        if "<!doctype html>" not in html.lower():
            self.send_json(500, {"error": "La respuesta no contenía un documento HTML válido.", "raw": html[:4000]})
            return

        logo_b64 = base64.b64encode((ROOT / "assets" / "logo-edgebeyond.svg").read_bytes()).decode("ascii")
        html = html.replace("{{LOGO_DATA_URI_PLACEHOLDER}}", f"data:image/svg+xml;base64,{logo_b64}")

        self.send_json(200, {"html": html})

    def send_json(self, status: int, data: dict):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    server = http.server.ThreadingHTTPServer(("localhost", PORT), Handler)
    print(f"-Snapshot corriendo en http://localhost:{PORT}  (Ctrl+C para detener)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
