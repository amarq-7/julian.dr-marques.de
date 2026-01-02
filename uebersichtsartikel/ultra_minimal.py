#!/usr/bin/env python3
"""
Ultra-minimales Artikel-Design
- Entfernt "Zurück zur Übersicht"
- Minimalstes Design
- Garantiert nichts zerschossen
"""

import re
from pathlib import Path

# Ultra-minimales HTML-Template
MINIMAL_TEMPLATE = '''<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            line-height: 1.5;
            color: #000;
            background: #fff;
            padding: 20px;
            max-width: 1200px;
            margin: 0 auto;
        }}

        .container {{
            display: flex;
            gap: 30px;
        }}

        /* Navigation Sidebar */
        .nav {{
            width: 250px;
            flex-shrink: 0;
            padding: 15px;
            background: #f8f8f8;
            border: 1px solid #ddd;
            border-radius: 8px;
            position: sticky;
            top: 20px;
            height: fit-content;
        }}

        .nav h3 {{
            font-size: 12px;
            text-transform: uppercase;
            color: #666;
            margin-bottom: 10px;
        }}

        .nav ul {{
            list-style: none;
        }}

        .nav li {{
            margin-bottom: 5px;
        }}

        .nav a {{
            font-size: 13px;
            color: #000;
            text-decoration: none;
            display: block;
            padding: 5px;
            border-radius: 4px;
        }}

        .nav a:hover {{
            background: #e8e8e8;
            color: #0066cc;
        }}

        /* Content */
        .content {{
            flex: 1;
            min-width: 0;
        }}

        .breadcrumbs {{
            font-size: 13px;
            color: #666;
            margin-bottom: 15px;
        }}

        .breadcrumbs a {{
            color: #0066cc;
            text-decoration: none;
        }}

        .back-link {{
            display: inline-block;
            color: #0066cc;
            text-decoration: none;
            margin-bottom: 20px;
            font-size: 14px;
        }}

        .back-link:hover {{
            text-decoration: underline;
        }}

        h1 {{
            font-size: 28px;
            margin-bottom: 20px;
            font-weight: 600;
        }}

        h2 {{
            font-size: 22px;
            margin-top: 30px;
            margin-bottom: 10px;
            font-weight: 600;
        }}

        h3 {{
            font-size: 18px;
            margin-top: 20px;
            margin-bottom: 8px;
            font-weight: 600;
        }}

        h4 {{
            font-size: 16px;
            margin-top: 15px;
            margin-bottom: 5px;
            font-weight: 600;
        }}

        p {{
            margin-bottom: 10px;
        }}

        ul, ol {{
            margin-bottom: 10px;
            padding-left: 25px;
        }}

        li {{
            margin-bottom: 3px;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }}

        th, td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }}

        th {{
            background: #f0f0f0;
            font-weight: 600;
        }}

        strong {{
            font-weight: 600;
        }}

        /* Mobile */
        @media (max-width: 768px) {{
            .container {{
                flex-direction: column;
            }}

            .nav {{
                width: 100%;
                position: static;
            }}
        }}

        /* Smooth scroll */
        html {{
            scroll-behavior: smooth;
        }}

        h2[id] {{
            scroll-margin-top: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Navigation Sidebar -->
        <nav class="nav">
            <h3>Navigation</h3>
            <ul>
{nav}
            </ul>
        </nav>

        <!-- Content -->
        <div class="content">
{content}
        </div>
    </div>
</body>
</html>'''


def extract_title(html):
    """Extrahiert Titel"""
    match = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.I | re.S)
    if match:
        return re.sub(r'<[^>]+>', '', match.group(1)).strip()
    
    match = re.search(r'<title[^>]*>(.*?)</title>', html, re.I)
    if match:
        return re.sub(r'\s*-\s*.*', '', match.group(1)).strip()
    
    return "Artikel"


def extract_h2(html):
    """Extrahiert H2-Überschriften"""
    headings = []
    for match in re.finditer(r'<h2[^>]*>(.*?)</h2>', html, re.I | re.S):
        text = re.sub(r'<[^>]+>', '', match.group(1)).strip()
        if text:
            headings.append(text)
    return headings


def make_id(text):
    """Macht ID"""
    text = text.lower()
    text = text.replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace('ß', 'ss')
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return re.sub(r'-+', '-', text).strip('-')[:40]


def add_ids(html, headings):
    """Fügt IDs zu H2 hinzu"""
    def replace(match):
        text = re.sub(r'<[^>]+>', '', match.group(1)).strip()
        if text in headings:
            return f'<h2 id="{make_id(text)}">{match.group(1)}</h2>'
        return match.group(0)
    
    return re.sub(r'<h2[^>]*>(.*?)</h2>', replace, html, flags=re.I | re.S)


def make_nav(headings):
    """Erstellt Navigation"""
    if not headings:
        return '            <li>Keine Abschnitte</li>'
    
    items = []
    for h in headings[:10]:  # Max 10
        display = h if len(h) < 35 else h[:32] + '...'
        items.append(f'            <li><a href="#{make_id(h)}">{display}</a></li>')
    
    return '\n'.join(items)


def extract_content(html):
    """Extrahiert Body - Breadcrumbs und Zurück-Links bleiben drin!"""
    match = re.search(r'<body[^>]*>(.*?)</body>', html, re.I | re.S)
    if not match:
        return html
    
    content = match.group(1)
    
    # Entferne nur störende Elemente
    content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.I | re.S)
    content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.I | re.S)
    content = re.sub(r'<nav[^>]*class=["\']nav["\'][^>]*>.*?</nav>', '', content, flags=re.I | re.S)
    content = re.sub(r'<header[^>]*>.*?</header>', '', content, flags=re.I | re.S)
    content = re.sub(r'<footer[^>]*>.*?</footer>', '', content, flags=re.I | re.S)
    content = re.sub(r'<aside[^>]*>.*?</aside>', '', content, flags=re.I | re.S)
    
    # WICHTIG: Breadcrumbs und "Zurück"-Links bleiben erhalten!
    
    return content.strip()


def convert(filepath):
    """Konvertiert Artikel"""
    print(f"📄 {filepath.name}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()
        
        title = extract_title(html)
        content = extract_content(html)
        headings = extract_h2(content)
        
        print(f"   📋 {len(headings)} Abschnitte")
        
        content = add_ids(content, headings)
        nav = make_nav(headings)
        breadcrumb = title if len(title) < 40 else title[:37] + '...'
        
        new_html = MINIMAL_TEMPLATE.format(
            title=title,
            breadcrumb=breadcrumb,
            nav=nav,
            content=content
        )
        
        # Backup
        backup = filepath.with_suffix('.html.backup')
        with open(backup, 'w', encoding='utf-8') as f:
            f.write(html)
        
        # Schreibe
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_html)
        
        print(f"   ✅ Konvertiert")
        return True
        
    except Exception as e:
        print(f"   ❌ Fehler: {e}")
        return False


def main():
    print("=" * 70)
    print("🎨 ULTRA-MINIMAL DESIGN")
    print("=" * 70)
    print()
    print("• Entfernt 'Zurück zur Übersicht'")
    print("• Kleinstmögliches Design")
    print("• Garantiert nichts zerschossen")
    print()
    
    cwd = Path.cwd()
    
    # Backups löschen
    backups = list(cwd.glob('*.backup')) + list(cwd.glob('*.backup2'))
    if backups:
        print(f"🗑️  {len(backups)} Backups gefunden")
        resp = input("Backups löschen? (j/n): ")
        if resp.lower() in ['j', 'ja', 'y']:
            for b in backups:
                b.unlink()
            print(f"✅ {len(backups)} Backups gelöscht")
        print()
    
    # Finde Artikel
    exclude = {'index.html', 'huefte.html', 'hufte.html'}
    files = [f for f in cwd.glob('*.html') 
             if f.name.lower() not in exclude 
             and not f.name.endswith('.backup')]
    
    if not files:
        print("❌ Keine Artikel")
        return
    
    print(f"📋 {len(files)} Artikel")
    print()
    
    resp = input("Konvertieren? (j/n): ")
    if resp.lower() not in ['j', 'ja', 'y']:
        print("Abgebrochen")
        return
    
    print()
    
    ok = 0
    for f in files:
        if convert(f):
            ok += 1
    
    print()
    print("=" * 70)
    print(f"✅ {ok}/{len(files)} erfolgreich")
    print("🎉 Fertig!")
    print("=" * 70)


if __name__ == "__main__":
    main()
