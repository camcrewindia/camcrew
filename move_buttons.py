import re

with open('professional-profile.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Remove .banner-actions block
html = re.sub(r'<div class="banner-actions">.*?</div>', '', html, flags=re.DOTALL)

# 2. Update .avatar-actions block to include Home and Dashboard buttons
new_avatar_actions = """<div class="avatar-actions">
              <a href="index.html" class="btn-ghost" style="font-size:0.78rem;padding:0.45rem 0.9rem;" title="Go to Home">
                <span class="material-symbols-outlined" style="font-size:0.88rem;">home</span>
                Home
              </a>
              <a href="professional-dashboard.html" class="btn-primary" style="padding:0.45rem 0.9rem;font-size:0.78rem;">
                <span class="material-symbols-outlined" style="font-size:0.88rem;">dashboard</span>
                Dashboard
              </a>
              <a href="professional-edit.html" class="btn-ghost" style="font-size:0.78rem;padding:0.45rem 0.9rem;">
                <span class="material-symbols-outlined" style="font-size:0.88rem;">edit</span>
                Edit Profile
              </a>
              <a href="professional-edit.html" class="btn-icon" title="Edit Profile">
                <span class="material-symbols-outlined">tune</span>
              </a>
            </div>"""

# Replace the existing avatar-actions block
html = re.sub(r'<div class="avatar-actions">.*?</div>\s*</div>', new_avatar_actions + '\n          </div>', html, flags=re.DOTALL)

with open('professional-profile.html', 'w', encoding='utf-8') as f:
    f.write(html)
