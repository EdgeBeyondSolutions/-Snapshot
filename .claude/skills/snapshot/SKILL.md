---
name: snapshot
description: Generate a "Digital Presence Snapshot" lead-gen report (HTML, printable to PDF) for a prospect business, auditing their website (or lack of one), Google Business Profile, and social/directory listings. Use when the user asks to "genera el snapshot para <prospecto>", "haz un snapshot de <negocio>", or similar, from within the -Snapshot project.
---

# Digital Presence Snapshot generator

Produces the same report format built for Terra Klean Solutions: a cold, evidence-based
audit of a prospect's online presence, used as a free lead-magnet by EdgeBeyond Solutions
to book a 30-minute walkthrough call. One self-contained HTML file — the report itself has
no download/print button embedded; the `index.html` app's toolbar handles Download
HTML/PDF (the native print dialog — the report's CSS is already tuned for clean
pagination). Don't add a print button inside template.html/the generated report — that was
tried and caused a visible duplicate with the app's own toolbar button.

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

## Step 2 — Grade each pillar (A–F)

Grade honestly, the way a prospect's next customer would judge them:

- **Website:** A/B = modern, mobile-first, clear CTA, consistent trust signals. C = dated
  but functional. D = seriously dated, phone-only contact, or trust-claim problems. F = no
  working site, or one that actively misleads (broken trust claims, dead links).
  **No website at all is an automatic F** — reframe the whole pillar around that absence.
- **Google Business Profile:** A/B = claimed, actively managed, real reviews, photos. C =
  claimed but thin (few reviews/photos). D = claimed but neglected. F = unclaimed or
  nonexistent.
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
  Calendar booking page — `https://calendar.app.google/1GFwXDncbppQ1RHn6`, `target="_blank"
  rel="noopener"` — not a `mailto:` link. This is intentional: a real scheduling link is
  actual lead capture (name/email/time collected by Google), where a mailto is not. The
  same fixed URL is used for every prospect — nothing to customize per report.

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
inside the page; **Descargar HTML** saves the self-contained file, **Descargar PDF** opens
the browser's native print dialog (already paginated one section per page).

Suggest they save the downloaded HTML/PDF into `reports/<Slug>-Snapshot/` — that naming
convention (a per-prospect folder ending in `-Snapshot`) is how the user identifies
prospect-project apps/assets across their GitHub folder.

Run the $10K Checklist + 4 conversion-standard review only if asked — this report is a
lead-magnet artifact, not a full site build, so most of those criteria don't apply as-is;
the equivalent bar here is: specific point of view (not generic audit boilerplate),
evidence-backed findings, and a single clear CTA.
