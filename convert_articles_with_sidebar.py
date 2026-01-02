#!/usr/bin/env python3
"""
Artikel-Konverter mit Sidebar-Navigation
Erstellt übersichtliche Artikel mit automatischem Inhaltsverzeichnis
"""

import os
import re
from pathlib import Path

# HTML-Template mit Sidebar-Navigation
ARTICLE_TEMPLATE = '''<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Orthopedic Knowledge Base</title>
    <link rel="stylesheet" href="styles.css">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
        }}

        /* Header */
        .header {{
            background: white;
            border-bottom: 2px solid #e0e0e0;
            padding: 1rem 2rem;
            position: sticky;
            top: 0;
            z-index: 1000;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }}

        .header-content {{
            max-width: 1400px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .logo {{
            font-size: 1.5rem;
            font-weight: bold;
            color: #2563eb;
            text-decoration: none;
        }}

        .nav-links {{
            display: flex;
            gap: 2rem;
        }}

        .nav-links a {{
            color: #666;
            text-decoration: none;
            font-weight: 500;
        }}

        .nav-links a:hover {{
            color: #2563eb;
        }}

        /* Breadcrumbs */
        .breadcrumbs {{
            background: white;
            padding: 0.75rem 2rem;
            border-bottom: 1px solid #e0e0e0;
            font-size: 0.9rem;
        }}

        .breadcrumbs-content {{
            max-width: 1400px;
            margin: 0 auto;
            color: #666;
        }}

        .breadcrumbs a {{
            color: #2563eb;
            text-decoration: none;
        }}

        .breadcrumbs a:hover {{
            text-decoration: underline;
        }}

        /* Main Layout */
        .main-container {{
            max-width: 1400px;
            margin: 2rem auto;
            padding: 0 2rem;
            display: grid;
            grid-template-columns: 280px 1fr;
            gap: 2rem;
        }}

        /* Sidebar Navigation */
        .sidebar {{
            position: sticky;
            top: 100px;
            height: fit-content;
            background: white;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 1.5rem;
        }}

        .sidebar h3 {{
            font-size: 0.9rem;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 1rem;
            font-weight: 600;
        }}

        .toc-list {{
            list-style: none;
        }}

        .toc-item {{
            margin-bottom: 0.5rem;
        }}

        .toc-link {{
            display: block;
            padding: 0.5rem;
            color: #333;
            text-decoration: none;
            border-radius: 4px;
            font-size: 0.9rem;
            transition: all 0.2s;
        }}

        .toc-link:hover {{
            background: #f0f9ff;
            color: #2563eb;
        }}

        .toc-link.active {{
            background: #e0f2fe;
            color: #2563eb;
            font-weight: 500;
        }}

        /* Article Content */
        .article {{
            background: white;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 2rem;
        }}

        .article h1 {{
            font-size: 2rem;
            color: #000;
            margin-bottom: 1.5rem;
            font-weight: 600;
        }}

        .article h2 {{
            font-size: 1.5rem;
            color: #000;
            margin-top: 2rem;
            margin-bottom: 0.75rem;
            font-weight: 600;
        }}

        .article h3 {{
            font-size: 1.2rem;
            color: #000;
            margin-top: 1.5rem;
            margin-bottom: 0.5rem;
            font-weight: 600;
        }}

        .article h4 {{
            font-size: 1rem;
            color: #000;
            margin-top: 1rem;
            margin-bottom: 0.5rem;
            font-weight: 600;
        }}

        .article p {{
            margin-bottom: 0.75rem;
            line-height: 1.6;
        }}

        .article ul,
        .article ol {{
            margin-bottom: 0.75rem;
            padding-left: 1.5rem;
        }}

        .article li {{
            margin-bottom: 0.25rem;
            line-height: 1.6;
        }}

        .article strong {{
            font-weight: 600;
        }}

        .article table {{
            width: 100%;
            border-collapse: collapse;
            margin: 1rem 0;
            border: 1px solid #ddd;
        }}

        .article th {{
            background: #f5f5f5;
            padding: 0.5rem;
            text-align: left;
            border: 1px solid #ddd;
            font-weight: 600;
        }}

        .article td {{
            padding: 0.5rem;
            border: 1px solid #ddd;
        }}

        /* Mobile */
        @media (max-width: 768px) {{
            .main-container {{
                grid-template-columns: 1fr;
            }}

            .sidebar {{
                position: static;
                margin-bottom: 1rem;
            }}

            .article {{
                padding: 1.5rem;
            }}

            .article h1 {{
                font-size: 2rem;
            }}

            .article h2 {{
                font-size: 1.5rem;
            }}
        }}

        /* Scroll behavior */
        html {{
            scroll-behavior: smooth;
        }}

        /* Section spacing */
        .article section {{
            scroll-margin-top: 100px;
        }}
    </style>
</head>
<body>
    <!-- Header -->
    <header class="header">
        <div class="header-content">
            <a href="index.html" class="logo">OrthopedicKB</a>
            <nav class="nav-links">
                <a href="index.html">Home</a>
                <a href="huefte.html">Hüfte</a>
            </nav>
        </div>
    </header>

    <!-- Breadcrumbs -->
    <div class="breadcrumbs">
        <div class="breadcrumbs-content">
            <a href="index.html">Home</a> › 
            <a href="huefte.html">Hüfte</a> › 
            <span>{breadcrumb}</span>
        </div>
    </div>

    <!-- Main Content -->
    <div class="main-container">
        <!-- Sidebar Navigation -->
        <aside class="sidebar">
            <h3>Inhaltsverzeichnis</h3>
            <ul class="toc-list">
{toc_items}
            </ul>
        </aside>

        <!-- Article -->
        <article class="article">
{content}
        </article>
    </div>

    <script>
        // Active TOC highlighting
        const sections = document.querySelectorAll('.article h2[id]');
        const tocLinks = document.querySelectorAll('.toc-link');

        window.addEventListener('scroll', () => {{
            let current = '';
            sections.forEach(section => {{
                const sectionTop = section.offsetTop;
                if (window.pageYOffset >= sectionTop - 150) {{
                    current = section.getAttribute('id');
                }}
            }});

            tocLinks.forEach(link => {{
                link.classList.remove('active');
                if (link.getAttribute('href') === '#' + current) {{
                    link.classList.add('active');
                }}
            }});
        }});
    </script>
</body>
</html>'''


def extract_title(html_content):
    """Extrahiert den Titel"""
    h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', html_content, re.IGNORECASE | re.DOTALL)
    if h1_match:
        title = re.sub(r'<[^>]+>', '', h1_match.group(1))
        return title.strip()
    
    title_match = re.search(r'<title[^>]*>(.*?)</title>', html_content, re.IGNORECASE)
    if title_match:
        title = title_match.group(1)
        title = re.sub(r'\s*-\s*Orthopedic Knowledge Base.*$', '', title)
        return title.strip()
    
    return "Artikel"


def extract_headings(content):
    """Extrahiert alle h2-Überschriften für das Inhaltsverzeichnis"""
    headings = []
    h2_pattern = re.compile(r'<h2[^>]*>(.*?)</h2>', re.IGNORECASE | re.DOTALL)
    
    for match in h2_pattern.finditer(content):
        heading_text = re.sub(r'<[^>]+>', '', match.group(1))
        heading_text = heading_text.strip()
        if heading_text:
            headings.append(heading_text)
    
    return headings


def create_slug(text):
    """Erstellt URL-freundliche IDs"""
    # Kleinbuchstaben
    slug = text.lower()
    # Umlaute ersetzen
    slug = slug.replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace('ß', 'ss')
    # Nur Buchstaben und Zahlen
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    # Doppelte Bindestriche entfernen
    slug = re.sub(r'-+', '-', slug)
    # Bindestriche am Anfang/Ende entfernen
    slug = slug.strip('-')
    return slug


def add_ids_to_headings(content, headings):
    """Fügt IDs zu h2-Tags hinzu"""
    def replace_h2(match):
        heading_text = re.sub(r'<[^>]+>', '', match.group(1)).strip()
        if heading_text in headings:
            slug = create_slug(heading_text)
            return f'<h2 id="{slug}">{match.group(1)}</h2>'
        return match.group(0)
    
    content = re.sub(r'<h2[^>]*>(.*?)</h2>', replace_h2, content, flags=re.IGNORECASE | re.DOTALL)
    return content


def create_toc(headings):
    """Erstellt HTML für Inhaltsverzeichnis"""
    if not headings:
        return '                <li class="toc-item">Kein Inhaltsverzeichnis verfügbar</li>'
    
    toc_items = []
    for heading in headings:
        slug = create_slug(heading)
        toc_items.append(f'                <li class="toc-item"><a href="#{slug}" class="toc-link">{heading}</a></li>')
    
    return '\n'.join(toc_items)


def extract_body_content(html_content):
    """Extrahiert Inhalt aus body"""
    body_match = re.search(r'<body[^>]*>(.*?)</body>', html_content, re.IGNORECASE | re.DOTALL)
    if body_match:
        content = body_match.group(1)
        
        # Entferne störende Elemente
        content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)
        content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL | re.IGNORECASE)
        content = re.sub(r'<nav[^>]*>.*?</nav>', '', content, flags=re.DOTALL | re.IGNORECASE)
        content = re.sub(r'<header[^>]*>.*?</header>', '', content, flags=re.DOTALL | re.IGNORECASE)
        content = re.sub(r'<footer[^>]*>.*?</footer>', '', content, flags=re.DOTALL | re.IGNORECASE)
        content = re.sub(r'<a[^>]*zurück[^>]*>.*?</a>', '', content, flags=re.IGNORECASE)
        
        return content.strip()
    
    return html_content


def convert_article(filepath):
    """Konvertiert einen Artikel"""
    print(f"📄 Konvertiere: {filepath.name}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Extrahiere Informationen
        title = extract_title(html_content)
        content = extract_body_content(html_content)
        
        # Extrahiere Überschriften
        headings = extract_headings(content)
        print(f"   📋 Gefunden: {len(headings)} Abschnitte")
        
        # Füge IDs zu Überschriften hinzu
        content = add_ids_to_headings(content, headings)
        
        # Erstelle TOC
        toc_html = create_toc(headings)
        
        breadcrumb = title[:47] + "..." if len(title) > 50 else title
        
        # Erstelle neues HTML
        new_html = ARTICLE_TEMPLATE.format(
            title=title,
            breadcrumb=breadcrumb,
            toc_items=toc_html,
            content=content
        )
        
        # Backup
        backup_path = filepath.with_suffix('.html.backup')
        if not backup_path.exists():
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"   💾 Backup erstellt")
        
        # Schreibe neue Datei
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_html)
        
        print(f"   ✅ Erfolgreich konvertiert")
        return True
        
    except Exception as e:
        print(f"   ❌ Fehler: {e}")
        return False


def main():
    """Hauptfunktion"""
    print("=" * 70)
    print("🔄 Artikel-Konverter mit Sidebar-Navigation")
    print("=" * 70)
    print()
    
    current_dir = Path.cwd()
    print(f"📂 Arbeitsverzeichnis: {current_dir}")
    print()
    
    # Finde Artikel
    exclude_files = {'index.html', 'huefte.html', 'hufte.html'}
    html_files = [
        f for f in current_dir.glob('*.html') 
        if f.name.lower() not in exclude_files 
        and not f.name.endswith('.backup')
    ]
    
    # Finde Backups
    backup_files = list(current_dir.glob('*.html.backup'))
    
    if not html_files:
        print("❌ Keine Artikel gefunden!")
        return
    
    print(f"📋 Gefundene Artikel: {len(html_files)}")
    if backup_files:
        print(f"💾 Gefundene Backups: {len(backup_files)}")
    print()
    
    # Backup-Lösch-Option
    if backup_files:
        print("🗑️  Möchten Sie alle Backups löschen?")
        delete_response = input("   (j/n): ")
        if delete_response.lower() in ['j', 'ja', 'y', 'yes']:
            for backup in backup_files:
                backup.unlink()
                print(f"   ✅ Gelöscht: {backup.name}")
            print(f"   🗑️  {len(backup_files)} Backups gelöscht")
        print()
    
    print("⚠️  WICHTIG:")
    print("   • Neue Backups werden erstellt (.html.backup)")
    print("   • Alle Artikel bekommen Sidebar-Navigation")
    print("   • Minimales, übersichtliches Design")
    print("   • 'Zurück zur Übersicht' wird entfernt")
    print()
    
    response = input("Möchten Sie die Artikel konvertieren? (j/n): ")
    if response.lower() not in ['j', 'ja', 'y', 'yes']:
        print("❌ Abgebrochen.")
        return
    
    print()
    print("=" * 70)
    print("🔄 Starte Konvertierung...")
    print("=" * 70)
    print()
    
    success_count = 0
    for filepath in html_files:
        if convert_article(filepath):
            success_count += 1
        print()
    
    print("=" * 70)
    print(f"✅ Erfolgreich konvertiert: {success_count}/{len(html_files)}")
    print(f"💾 Backups gespeichert (.html.backup)")
    print()
    print("🎉 Fertig! Öffnen Sie die Artikel im Browser.")
    print("=" * 70)


if __name__ == "__main__":
    main()
