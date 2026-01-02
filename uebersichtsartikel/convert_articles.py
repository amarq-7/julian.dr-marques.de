#!/usr/bin/env python3
"""
Artikel-Konverter für Orthopedic Knowledge Base
Konvertiert alle Artikel in das neue einheitliche Format
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup

# HTML-Template für Artikel
ARTICLE_TEMPLATE = '''<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Orthopedic Knowledge Base</title>
    <link rel="stylesheet" href="styles.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        .article-page {{
            min-height: 100vh;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        }}

        .article-header {{
            background: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            position: sticky;
            top: 0;
            z-index: 100;
        }}

        .article-nav {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 1rem 2rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}

        .logo {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
            text-decoration: none;
        }}

        .logo-icon {{
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, #3b82f6, #14b8a6);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .logo-icon svg {{
            width: 24px;
            height: 24px;
            color: white;
        }}

        .logo-text {{
            font-size: 1.5rem;
            font-weight: 800;
            color: #1f2937;
        }}

        .logo-text .highlight {{
            color: #3b82f6;
        }}

        .main-nav {{
            display: flex;
            gap: 2rem;
        }}

        .nav-link {{
            color: #6b7280;
            text-decoration: none;
            font-weight: 500;
            transition: color 0.2s;
        }}

        .nav-link:hover,
        .nav-link.active {{
            color: #3b82f6;
        }}

        .breadcrumbs {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 1.5rem 2rem 0.5rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.875rem;
            color: #6b7280;
        }}

        .breadcrumbs a {{
            color: #3b82f6;
            text-decoration: none;
        }}

        .breadcrumbs a:hover {{
            color: #2563eb;
        }}

        .breadcrumb-separator {{
            color: #d1d5db;
        }}

        .article-container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }}

        .article-content {{
            background: white;
            border-radius: 1rem;
            padding: 3rem;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        }}

        .back-link {{
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.75rem 1.5rem;
            background: linear-gradient(135deg, #eff6ff, #dbeafe);
            color: #2563eb;
            text-decoration: none;
            font-weight: 600;
            border-radius: 0.5rem;
            margin-bottom: 2rem;
            transition: all 0.2s;
        }}

        .back-link:hover {{
            background: linear-gradient(135deg, #dbeafe, #bfdbfe);
            transform: translateX(-4px);
        }}

        .article-content h1 {{
            font-size: 2.5rem;
            font-weight: 800;
            color: #1f2937;
            margin-bottom: 1.5rem;
            background: linear-gradient(135deg, #1f2937, #3b82f6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .article-content h2 {{
            font-size: 2rem;
            font-weight: 700;
            color: #374151;
            margin-top: 3rem;
            margin-bottom: 1.5rem;
            padding-bottom: 0.5rem;
            border-bottom: 3px solid #e5e7eb;
        }}

        .article-content h3 {{
            font-size: 1.5rem;
            font-weight: 600;
            color: #4b5563;
            margin-top: 2rem;
            margin-bottom: 1rem;
        }}

        .article-content p {{
            font-size: 1.0625rem;
            line-height: 1.8;
            color: #374151;
            margin-bottom: 1.25rem;
        }}

        .article-content ul,
        .article-content ol {{
            margin-bottom: 1.5rem;
            padding-left: 2rem;
        }}

        .article-content li {{
            font-size: 1.0625rem;
            line-height: 1.7;
            color: #4b5563;
            margin-bottom: 0.5rem;
        }}

        .article-content strong {{
            font-weight: 700;
            color: #1f2937;
        }}

        .article-content table {{
            width: 100%;
            border-collapse: collapse;
            margin: 2rem 0;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            border-radius: 0.5rem;
            overflow: hidden;
        }}

        .article-content thead {{
            background: linear-gradient(135deg, #3b82f6, #2563eb);
        }}

        .article-content th {{
            padding: 1rem;
            text-align: left;
            color: white;
            font-weight: 600;
        }}

        .article-content td {{
            padding: 1rem;
            border-bottom: 1px solid #e5e7eb;
        }}

        @media (max-width: 768px) {{
            .article-nav {{
                flex-direction: column;
                gap: 1rem;
            }}
            
            .article-container {{
                padding: 1rem;
            }}

            .article-content {{
                padding: 1.5rem;
            }}

            .article-content h1 {{
                font-size: 2rem;
            }}
        }}
    </style>
</head>
<body class="article-page">
    <header class="article-header">
        <nav class="article-nav">
            <a href="index.html" class="logo">
                <div class="logo-icon">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M12 2L12 6M12 18L12 22M6 12L2 12M22 12L18 12"/>
                        <circle cx="12" cy="12" r="4"/>
                    </svg>
                </div>
                <span class="logo-text">Orthopedic<span class="highlight">KB</span></span>
            </a>
            <nav class="main-nav">
                <a href="index.html" class="nav-link">Home</a>
                <a href="huefte.html" class="nav-link active">Hüfte</a>
            </nav>
        </nav>
    </header>

    <div class="breadcrumbs">
        <a href="index.html">Home</a>
        <span class="breadcrumb-separator">›</span>
        <a href="huefte.html">Hüfte</a>
        <span class="breadcrumb-separator">›</span>
        <span>{breadcrumb}</span>
    </div>

    <div class="article-container">
        <a href="huefte.html" class="back-link">
            ← Zurück zur Übersicht
        </a>

        <div class="article-content">
{content}
        </div>
    </div>
</body>
</html>'''


def extract_title(html_content):
    """Extrahiert den Titel aus dem ersten h1-Tag oder dem title-Tag"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Versuche h1 zu finden
    h1 = soup.find('h1')
    if h1:
        return h1.get_text().strip()
    
    # Versuche title-Tag
    title = soup.find('title')
    if title:
        title_text = title.get_text().strip()
        # Entferne " - Orthopedic Knowledge Base" falls vorhanden
        title_text = re.sub(r'\s*-\s*Orthopedic Knowledge Base.*$', '', title_text)
        return title_text
    
    return "Artikel"


def extract_content(html_content):
    """Extrahiert den Hauptinhalt aus dem HTML"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Versuche den Inhalt zu finden
    # Mögliche Container: article, main, div mit bestimmten Klassen
    content = None
    
    # Suche nach article tag
    article = soup.find('article')
    if article:
        content = article
    else:
        # Suche nach main tag
        main = soup.find('main')
        if main:
            content = main
        else:
            # Suche nach body
            body = soup.find('body')
            if body:
                content = body
    
    if content:
        # Entferne störende Elemente
        for elem in content.find_all(['script', 'style', 'nav', 'header', 'footer']):
            elem.decompose()
        
        # Entferne "Zurück"-Links
        for a in content.find_all('a'):
            if 'zurück' in a.get_text().lower():
                a.decompose()
        
        # Hole den HTML-Inhalt
        return str(content).strip()
    
    # Fallback: gesamten body-Inhalt
    body = soup.find('body')
    if body:
        return str(body).strip()
    
    return html_content


def create_breadcrumb_name(title):
    """Erstellt einen kürzeren Breadcrumb-Namen"""
    # Kürze sehr lange Titel
    if len(title) > 50:
        return title[:47] + "..."
    return title


def convert_article(filepath, output_dir=None):
    """Konvertiert einen Artikel in das neue Format"""
    print(f"📄 Konvertiere: {filepath.name}")
    
    try:
        # Lese die Originaldatei
        with open(filepath, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Extrahiere Titel und Inhalt
        title = extract_title(html_content)
        content = extract_content(html_content)
        breadcrumb = create_breadcrumb_name(title)
        
        # Erstelle neues HTML
        new_html = ARTICLE_TEMPLATE.format(
            title=title,
            breadcrumb=breadcrumb,
            content=content
        )
        
        # Bestimme Ausgabepfad
        if output_dir:
            output_path = output_dir / filepath.name
        else:
            output_path = filepath
        
        # Erstelle Backup
        backup_path = filepath.with_suffix('.html.backup')
        if not backup_path.exists():
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"💾 Backup: {backup_path.name}")
        
        # Schreibe neue Datei
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(new_html)
        
        print(f"✅ Erfolgreich konvertiert: {filepath.name}")
        return True
        
    except Exception as e:
        print(f"❌ Fehler bei {filepath.name}: {e}")
        return False


def main():
    """Hauptfunktion"""
    print("🔄 Artikel-Konverter für Orthopedic Knowledge Base")
    print("=" * 60)
    
    # Aktuelles Verzeichnis
    current_dir = Path.cwd()
    print(f"📂 Arbeitsverzeichnis: {current_dir}")
    print()
    
    # Finde alle HTML-Dateien (außer index.html und huefte.html)
    exclude_files = {'index.html', 'huefte.html', 'hufte.html'}
    html_files = [
        f for f in current_dir.glob('*.html') 
        if f.name.lower() not in exclude_files 
        and not f.name.endswith('.backup')
    ]
    
    if not html_files:
        print("❌ Keine Artikel-HTML-Dateien gefunden!")
        return
    
    print(f"📋 Gefundene Artikel: {len(html_files)}")
    print()
    
    # Bestätigung
    print("⚠️  WICHTIG:")
    print("- Backups werden erstellt (.html.backup)")
    print("- Alle Artikel werden in das neue Format konvertiert")
    print()
    
    response = input("Möchten Sie fortfahren? (j/n): ")
    if response.lower() not in ['j', 'ja', 'y', 'yes']:
        print("❌ Abgebrochen.")
        return
    
    print()
    print("🔄 Starte Konvertierung...")
    print()
    
    # Konvertiere alle Dateien
    success_count = 0
    for filepath in html_files:
        if convert_article(filepath):
            success_count += 1
        print()
    
    # Zusammenfassung
    print("=" * 60)
    print(f"✅ Erfolgreich konvertiert: {success_count}/{len(html_files)}")
    print(f"💾 Backups wurden erstellt (.html.backup)")
    print()
    print("🎉 Fertig! Öffnen Sie die Artikel im Browser zum Testen.")


if __name__ == "__main__":
    main()
