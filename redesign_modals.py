import re

with open('professional-dashboard.html', 'r', encoding='utf-8') as f:
    html = f.read()

# ── 1. MODAL BOX: glassomorphism panel ───────────────────────────────────────
html = re.sub(
    r'\.modal-box\s*\{[^}]*\}',
    '''.modal-box {
    background: rgba(14, 14, 18, 0.92);
    backdrop-filter: blur(28px);
    -webkit-backdrop-filter: blur(28px);
    border-radius: 1.5rem;
    padding: 2rem;
    width: 100%;
    max-width: 500px;
    max-height: 90vh;
    overflow-y: auto;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 24px 64px rgba(0,0,0,0.7), 0 0 0 1px rgba(0,219,233,0.06);
  }''',
    html
)

# ── 2. FORM INPUTS (.fi): dark rounded rectangles ────────────────────────────
html = re.sub(
    r'\.fi\s*\{[^}]*\}',
    '''.fi {
    width: 100%;
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 0.75rem !important;
    padding: 0.7rem 1rem;
    color: #dce4e5 !important;
    font-size: 0.82rem;
    outline: none;
    transition: border-color 0.2s, box-shadow 0.2s;
    font-family: 'Plus Jakarta Sans', sans-serif;
    color-scheme: dark;
    -webkit-text-fill-color: #dce4e5;
    box-shadow: none !important;
  }''',
    html
)

# Remove the neumorphic focus shadow and replace with glow
html = re.sub(
    r'\.fi:focus\s*\{[^}]*\}',
    '''.fi:focus {
    border-color: rgba(0,219,233,0.5) !important;
    box-shadow: 0 0 0 3px rgba(0,219,233,0.08) !important;
    background: rgba(0,219,233,0.03) !important;
  }''',
    html
)

# Placeholder faded
if '::placeholder' not in html or '.fi::placeholder' not in html:
    html = html.replace(
        '.fi:focus {',
        '''.fi::placeholder { color: rgba(185,202,203,0.3) !important; font-size: 0.82rem; }
  .fi:focus {'''
    )

# ── 3. BUTTON (.cc-btn-primary): sleek cybertruck glow ───────────────────────
html = re.sub(
    r'\.cc-btn-primary\s*\{[^}]*\}',
    '''.cc-btn-primary {
    background: linear-gradient(135deg, rgba(0,180,200,0.85), rgba(0,219,233,0.9)) !important;
    border: 1px solid rgba(0,219,233,0.4) !important;
    border-radius: 0.85rem !important;
    padding: 0.8rem 1.75rem;
    font-weight: 800;
    cursor: pointer;
    color: #001f22 !important;
    font-size: 0.9rem;
    font-family: inherit;
    width: 100%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.45rem;
    transition: all 0.2s ease;
    box-shadow: 0 4px 20px rgba(0,219,233,0.25) !important;
    letter-spacing: 0.02em;
  }''',
    html
)

html = re.sub(
    r'\.cc-btn-primary:hover\s*\{[^}]*\}',
    '''.cc-btn-primary:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(0,219,233,0.4) !important;
    background: linear-gradient(135deg, rgba(0,200,220,0.95), rgba(0,230,245,1)) !important;
  }''',
    html
)

html = re.sub(
    r'\.cc-btn-primary:active\s*\{[^}]*\}',
    '''.cc-btn-primary:active {
    transform: translateY(0) !important;
    box-shadow: 0 2px 10px rgba(0,219,233,0.2) !important;
  }''',
    html
)

# ── 4. MODAL CLOSE BUTTON: cleaner look ──────────────────────────────────────
html = re.sub(
    r'\.modal-close-btn\s*\{[^}]*\}',
    '''.modal-close-btn {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 0.6rem;
    width: 2rem;
    height: 2rem;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    color: #849495;
    transition: all 0.2s;
    flex-shrink: 0;
  }''',
    html
)

html = re.sub(
    r'\.modal-close-btn:hover\s*\{[^}]*\}',
    '.modal-close-btn:hover { color: #ff6b6b; border-color: rgba(255,107,107,0.3); background: rgba(255,107,107,0.08); }',
    html
)

# ── 5. MODAL LABEL: all uppercase small faded labels ─────────────────────────
# Add .modal-box label rule
if '.modal-box label' not in html:
    html = html.replace(
        '.modal-close-btn {',
        '''.modal-box label {
    font-size: 0.68rem !important;
    font-weight: 800 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: #6a8a8c !important;
    margin-bottom: 0.35rem;
    display: block;
  }
  .modal-close-btn {'''
    )

# ── 6. Fix light mode overrides for .fi to not apply ─────────────────────────
# Override html.light .fi to still look dark in modal context (all modals dark)
old_light_fi = re.search(r'html\.light \.fi\s*\{[^}]*\}', html)
if old_light_fi:
    html = html.replace(old_light_fi.group(), '')

with open('professional-dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Done! Modal styles updated.")
