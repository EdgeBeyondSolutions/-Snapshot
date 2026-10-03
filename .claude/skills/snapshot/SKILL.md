---
name: snapshot
description: Generate a "Digital Presence Snapshot" lead-gen report (HTML, printable to PDF) for a prospect business, auditing their website (or lack of one), Google Business Profile, and social/directory listings. Use when the user asks to "genera el snapshot para <prospecto>", "haz un snapshot de <negocio>", or similar, from within the -Snapshot project.
---

> **This folder lives in `Dropbox/GitHub/Apps/-Snapshot` and the user keeps it set to
> "online-only" between uses to save local disk space.** If any file here reads as 0 bytes
> (to `cat`, `Read`, `git`, etc.), that almost always means Dropbox hasn't finished
> downloading it locally yet — it is NOT data loss or corruption, the real content is safe
> in Dropbox's cloud. Before editing or running anything here, ask the user to confirm the
> folder is actually downloaded/available offline (not just that they toggled it), and
> re-check file sizes rather than concluding the project is broken.

# Digital Presence Snapshot generator

Produces the same report format built for Terra Klean Solutions: a cold, evidence-based
audit of a prospect's online presence, used as a free lead-magnet by EdgeBeyond Solutions
to book a 30-minute walkthrough call. One self-contained HTML file — the report itself has
no download/print button embedded; the `index.html` app's toolbar handles both Download
HTML and Download PDF. PDF is rendered server-side by `server.py` (`POST /render-pdf`,
headless Chrome with `--no-pdf-header-footer`) — deliberately not the browser's own print
dialog, because that dialog's default "Headers and footers" option stamps the date,
`localhost:8787`, and page numbers onto every page, and a report went out to a real
prospect that way once. Don't add a print button inside template.html/the generated report
— that was tried and caused a visible duplicate with the app's own toolbar button.

**Primary path:** `server.py` runs this exact playbook automatically — the user opens
`index.html` at http://localhost:8787, types just the prospect's name (+ optionally
website/Facebook/Instagram), and clicks "Generate Snapshot". That request is served by
`server.py` shelling out to `claude -p` (this CLI, headless) with this SKILL.md as its
instructions, `WebSearch`/`WebFetch`/`Read` tools only, and a strict "output nothing but
the final HTML document" contract. You (an interactive Claude Code session) only need to
run these steps by hand if the user asks you directly in chat, or if they use the manual
fallback form in `index.html` instead of the automated one.

## Inputs

- **Prospect business name** (required).
- **Known website URL** (optional — if not given, search for it first).
- **City/region** (optional but helps disambiguate search results and GBP lookup).
- **Report language** — English (US) or Spanish (Mexico). EdgeBeyond serves prospects in
  both the US and Mexico; if not specified, ask, or infer from context (a `.mx` domain, a
  Mexican city, Spanish-language site content). Write the ENTIRE report in that
  language — every heading, label, finding, quick win, and CTA, not just the findings —
  translating fixed chrome text too ("Free Snapshot Report", "Grade",
  pillar names, footer disclaimer). Keep the prospect's own business name and any verbatim
  evidence quotes exactly as found, untranslated. Spanish should read as natural business
  Spanish for Mexico (tú/informal but professional), not a literal word-for-word translation.
- **Datos verificados manualmente** (optional, free text) — facts the user already confirmed
  firsthand (e.g. "saw on Google Maps: unclaimed listing, 139 reviews, 4.2★"; "Facebook has
  2,700 followers, 11 reviews"). **Treat anything given here as ground truth that overrides
  your own research.** This exists because Google Maps, Facebook, and Instagram actively
  block automated fetches — see the rule under Step 1 — so a human who actually opened the
  real page is a more reliable source than this tool's own WebFetch attempt on that same
  page. Reconcile: if your research disagrees with a verified fact, the verified fact wins,
  and don't describe the two as if they're both independently confirmed.

## Step 1 — Research (use WebSearch / WebFetch)

Investigate exactly what a cold prospect would find, tonight, on their phone:

1. **Website.** Search `"<business name>" <city>` and variants. If a site exists, fetch it
   and check: how dated the design/template is (look for footer copyright years, template
   credits), whether there's a real lead-capture form (vs. phone-only), any trust claims
   that can be verified (BBB accreditation, certifications, associations — cross-check
   against the real source, e.g. BBB's own site), and NAP consistency (Name/Address/Phone)
   across the site itself. If **no website can be found**, that is itself the headline
   finding — do not force a critique of a site that doesn't exist.
2. **Google Business Profile.** Search `"<business name>" <city> google maps` /
   `<business name> reviews`. Check: is the listing claimed (look for "claim this
   business" prompts, or an unclaimed/unverified status), review count and rating, photo
   count, category accuracy, and whether hours/NAP match the website.
3. **Social & directories.** Check for LinkedIn, Facebook, Instagram company presence and
   whether they're active (recent posts) or dormant/absent. Check directory listings
   relevant to the industry (BBB, HomeAdvisor, Yelp, Indeed, D&B, industry-specific
   directories) for existence and NAP consistency across them.

Keep concrete evidence for anything you plan to quote verbatim (footer text, exact phone
numbers/addresses found, review counts) — the report's credibility depends on specific,
checkable facts, not vague claims.

**"Couldn't access" is not "doesn't exist" — this caused a real false claim once, fix
it at the source.** Google Maps, Facebook, and Instagram actively block automated
WebFetch requests (you'll typically get a captcha/consent wall or an empty shell page, not
the real content). When that happens:
- Do NOT write a finding that implies the profile/account is absent, unclaimed-and-empty,
  or ungraded-for-lack-of-data as if that were a confirmed observation. A sentence like "no
  regresó una ficha oficial con calificación, número de reseñas o fotos" reads to the
  prospect as "you have no GBP presence," which may be flatly false and contradict what
  they can see themselves by opening the page — exactly what happened with Balneario Las
  Torres (it has 139 reviews, 4.2★, unclaimed).
- First, try WebSearch instead of WebFetch for that specific thing — a search for
  `"<business name>" reviews` or `"<business name>" google maps` very often surfaces the
  rating and review count directly in the search snippet text even when the page itself is
  blocked.
- If WebSearch snippets don't surface it either, say so plainly and narrowly: "No pudimos
  cargar directamente la ficha de Google (Google bloquea accesos automatizados) y la
  búsqueda tampoco mostró calificación o número de reseñas en el resultado." Grade that
  pillar as unknown/not-gradable-with-confidence rather than F, and do not invent a
  narrative around an assumed absence.
- If the **Datos verificados manualmente** input (see Inputs above) supplies the real
  numbers, use those — they're from a human who actually opened the page, which beats this
  tool's own blocked fetch every time.
- **Stay consistent across the WHOLE report, not just that one finding.** This exact
  failure happened: Pilar 02 correctly said "no pudimos verificar el estado de su ficha,"
  but another sentence elsewhere (overall summary) still asserted a definite negative —
  "el interés no se está convirtiendo en reseñas" — about that same unverified channel.
  Once you've written "couldn't verify X," grep your own draft mentally for any other
  place you're implying something definite about X, and soften or remove it. An unverified
  pillar should read as genuinely unverified everywhere it's mentioned, not confidently
  negative in the hero/summary and merely uncertain in its own section.

**Claims naming a real third party (a public official, government body, news outlet,
named competitor, etc.) need an actually-fetched source, every time — no exceptions.**
Before including something like "the governor recommended this business, covered by
[Publication]," you must have fetched (via WebSearch/WebFetch, this run) a real, specific
URL that confirms it, and you should be able to name that URL if asked. Don't include a
claim like this because it "sounds plausible" or matches a pattern — attributing something
false to a real public figure or a real publication in a document sent to a client is a
legal/reputational risk, not just a factual error. (In the Las Torres case this particular
claim turned out to be true and verifiable — lasillarota.com and milenio.com both have
real March 2024 articles — but it was included without the agent having confirmed that at
the time, which was the actual process failure, not the content.)

## Step 2 — Grade each pillar (A–F)

Grade honestly, the way a prospect's next customer would judge them:

- **Website:** A/B = modern, mobile-first, clear CTA, consistent trust signals. C = dated
  but functional. D = seriously dated, phone-only contact, or trust-claim problems. F = no
  working site, or one that actively misleads (broken trust claims, dead links).
  **No website at all is an automatic F** — reframe the whole pillar around that absence.
- **Google Business Profile:** A/B = claimed, actively managed, real reviews, photos. C =
  claimed but thin (few reviews/photos). D = claimed but neglected or genuinely unclaimed
  (confirmed, not assumed). F = confirmed nonexistent. If direct access was blocked and
  neither WebSearch snippets nor **Datos verificados manualmente** could confirm the real
  state, do not default to F — grade conservatively (C) and say explicitly in the finding
  that this pillar couldn't be fully verified, rather than implying confirmed absence.
- **Social:** graded on whether there's an active, prospect-facing channel (not just a
  dormant LinkedIn page).
- **Listings:** graded on NAP consistency across directories, not on how many directories
  they're in.
- **Overall grade:** roughly the worst 1–2 pillars pull it down — don't average blindly. A
  business can have decades of real credibility (certifications, tenure, marquee clients)
  and still land a D+/C- overall because none of it is discoverable online. That tension
  ("doing the work vs. the internet not backing it up") is the emotional core of the hero
  copy — find the prospect's real, verifiable credibility signal (years in business, a
  notable client, a certification) and use it there.

## Step 3 — Write the copy, in voice

Tone: direct, second-person ("you/your"), evidence-first, never insulting — the target
reader is the business owner. Every finding should answer "so what, concretely" (what a
real prospect does because of this problem), not just describe the issue abstractly.
Findings get a status chip: `critical` (real problem, costs leads), `warn` (real but
lower-stakes), `pass` (genuinely fine — include 1 pass finding per pillar where honestly
earned, it makes the critical ones more credible).

Two guardrails, added after a copy review flagged both:

- **Never state a generic statistic you can't attribute** (e.g. "90% of buyers look online
  first"). It undermines a report whose whole pitch is "evidence-first" if the prospect
  fact-checks it and it's unsourced. Make the same point with something you *can* stand
  behind: the business's own verified gap (no GBP reviews, no working contact form), not an
  invented industry-wide number.
- **When a finding involves a false or outdated trust claim** (e.g. a site claims an
  accreditation it doesn't have), frame it as something that likely slipped through when
  the site/listing was built, not as a deliberate misrepresentation — the fact itself
  (verified against the real source) does the persuading; don't editorialize about intent.

- **Hero H1**: a short, specific tension statement about this business (≤16 characters
  wide is not a rule, just keep it punchy — see Terra Klean's "Your business is doing the
  work. Your internet presence isn't backing it up.").
- **Hero lede**: 1–2 sentences framing the audit method (what you looked at, from whose
  perspective).
- **Overall summary**: 1 sentence anchoring the grade to the business's real, verifiable
  credibility (tenure, a marquee client/project, certifications) — the gap between earned
  trust and online trust IS the pitch.
- **Per-pillar h2**: a specific, factual headline (not generic — "terraklean.com is
  running on a 2010 template", not "Website needs work").
- **Findings**: 2–4 per pillar. Title = h4, short and specific. Body = 1–3 sentences,
  evidence-first, ending on the concrete cost. Use the `<div class="evidence">` block only
  when you have an exact quote/data point worth showing verbatim (footer text, conflicting
  phone numbers, etc.) — don't force it.
- **Five Quick Wins**: exactly 5, ranked by "cost to ignore" (cheapest/highest-leverage
  first — claiming a free GBP listing typically ranks #1). Each gets a short `impact` tag
  (e.g. "Highest impact · Free", "Reputation risk", "SEO foundation", "Lead capture", "Full
  rebuild").
- **CTA**: keep EdgeBeyond Solutions branding fixed. The button links to the real Google
  Calendar booking page — `https://calendar.app.google/11WtesnFPFsi62aZ6`, `target="_blank"
  rel="noopener"` — not a `mailto:` link. This is intentional: a real scheduling link is
  actual lead capture (name/email/time collected by Google), where a mailto is not. The
  same fixed URL is used for every prospect — nothing to customize per report. If this
  booking page ever shows "Appointment not found," it means its availability window
  expired in Google Calendar (it was set for specific dates, not recurring) — that's fixed
  in Google Calendar itself (make the schedule recurring / extend its dates), not in this
  codebase; only update this URL if the user gives you a genuinely new link.

## Step 4 — Hand off the content

The actual report is generated by **`index.html`** (a self-contained form + generator, no
backend) — you do not edit `template.html` or write HTML by hand. `template.html` exists
only as a design reference; the generation logic lives inline in `index.html`'s JS.

Your job at this point is to hand the user everything `index.html`'s form asks for, laid
out clearly enough to paste field-by-field:

1. Prospect name, and today's date if not obvious.
2. Hero H1 + lede.
3. Overall grade, H2, summary, and the 4 pillar grades (Website / Google Profile / Social /
   Listings).
4. Per pillar (Website, Google Business Profile, Social & Listings): the pillar H2, the
   grade-badge tone (critical/warn/pass), and each finding as {status, title, body,
   optional verbatim evidence}.
5. Exactly 5 quick wins, ranked, each as {title, body, impact tag}.

Present this as a clean, copy-pasteable block (plain text is fine — the user pastes each
piece into the matching form field). Mention explicitly if this prospect has no website, so
they check the "no tiene sitio web" box in the form (it auto-sets the Website grade to F and
suggests a starter finding — the user still reviews/edits it).

**No-website case:** still write real content for Pillar 01 rather than leaving it to the
form's auto-fill — reframe the finding(s) around the absence itself as the story (e.g. "No
website could be found for <business> — searches for '<business> <city>' surface only <what
you did find: GBP/social/directories>", "Every prospect who searches for you tonight lands
on a competitor instead").

## Step 5 — Point to the app

Tell the user to open `index.html` in their browser (or open it yourself in the Browser
pane via `preview_start` with the local file path) and paste the content from Step 4 into
the matching fields. Clicking **Generar reporte** renders the finished report instantly
inside the page; **Descargar HTML** saves the self-contained file, **Descargar PDF** sends
it to `server.py`'s `/render-pdf` endpoint (headless Chrome, no header/footer, already
paginated one section per page) and downloads the result — no browser print dialog
involved, so there's no "Headers and footers" setting to remember to uncheck.

Suggest they save the downloaded HTML/PDF into `reports/<Slug>-Snapshot/` — that naming
convention (a per-prospect folder ending in `-Snapshot`) is how the user identifies
prospect-project apps/assets across their GitHub folder.

Run the $10K Checklist + 4 conversion-standard review only if asked — this report is a
lead-magnet artifact, not a full site build, so most of those criteria don't apply as-is;
the equivalent bar here is: specific point of view (not generic audit boilerplate),
evidence-backed findings, and a single clear CTA.
