import re

with open('professional-dashboard.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix the checkbox container in Add Equipment modal (still uses neumorphic var)
html = html.replace(
    'style="display:flex;align-items:center;gap:0.75rem;padding:0.65rem 0.85rem;background:var(--nb);border-radius:0.6rem;box-shadow:var(--ni-s);"',
    'style="display:flex;align-items:center;gap:0.75rem;padding:0.65rem 0.85rem;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.1);border-radius:0.75rem;"'
)

# Fix fi-label to match the small faded uppercase style
html = re.sub(
    r'\.fi-label\s*\{[^}]*\}',
    '''.fi-label {
    display: block;
    font-size: 0.68rem;
    font-weight: 800;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #6a8a8c;
    margin-bottom: 0.35rem;
    font-family: 'Plus Jakarta Sans', sans-serif;
  }''',
    html
)

# Ensure selects (dropdowns) have a dark background
html = re.sub(
    r'select\.fi,\s*select\s*\{[^}]*\}',
    '',
    html
)
# Add select-specific dark override
if 'select.fi {' not in html:
    html = html.replace(
        '.fi::placeholder',
        '''select.fi {
    background: rgba(14,14,18,0.9) !important;
    color: #dce4e5 !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 0.75rem !important;
    -webkit-text-fill-color: #dce4e5 !important;
  }
  select.fi option {
    background: #161618;
    color: #dce4e5;
  }
  .fi::placeholder'''
    )

with open('professional-dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Fixes applied!")
