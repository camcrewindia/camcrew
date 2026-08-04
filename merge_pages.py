import re

def merge():
    with open('professional-profile-merged.html', 'r', encoding='utf-8') as f:
        prof = f.read()

    with open('professional-dashboard.html', 'r', encoding='utf-8') as f:
        dash = f.read()

    # 1. Extract styles from dashboard
    dash_styles_match = re.search(r'<style>(.*?)</style>', dash, re.DOTALL)
    if dash_styles_match:
        dash_styles = dash_styles_match.group(1)
        # Remove :root definitions and html.light body to avoid clashing with profile
        dash_styles = re.sub(r':root,\s*\[data-theme="dark"\]\s*\{[^}]*\}', '', dash_styles)
        dash_styles = re.sub(r':root\s*\{[^}]*\}', '', dash_styles)
        dash_styles = re.sub(r'html\.light body\s*\{[^}]*\}', '', dash_styles)
        
        prof = prof.replace('</style>', f'/* DASHBOARD STYLES */\n{dash_styles}\n</style>')

    # 2. Extract #dashboard from dash
    dashboard_match = re.search(r'<div id="dashboard".*?</div><!-- /dashboard -->', dash, re.DOTALL)
    if dashboard_match:
        dashboard_html = dashboard_match.group(0)
        
        # Add a "View Profile" tab to the dashboard sidebar
        tab_html = '<div class="nav-item" data-section="profile-view" onclick="toggleProfileView()"><span class="material-symbols-outlined">visibility</span>Public Profile</div>\n'
        dashboard_html = dashboard_html.replace('data-section="account"', 'data-section="account" onclick="showSection(\'account\')"><span class="material-symbols-outlined">manage_accounts</span>Account</div>\n      ' + tab_html, 1)

        prof = prof.replace('</main>', f'</main>\n\n  <!-- DASHBOARD WRAPPER -->\n  {dashboard_html}')
    
    # 3. Extract modals from dash
    modals_match = re.search(r'<!--.*?MODALS.*?-->(.*?)<script>', dash, re.DOTALL)
    if modals_match:
        modals_html = modals_match.group(1)
        prof = prof.replace('<div id="pp-toast"></div>', f'<div id="pp-toast"></div>\n\n  <!-- DASHBOARD MODALS -->\n  {modals_html}')

    # 4. Extract JS from dash
    dash_js_match = re.search(r'<script>(.*?)</script>', dash, re.DOTALL)
    if dash_js_match:
        dash_js = dash_js_match.group(1)
        
        funcs_match = re.search(r'function showSection\((.*?)$', dash_js, re.DOTALL)
        if funcs_match:
            dash_funcs = 'function showSection(' + funcs_match.group(1)
        else:
            dash_funcs = dash_js
            
        toggle_logic = '''
  function toggleProfileView() {
    document.getElementById("dashboard").style.display = "none";
    document.getElementById("profile-root").style.display = "block";
    document.getElementById("header-placeholder").style.display = "block";
    document.getElementById("footer-placeholder").style.display = "block";
  }
  function toggleDashboardView() {
    document.getElementById("profile-root").style.display = "none";
    document.getElementById("header-placeholder").style.display = "none";
    document.getElementById("footer-placeholder").style.display = "none";
    document.getElementById("dashboard").style.display = "flex";
    
    // Default section to load
    showSection('overview');
  }
'''
        prof = prof.replace('</script>\n</body>', f'/* DASHBOARD JS */\n{dash_funcs}\n{toggle_logic}\n</script>\n</body>')
    
    with open('professional-profile-merged.html', 'w', encoding='utf-8') as f:
        f.write(prof)

if __name__ == '__main__':
    merge()
    print("Merge completed.")
