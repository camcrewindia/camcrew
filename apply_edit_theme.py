import re

with open('professional-edit.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Remove data-theme from html tag
html = re.sub(r'<html class="dark" lang="en" data-theme="dark">', '<html class="dark" lang="en">', html)

# Remove all [data-theme] CSS rules
html = re.sub(r'\[data-theme="light"\].*?(?=\n)', '', html)
html = re.sub(r'\[data-theme="light"\]\s*\{[^}]*\}', '', html)
html = re.sub(r'\[data-theme="dark"\].*?(?=\n)', '', html)

# Remove #theme-toggle HTML, CSS, script
html = re.sub(r'#theme-toggle\s*\{[^}]*\}', '', html)
html = re.sub(r'#theme-toggle:hover\s*\{[^}]*\}', '', html)
html = re.sub(r'#theme-toggle:active\s*\{[^}]*\}', '', html)
# Note: #theme-toggle isn't in HTML based on the paste? Wait, it wasn't in the pasted HTML for the button, just the JS and CSS.
html = re.sub(r'/\*\s*──\s*Tesla Cybertruck Theme Toggle[\s\S]*?</script>', '</script>', html)

# Change .cc-input for rounded rectangles
cc_input_repl = """.cc-input {
    width: 100%;
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 0.75rem !important;
    box-shadow: none !important;
    color: #dce4e5 !important;
    padding: 0.75rem 1rem;
    font-size: 1rem;
    font-family: 'Plus Jakarta Sans', sans-serif;
    outline: none;
    transition: all 0.2s ease;
    -webkit-appearance: none;
  }
  .cc-input:focus {
    border-color: #00dbe9 !important;
    background: rgba(0,219,233,0.02) !important;
    box-shadow: 0 0 0 2px rgba(0,219,233,0.1) !important;
    outline: none !important;
  }"""
html = re.sub(r'\.cc-input\s*\{[^}]*\}[^{]*\.cc-input:focus\s*\{[^}]*\}', cc_input_repl, html, flags=re.MULTILINE)

# Remove the padding-left inline styles from the inputs with icons
html = re.sub(r'style="padding-left:1\.75rem;"', 'style="padding-left: 2.25rem !important;"', html)
html = re.sub(r'style="padding-left:1rem;"', 'style="padding-left: 1.5rem !important;"', html)

# Change loc-input padding-left explicitly to fix the override
html = re.sub(r'padding:0\.85rem 1rem 0\.85rem 2\.75rem !important;', 'padding: 0.75rem 1rem 0.75rem 2.5rem !important;', html)

# Ensure icons inside input wrappers are positioned correctly for the new padding
html = re.sub(r'left:0;', 'left: 0.75rem;', html)
html = re.sub(r'left:1rem;', 'left: 0.75rem;', html)

# Set body background
html = re.sub(r'body class="([^"]*)"', r'body class="\1" style="background-color: #0A0A0B;"', html)

# Ambient background
bg_repl = """<div class="fixed inset-0 z-[-1] pointer-events-none overflow-hidden">
  <div class="hero-grid absolute inset-0 opacity-15"></div>
  <div class="orb-1"></div>
  <div class="orb-2"></div>
</div>"""
html = re.sub(r'<div class="fixed inset-0 z-\[-1\] overflow-hidden">.*?</div>\n</div>', bg_repl, html, flags=re.DOTALL)

# Glassmorphism on .edit-section
html = re.sub(r'\.edit-section\s*\{[^}]*\}', '.edit-section { background: rgba(22, 22, 24, 0.6); backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.08); border-radius: 1.5rem; padding: 2rem; }', html)

# Glassmorphism on #save-bar
html = re.sub(r'#save-bar\s*\{[^}]*\}', '#save-bar { position: fixed; bottom: 1.5rem; left: 50%; transform: translateX(-50%); z-index: 100; background: rgba(22, 22, 24, 0.85); backdrop-filter: blur(20px); border: 1px solid rgba(0,219,233,0.3); border-radius: 999px; padding: 0.65rem 0.65rem 0.65rem 1.4rem; display: flex; align-items: center; gap: 1rem; box-shadow: 0 8px 32px rgba(0,0,0,0.6), 0 0 0 1px rgba(0,219,233,0.1); transition: opacity 0.3s, transform 0.3s; white-space: nowrap; }', html)

with open('professional-edit.html', 'w', encoding='utf-8') as f:
    f.write(html)
