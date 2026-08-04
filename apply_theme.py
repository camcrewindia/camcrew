import re

with open('professional-profile.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Remove html.light CSS blocks
html = re.sub(r'html\.light.*?\{[^}]*\}', '', html, flags=re.MULTILINE | re.DOTALL)
html = re.sub(r'html\.light.*?(?=\n)', '', html) # any single line html.light rules

# Replace neumorphic root variables with cybertruck ones if needed, or just remove the neumorphic ones
html = re.sub(r':root\s*\{[^}]*\}', ':root { --ac: #00dbe9; --ac2: #ebb2ff; }', html)

# Fix background
html = re.sub(r'body\s*\{[^}]*background:[^;]+;', 'body {\n      background: #0A0A0B;\n      background-image: radial-gradient(circle at top right, rgba(0,219,233,0.03), transparent 40%), radial-gradient(circle at bottom left, rgba(235,178,255,0.03), transparent 40%);\n      background-attachment: fixed;', html)

# Inject animated hero-grid into page-wrap
html = html.replace('<div class="page-wrap">', '<div class="fixed inset-0 z-[-1] pointer-events-none"><div class="hero-grid absolute inset-0 opacity-15"></div><div class="orb-1"></div><div class="orb-2"></div></div>\n    <div class="page-wrap relative z-10">')

# Profile Banner
html = re.sub(r'\.profile-banner\s*\{[^}]*\}', '.profile-banner { position: relative; height: 200px; background: rgba(0,0,0,0.3); backdrop-filter: blur(20px); border-bottom: 1px solid rgba(255,255,255,0.08); overflow: hidden; border-radius: 0 0 1.25rem 1.25rem; }', html)

# Avatar ring border
html = html.replace('border: 4px solid #0a0a0b;', 'border: 3px solid rgba(255,255,255,0.1); box-shadow: 0 0 20px rgba(0,219,233,0.3);')

# Stat cell glassmorphism
html = re.sub(r'\.stat-cell\s*\{[^}]*\}', '.stat-cell { padding: 1rem 1.25rem; border-radius: 1rem; background: rgba(22, 22, 24, 0.6); backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.08); text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: center; }', html)

# Service card glassmorphism
html = re.sub(r'\.service-card\s*\{[^}]*\}', '.service-card { background: rgba(22, 22, 24, 0.6); backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.08); border-radius: 1rem; padding: 1.5rem; display: flex; flex-direction: column; height: 100%; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); cursor: pointer; }', html)
html = re.sub(r'\.service-card:hover\s*\{[^}]*\}', '.service-card:hover { transform: translateY(-5px); border-color: rgba(0,219,233,0.4); background: rgba(30, 30, 34, 0.8); box-shadow: 0 8px 32px rgba(0,0,0,0.4); }', html)

# Portfolio cell glassmorphism
html = re.sub(r'\.portfolio-cell\s*\{[^}]*\}', '.portfolio-cell { background: rgba(255, 255, 255, 0.04); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 0.75rem; aspect-ratio: 1; overflow: hidden; position: relative; cursor: pointer; transition: transform 0.2s; }', html)
html = re.sub(r'\.portfolio-cell:hover\s*\{[^}]*\}', '.portfolio-cell:hover { transform: scale(0.97); }', html)

# Remove explicit text-color changes in buttons, etc to let them default properly
html = re.sub(r'color: #0a1618;', 'color: #dce4e5;', html)

with open('professional-profile.html', 'w', encoding='utf-8') as f:
    f.write(html)
