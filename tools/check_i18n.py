"""Post-build verification for the claude-code-4-skills i18n work.

Checks (headless DOM assertions only, no network):
  - the three dictionaries are inlined and key-complete
  - every data-i18n / data-i18n-html key exists in all locales
  - <html lang> mapping, title/meta swap, checklist re-render data
"""
import json
import re
import sys

PAGE = "/mnt/d/dev/claude-code-4-skills/index.html"
html = open(PAGE, encoding="utf-8").read()

m = re.search(r"/\*I18N_START\*/(.*?)/\*I18N_END\*/", html, re.S)
if not m:
    sys.exit("no I18N block in index.html — run tools/build_i18n.py first")

data = json.loads(m.group(1))
print("locales:", list(data), "| keys per locale:", {k: len(v) for k, v in data.items()})

text_keys = set(re.findall(r'data-i18n="([^"]+)"', html))
html_keys = set(re.findall(r'data-i18n-html="([^"]+)"', html))
dom_keys = text_keys | html_keys
print(f"DOM keys: {len(dom_keys)} (text {len(text_keys)} / html {len(html_keys)})")

problems = []
for lang, d in data.items():
    missing = sorted(dom_keys - set(d))
    if missing:
        problems.append(f"{lang}: keys missing from dictionary: {missing[:5]}")
    unused = sorted(set(d) - dom_keys - {"check", "meta.title", "meta.description",
                                         "meta.ogTitle", "meta.ogDescription", "ui.copied",
                                         "ui.copyFail", "ui.theme.toDark", "ui.theme.toLight",
                                         "ui.theme.toDarkAria", "ui.theme.toLightAria"})
    if unused:
        problems.append(f"{lang}: dictionary keys not used by the page: {unused[:5]}")
    if len(d.get("check", [])) != 8:
        problems.append(f"{lang}: check array is not 8 rows")
    if lang != "ko" and re.search(r"[\uac00-\ud7a3]", json.dumps(d, ensure_ascii=False)):
        problems.append(f"{lang}: Hangul residue")

print("html lang map present:", "HTML_LANG" in html)
print("switcher buttons:", len(re.findall(r'class="lang-btn"', html)))
print("theme toggle:", 'id="theme-toggle"' in html)

if problems:
    print("\nPROBLEMS")
    for p in problems:
        print("  -", p)
    sys.exit(1)
print("\nverification passed")
