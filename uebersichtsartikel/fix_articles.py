#!/usr/bin/env python3
"""
Artikel-Konverter - FIXED VERSION
Erstellt garantiert funktionierende, saubere Artikel mit Sidebar
"""

import os
import re
from pathlib import Path

# Funktionierendes HTML-Template
ARTICLE_TEMPLATE = '''<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Orthopedic Knowledge Base</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f8f9fa;
        }}

        /* Header */
        .header {{
            background: white;
            border-bottom: 1px solid #dee2e6;
            padding: 1rem 0;
            position: sticky;
            top: 0;
            z-index: 1000;
            box-shadow: 0 2px 4px rgba(0,0,0,0.04);
        }}

        .header-inner {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .logo {{
            font-size: 1.25rem;
            font-weight: 700;
            color: #2563eb;
            text-decoration: none;
        }}

        .nav {{
            display: flex;
            gap: 1.5rem;
        }}

        .nav a {{
            color: #6c757d;
            text-decoration: none;
            font-weight: 500;
            font-size: 0.95rem;
        }}

        .nav a:hover {{
            color: #2563eb;
        }}

        /* Breadcrumbs */
        .breadcrumbs {{
            background: white;
            border-bottom: 1px solid #dee2e6;
            padding: 0.75rem 0;
        }}

        .breadcrumbs-inner {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 2rem;
            font-size: 0.875rem;
            color: #6c757d;
        }}

        .breadcrumbs a {{
            color: #2563eb;
            text-decoration: none;
        }}

        /* Main Container */
        .container {{
            max-width: 1400px;
            margin: 2rem auto;
            padding: 0 2rem;
            display: flex;
            gap: 2rem;
            align-items: flex-start;
        }}

        /* Sidebar */
        .sidebar {{
            width: 250px;
            flex-shrink: 0;
            position: sticky;
            top: 80px;
        }}

        .sidebar-inner {{
            background: white;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            padding: 1.5rem;
        }}

        .sidebar h3 {{
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: #6c757d;
            margin-bottom: 1rem;
            font-weight: 600;
        }}

        .toc {{
            list-style: none;
        }}

        .toc li {{
            margin-bottom: 0.5rem;
        }}

        .toc a {{
            display: block;
            padding: 0.4rem 0.6rem;
            color: #495057;
            text-decoration: none;
            border-radius: 4px;
            font-size: 0.875rem;
            transition: all 0.15s;
        }}

        .toc a:hover {{
            background: #f8f9fa;
            color: #2563eb;
        }}

        .toc a.active {{
            background: #e7f3ff;
            color: #2563eb;
            font-weight: 500;
        }}

        /* Content */
        .content {{
            flex: 1;
            min-width: 0;
            background: white;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            padding: 2.5rem;
        }}

        /* Typography */
        .content h1 {{
            font-size: 2rem;
            font-weight: 700;
            color: #212529;
            margin-bottom: 1.5rem;
            line-height: 1.2;
        }}

        .content h2 {{
            font-size: 1.5rem;
            font-weight: 600;
            color: #212529;
            margin-top: 2.5rem;
            margin-bottom: 1rem;
            padding-top: 1.5rem;
            border-top: 1px solid #dee2e6;
        }}

        .content h2:first-of-type {{
            margin-top: 0;
            padding-top: 0;
            border-top: none;
        }}

        .content h3 {{
            font-size: 1.25rem;
            font-weight: 600;
            color: #212529;
            margin-top: 1.5rem;
            margin-bottom: 0.75rem;
        }}

        .content h4 {{
            font-size: 1.1rem;
            font-weight: 600;
            color: #495057;
            margin-top: 1.25rem;
            margin-bottom: 0.5rem;
        }}

        .content p {{
            margin-bottom: 1rem;
            color: #495057;
        }}

        .content ul,
        .content ol {{
            margin-bottom: 1rem;
            padding-left: 1.5rem;
        }}

        .content li {{
            margin-bottom: 0.4rem;
            color: #495057;
        }}

        .content strong {{
            font-weight: 600;
            color: #212529;
        }}

        .content em {{
            font-style: italic;
        }}

        /* Tables */
        .content table {{
            width: 100%;
            border-collapse: collapse;
            margin: 1.5rem 0;
            font-size: 0.9rem;
        }}

        .content th {{
            background: #f8f9fa;
            padding: 0.75rem;
            text-align: left;
            font-weight: 600;
            border: 1px solid #dee2e6;
        }}

        .content td {{
            padding: 0.75rem;
            border: 1px solid #dee2e6;
        }}

        .content tbody tr:hover {{
            background: #f8f9fa;
        }}

        /* Images */
        .content img {{
            max-width: 100%;
            height: auto;
            border-radius: 4px;
            margin: 1.5rem 0;
        }}

        /* Responsive */
        @media (max-width: 992px) {{
            .container {{
                flex-direction: column;
            }}

            .sidebar {{
                width: 100%;
                position: static;
            }}

            .content {{
                padding: 1.5rem;
            }}
        }}

        /* Smooth scroll */
        html {{
            scroll-behavior: smooth;
        }}

        .content h2[id] {{
            scroll-margin-top: 100px;
        }}
    </style>
</head>
<body>
    <!-- Header -->
    <header class="header">
        <div class="header-inner">
            <a href="index.html" class="logo">OrthopedicKB</a>
            <nav class="nav">
                <a href="index.html">Home</a>
                <a href="huefte.html">Hüfte</a>
            </nav>
        </div>
    </header>

    <!-- Breadcrumbs -->
    <div class="breadcrumbs">
        <div class="breadcrumbs-inner">
            <a href="index.html">Home</a> › 
            <a href="huefte.html">Hüfte</a> › 
            {breadcrumb}
        </div>
    </div>

    <!-- Main -->
    <div class="container">
        <!-- Sidebar -->
        <aside class="sidebar">
            <div class="sidebar-inner">
                <h3>Inhaltsverzeichnis</h3>
                <ul class="toc">
{toc}
                </ul>
            </div>
        </aside>

        <!-- Content -->
        <main class="content">
{content}
        </main>
    </div>

    <script>
    // Active TOC
    const links = document.querySelectorAll('.toc a');
    const sections = document.querySelectorAll('.content h2[id]');
    
    window.addEventListener('scroll', () => {{
        let current = '';
        sections.forEach(section => {{
            const top = section.offsetTop;
            if (window.pageYOffset >= top - 120) {{
                current = section.id;
            }}
        }});
        
        links.forEach(link => {{
            link.classList.remove('active');
            if (link.getAttribute('href') === '#' + current) {{
                link.classList.add('active');
            }}
        }});
    }});
    </script>
</body>
</html>'''


def clean_html(text):
    """Bereinigt HTML von kaputten Strukturen"""
    # Entferne mehrfache Leerzeichen
    text = re.sub(r'\s+', ' ', text)
    # Entferne leere Tags
    text = re.sub(r'<(\w+)[^>]*>\s*</\1>', '', text)
    return text.strip()


def extract_title(html):
    """Extrahiert Titel"""
    match = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.I | re.S)
    if match:
        return clean_html(re.sub(r'<[^>]+>', '', match.group(1)))
    
    match = re.search(r'<title[^>]*>(.*?)</title>', html, re.I)
    if match:
        title = match.group(1)
        title = re.sub(r'\s*-\s*Orthopedic.*', '', title)
        return clean_html(title)
    
    return "Artikel"


def extract_h2_headings(html):
    """Extrahiert alle H2-Überschriften"""
    headings = []
    for match in re.finditer(r'<h2[^>]*>(.*?)</h2>', html, re.I | re.S):
        text = clean_html(re.sub(r'<[^>]+>', '', match.group(1)))
        if text and len(text) > 0:
            headings.append(text)
    return headings


def make_slug(text):
    """Macht URL-freundliche ID"""
    text = text.lower()
    text = text.replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace('ß', 'ss')
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = re.sub(r'-+', '-', text).strip('-')
    return text[:50]  # Max 50 Zeichen


def add_ids_to_h2(html, headings):
    """Fügt IDs zu H2-Tags hinzu"""
    def replacer(match):
        text = clean_html(re.sub(r'<[^>]+>', '', match.group(1)))
        if text in headings:
            slug = make_slug(text)
            return f'<h2 id="{slug}">{match.group(1)}</h2>'
        return match.group(0)
    
    return re.sub(r'<h2[^>]*>(.*?)</h2>', replacer, html, flags=re.I | re.S)


def make_toc(headings):
    """Erstellt TOC HTML"""
    if not headings:
        return '                    <li>Keine Abschnitte</li>'
    
    items = []
    for h in headings:
        slug = make_slug(h)
        # Kürze sehr lange Titel
        display = h if len(h) < 40 else h[:37] + '...'
        items.append(f'                    <li><a href="#{slug}">{display}</a></li>')
    
    return '\n'.join(items)


def extract_body(html):
    """Extrahiert Body-Content"""
    match = re.search(r'<body[^>]*>(.*?)</body>', html, re.I | re.S)
    if match:
        content = match.group(1)
        # Entferne Scripts, Styles, Nav, Header, Footer
        content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.I | re.S)
        content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.I | re.S)
        content = re.sub(r'<nav[^>]*>.*?</nav>', '', content, flags=re.I | re.S)
        content = re.sub(r'<header[^>]*>.*?</header>', '', content, flags=re.I | re.S)
        content = re.sub(r'<footer[^>]*>.*?</footer>', '', content, flags=re.I | re.S)
        return content.strip()
    
    return html


def convert(filepath):
    """Konvertiert eine Datei"""
    print(f"📄 {filepath.name}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()
        
        title = extract_title(html)
        content = extract_body(html)
        headings = extract_h2_headings(content)
        
        print(f"   📋 {len(headings)} Abschnitte")
        
        content = add_ids_to_h2(content, headings)
        toc = make_toc(headings)
        
        breadcrumb = title if len(title) < 50 else title[:47] + '...'
        
        new_html = ARTICLE_TEMPLATE.format(
            title=title,
            breadcrumb=breadcrumb,
            toc=toc,
            content=content
        )
        
        # Backup
        backup = filepath.with_suffix('.html.backup')
        if not backup.exists():
            with open(backup, 'w', encoding='utf-8') as f:
                f.write(html)
        
        # Schreibe
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_html)
        
        print(f"   ✅ Fertig")
        return True
        
    except Exception as e:
        print(f"   ❌ Fehler: {e}")
        return False


def main():
    print("=" * 70)
    print("🔧 ARTIKEL-REPARATUR (Fixed Version)")
    print("=" * 70)
    print()
    
    cwd = Path.cwd()
    print(f"📂 {cwd}")
    print()
    
    # Finde Artikel
    exclude = {'index.html', 'huefte.html', 'hufte.html'}
    files = [f for f in cwd.glob('*.html') 
             if f.name.lower() not in exclude and not f.name.endswith('.backup')]
    
    if not files:
        print("❌ Keine Artikel gefunden!")
        return
    
    print(f"📋 {len(files)} Artikel gefunden")
    print()
    
    # Backups löschen?
    backups = list(cwd.glob('*.html.backup'))
    if backups:
        print(f"💾 {len(backups)} Backups gefunden")
        resp = input("Backups löschen? (j/n): ")
        if resp.lower() in ['j', 'ja', 'y']:
            for b in backups:
                b.unlink()
            print(f"🗑️  {len(backups)} Backups gelöscht")
        print()
    
    resp = input("Artikel reparieren? (j/n): ")
    if resp.lower() not in ['j', 'ja', 'y']:
        print("Abgebrochen.")
        return
    
    print()
    print("🔄 Repariere...")
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
