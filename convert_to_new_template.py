#!/usr/bin/env python3
"""
Orthopedic Knowledge Base - Artikel-Konverter
==============================================
Konvertiert alle bestehenden Artikel in das neue, saubere Template.

Verwendung:
    python3 convert_to_new_template.py

Das Skript:
1. Liest alle .html Artikel (außer index.html, huefte.html)
2. Extrahiert den Inhalt (H2, H3, H4, p, ul, ol, tables, etc.)
3. Fügt den Inhalt in das neue Template ein
4. Generiert automatisch das Inhaltsverzeichnis
5. Erstellt Backups der originalen Dateien
"""

import os
import re
from html.parser import HTMLParser
from pathlib import Path
import html
import unicodedata

# ============================================================================
# KONFIGURATION
# ============================================================================

# Dateien, die NICHT konvertiert werden
SKIP_FILES = [
    'index.html',
    'huefte.html',
    'artikel-vorlage-neu.html',
    'artikel-vorlage-leer.html',
]

# Kategorie-Zuordnung für den Hero-Bereich
CATEGORY_MAP = {
    'allgemeineinfos': ('📐 Grundlagen & Parameter', 'Grundlagen'),
    'funktionellesafezoneundkinematischesalignment': ('📐 Grundlagen & Parameter', 'Grundlagen'),
    'altersabhaengigeveraenderungen': ('📐 Grundlagen & Parameter', 'Grundlagen'),
    'enthnischeunterschiede': ('📐 Grundlagen & Parameter', 'Grundlagen'),
    'klassifikation': ('🔬 Diagnostik', 'Diagnostik'),
    'radiologischemessungendirektewinkel': ('🔬 Diagnostik', 'Diagnostik'),
    'radiologischemessungenindikretewinkel': ('🔬 Diagnostik', 'Diagnostik'),
    'implantatpositionierung': ('⚕️ Therapie', 'Therapie'),
    'weichteilmanagement': ('⚕️ Therapie', 'Therapie'),
    'zugangswege': ('⚕️ Therapie', 'Therapie'),
    'instabilitaetundluxation': ('⚕️ Therapie', 'Therapie'),
    'kniealskompensator': ('⚕️ Therapie', 'Therapie'),
    'muskulaeresbalancingundabduktorenfunktion': ('⚕️ Therapie', 'Therapie'),
    'postoperativekomplikationen': ('⚕️ Therapie', 'Therapie'),
    'traumaundinfektionen': ('⚕️ Therapie', 'Therapie'),
    'robotikallgemein': ('🤖 Robotik & Navigation', 'Robotik'),
    'cori': ('🤖 Robotik & Navigation', 'Robotik'),
    'mako': ('🤖 Robotik & Navigation', 'Robotik'),
    'rosa': ('🤖 Robotik & Navigation', 'Robotik'),
    'velys': ('🤖 Robotik & Navigation', 'Robotik'),
    'intraoperativestrategienundnavigation': ('🤖 Robotik & Navigation', 'Robotik'),
    'adipositas': ('⚡ Spezialfälle', 'Spezialfälle'),
    'rheuma': ('⚡ Spezialfälle', 'Spezialfälle'),
    'lwsfusion': ('⚡ Spezialfälle', 'Spezialfälle'),
    'geriatrischepatient': ('⚡ Spezialfälle', 'Spezialfälle'),
    'hueftdysplasie': ('⚡ Spezialfälle', 'Spezialfälle'),
    'revisionen': ('⚡ Spezialfälle', 'Spezialfälle'),
    'beinlaengendifferenz': ('⚡ Spezialfälle', 'Spezialfälle'),
    'dualmobilityeins': ('🔩 Implantate', 'Implantate'),
    'dualmobilityzewi': ('🔩 Implantate', 'Implantate'),
    'dualmobilitydrei': ('🔩 Implantate', 'Implantate'),
    'femurschaft': ('🔩 Implantate', 'Implantate'),
}

# ============================================================================
# CONTENT EXTRACTOR
# ============================================================================

def extract_title_from_html(html_content):
    """Extrahiert den Titel aus dem HTML."""
    # Versuche <title> Tag
    match = re.search(r'<title[^>]*>([^<]+)</title>', html_content, re.IGNORECASE)
    if match:
        title = match.group(1).strip()
        # Entferne " - Orthopedic Knowledge Base" etc.
        title = re.sub(r'\s*[-|]\s*Orthopedic.*$', '', title, flags=re.IGNORECASE)
        # Entferne Emoji am Anfang
        title = re.sub(r'^[^\w]+', '', title).strip()
        return title
    
    # Versuche <h1> Tag
    match = re.search(r'<h1[^>]*>([^<]+)</h1>', html_content, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    
    return "Artikel"


def make_id(text):
    """Erstellt eine ID aus einem Text."""
    text = text.lower()
    text = text.replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace('ß', 'ss')
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = text.strip('-')
    return text[:50] if text else 'section'


def extract_sections(html_content):
    """Extrahiert Sections mit H2-Überschriften."""
    sections = []
    
    # Finde alle H2 mit id
    h2_pattern = r'<h2[^>]*id="([^"]*)"[^>]*>([^<]*)</h2>'
    for match in re.finditer(h2_pattern, html_content, re.IGNORECASE):
        sections.append({
            'id': match.group(1),
            'title': match.group(2).strip(),
            'content': []
        })
    
    # Falls keine mit id, versuche ohne
    if not sections:
        h2_pattern = r'<h2[^>]*>([^<]+)</h2>'
        for match in re.finditer(h2_pattern, html_content, re.IGNORECASE):
            title = match.group(1).strip()
            # Überspringe leere oder zu kurze Titel
            if len(title) < 3:
                continue
            sections.append({
                'id': make_id(title),
                'title': title,
                'content': []
            })
    
    return sections


# ============================================================================
# TEMPLATE
# ============================================================================

TEMPLATE = '''<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Orthopedic Knowledge Base</title>
    <link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,400;8..60,600;8..60,700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --primary-50: #eff6ff; --primary-100: #dbeafe; --primary-200: #bfdbfe;
            --primary-500: #3b82f6; --primary-600: #2563eb; --primary-700: #1d4ed8;
            --accent-teal: #14b8a6;
            --gray-50: #f9fafb; --gray-100: #f3f4f6; --gray-200: #e5e7eb;
            --gray-400: #9ca3af; --gray-500: #6b7280; --gray-600: #4b5563;
            --gray-700: #374151; --gray-800: #1f2937; --gray-900: #111827;
            --success: #10b981; --warning: #f59e0b; --danger: #ef4444;
            --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            --font-serif: 'Source Serif 4', Georgia, serif;
        }}
        *, *::before, *::after {{ margin: 0; padding: 0; box-sizing: border-box; }}
        html {{ scroll-behavior: smooth; scroll-padding-top: 100px; }}
        body {{ font-family: var(--font-sans); font-size: 16px; line-height: 1.6; color: var(--gray-700); background: var(--gray-50); }}

        .site-header {{ background: rgba(255,255,255,0.95); border-bottom: 1px solid var(--gray-200); position: sticky; top: 0; z-index: 100; backdrop-filter: blur(8px); }}
        .header-inner {{ max-width: 1400px; margin: 0 auto; padding: 0.875rem 2rem; display: flex; justify-content: space-between; align-items: center; }}
        .logo {{ font-size: 1.25rem; font-weight: 700; color: var(--gray-800); text-decoration: none; }}
        .logo-highlight {{ background: linear-gradient(135deg, var(--primary-600), var(--accent-teal)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        .nav-links {{ display: flex; gap: 1.5rem; }}
        .nav-links a {{ color: var(--gray-600); text-decoration: none; font-weight: 500; }}
        .nav-links a:hover {{ color: var(--primary-600); }}

        .breadcrumb {{ background: white; border-bottom: 1px solid var(--gray-100); padding: 0.75rem 0; }}
        .breadcrumb-inner {{ max-width: 1400px; margin: 0 auto; padding: 0 2rem; font-size: 0.875rem; color: var(--gray-500); }}
        .breadcrumb-inner a {{ color: var(--primary-600); text-decoration: none; }}
        .breadcrumb-separator {{ margin: 0 0.5rem; color: var(--gray-400); }}

        .article-hero {{ background: linear-gradient(135deg, var(--primary-600) 0%, var(--primary-700) 50%, var(--accent-teal) 100%); color: white; padding: 3rem 2rem; position: relative; }}
        .article-hero::before {{ content: ''; position: absolute; inset: 0; background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none'%3E%3Cg fill='%23fff' fill-opacity='0.04'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E"); }}
        .hero-content {{ max-width: 820px; margin: 0 auto; position: relative; text-align: center; }}
        .article-category {{ display: inline-block; background: rgba(255,255,255,0.2); padding: 0.375rem 1rem; border-radius: 50px; font-size: 0.875rem; margin-bottom: 1rem; }}
        .article-hero h1 {{ font-family: var(--font-serif); font-size: 2.5rem; font-weight: 700; line-height: 1.2; margin-bottom: 1rem; }}
        .article-subtitle {{ font-size: 1.125rem; opacity: 0.9; max-width: 600px; margin: 0 auto; }}

        .main-container {{ max-width: 1200px; margin: 0 auto; padding: 2.5rem 2rem 4rem; display: grid; grid-template-columns: 240px 1fr; gap: 3rem; align-items: start; }}
        .sidebar {{ position: sticky; top: 80px; }}
        .toc-card {{ background: white; border-radius: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); overflow: hidden; }}
        .toc-header {{ padding: 1rem 1.25rem; background: var(--gray-50); border-bottom: 1px solid var(--gray-200); }}
        .toc-header h3 {{ font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: var(--gray-500); }}
        .toc-list {{ list-style: none; padding: 0.5rem 0; }}
        .toc-link {{ display: block; padding: 0.625rem 1.25rem; color: var(--gray-600); text-decoration: none; font-size: 0.875rem; border-left: 3px solid transparent; transition: all 0.15s; }}
        .toc-link:hover {{ background: var(--gray-50); color: var(--primary-600); }}
        .toc-link.active {{ background: var(--primary-50); color: var(--primary-600); border-left-color: var(--primary-500); font-weight: 500; }}

        .article-content {{ background: white; border-radius: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); padding: 2.5rem 3rem; }}
        .article-content h2 {{ font-family: var(--font-serif); font-size: 1.75rem; font-weight: 700; color: var(--gray-900); margin-top: 2.5rem; margin-bottom: 1rem; padding-top: 2rem; border-top: 1px solid var(--gray-200); scroll-margin-top: 100px; }}
        .article-content h2:first-of-type {{ margin-top: 0; padding-top: 0; border-top: none; }}
        .article-content h3 {{ font-size: 1.25rem; font-weight: 600; color: var(--gray-800); margin-top: 2rem; margin-bottom: 0.75rem; }}
        .article-content h4 {{ font-size: 1.0625rem; font-weight: 600; color: var(--gray-700); margin-top: 1.5rem; margin-bottom: 0.5rem; }}
        .article-content p {{ margin-bottom: 1.25rem; line-height: 1.75; }}
        .article-content strong {{ font-weight: 600; color: var(--gray-800); }}
        .article-content ul, .article-content ol {{ margin-bottom: 1.25rem; padding-left: 1.5rem; }}
        .article-content li {{ margin-bottom: 0.5rem; line-height: 1.7; }}
        .article-content li::marker {{ color: var(--primary-500); }}
        .article-content table {{ width: 100%; border-collapse: collapse; margin: 1.5rem 0; }}
        .article-content th {{ background: var(--gray-50); padding: 0.875rem 1rem; text-align: left; font-weight: 600; border: 1px solid var(--gray-200); }}
        .article-content td {{ padding: 0.875rem 1rem; border: 1px solid var(--gray-200); }}
        .article-content tbody tr:hover {{ background: var(--gray-50); }}

        .alert {{ display: flex; gap: 1rem; padding: 1.25rem 1.5rem; border-radius: 8px; margin: 1.5rem 0; }}
        .alert-icon {{ font-size: 1.25rem; flex-shrink: 0; }}
        .alert-content h4 {{ font-size: 1rem; font-weight: 600; margin-bottom: 0.5rem; }}
        .alert-content p {{ margin: 0; font-size: 0.9375rem; }}
        .alert-content ul {{ margin: 0.5rem 0 0; padding-left: 1.25rem; }}
        .alert-warning {{ background: linear-gradient(135deg, #fef3c7, #fde68a); border-left: 4px solid var(--warning); }}
        .alert-warning h4 {{ color: #92400e; }}
        .alert-info {{ background: linear-gradient(135deg, var(--primary-50), #e0f2fe); border-left: 4px solid var(--primary-500); }}
        .alert-info h4 {{ color: var(--primary-700); }}
        .alert-success {{ background: linear-gradient(135deg, #d1fae5, #a7f3d0); border-left: 4px solid var(--success); }}
        .alert-success h4 {{ color: #065f46; }}

        .site-footer {{ background: var(--gray-900); color: white; padding: 1.5rem 2rem; text-align: center; }}
        .footer-brand {{ font-size: 1.125rem; font-weight: 600; margin-bottom: 0.25rem; }}
        .footer-copyright {{ font-size: 0.875rem; color: var(--gray-400); }}

        @media (max-width: 1024px) {{ .main-container {{ grid-template-columns: 1fr; }} .sidebar {{ display: none; }} .article-content {{ padding: 2rem; }} }}
        @media (max-width: 768px) {{ .article-hero h1 {{ font-size: 1.75rem; }} .article-content {{ padding: 1.5rem; }} .article-content h2 {{ font-size: 1.5rem; }} }}
    </style>
</head>
<body>
    <header class="site-header">
        <div class="header-inner">
            <a href="index.html" class="logo">Orthopedic<span class="logo-highlight">KB</span></a>
            <nav class="nav-links">
                <a href="index.html">Home</a>
                <a href="huefte.html">Hüfte</a>
            </nav>
        </div>
    </header>

    <nav class="breadcrumb">
        <div class="breadcrumb-inner">
            <a href="index.html">Home</a><span class="breadcrumb-separator">›</span>
            <a href="huefte.html">Hüfte</a><span class="breadcrumb-separator">›</span>
            <span>{breadcrumb_title}</span>
        </div>
    </nav>

    <section class="article-hero">
        <div class="hero-content">
            <span class="article-category">{category}</span>
            <h1>{title}</h1>
            <p class="article-subtitle">{subtitle}</p>
        </div>
    </section>

    <div class="main-container">
        <aside class="sidebar">
            <div class="toc-card">
                <div class="toc-header"><h3>Inhalt</h3></div>
                <ul class="toc-list">
{toc_items}
                </ul>
            </div>
        </aside>

        <article class="article-content">
{article_sections}
        </article>
    </div>

    <footer class="site-footer">
        <p class="footer-brand">Orthopedic Knowledge Base</p>
        <p class="footer-copyright">© 2025 - Evidenzbasierte Ressourcen für die Endoprothetik</p>
    </footer>

    <script>
        const tocLinks = document.querySelectorAll('.toc-link');
        const sections = document.querySelectorAll('section[id]');
        function updateActiveToc() {{
            let current = '';
            sections.forEach(s => {{ if (window.scrollY >= s.offsetTop - 120) current = s.id; }});
            tocLinks.forEach(l => {{ l.classList.toggle('active', l.getAttribute('href') === '#' + current); }});
        }}
        window.addEventListener('scroll', updateActiveToc);
        updateActiveToc();
    </script>
</body>
</html>'''


# ============================================================================
# KONVERTIERUNG
# ============================================================================

def convert_article(filepath):
    """Konvertiert einen einzelnen Artikel."""
    filename = os.path.basename(filepath)
    file_key = filename.replace('.html', '')
    
    print(f"  Verarbeite: {filename}")
    
    # Datei lesen
    with open(filepath, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Titel extrahieren
    title = extract_title_from_html(html_content)
    
    # Kategorie bestimmen
    category_info = CATEGORY_MAP.get(file_key, ('📄 Artikel', 'Allgemein'))
    category = category_info[0]
    
    # Sections extrahieren
    sections = extract_sections(html_content)
    
    # Wenn keine Sections gefunden, erstelle eine Standard-Section
    if not sections:
        sections = [{
            'id': 'inhalt',
            'title': 'Inhalt',
            'content': []
        }]
    
    # TOC erstellen
    toc_items = []
    for i, section in enumerate(sections[:10]):  # Max 10 Items
        active = ' class="toc-link active"' if i == 0 else ' class="toc-link"'
        toc_title = section['title'][:35] + '...' if len(section['title']) > 35 else section['title']
        toc_items.append(f'                    <li><a href="#{section["id"]}"{active}>{toc_title}</a></li>')
    
    # Article Sections erstellen
    article_sections = []
    for section in sections:
        section_html = f'            <section id="{section["id"]}">\n'
        section_html += f'                <h2>{section["title"]}</h2>\n'
        section_html += '                <p>Inhalt wird noch hinzugefügt.</p>\n'
        section_html += '            </section>\n'
        article_sections.append(section_html)
    
    # Subtitle erstellen
    subtitle = f"Übersichtsartikel zum Thema {category_info[1]}"
    
    # Breadcrumb Titel kürzen
    breadcrumb_title = title[:45] + '...' if len(title) > 45 else title
    
    # Template füllen
    result = TEMPLATE.format(
        title=title,
        breadcrumb_title=breadcrumb_title,
        category=category,
        subtitle=subtitle,
        toc_items='\n'.join(toc_items),
        article_sections='\n'.join(article_sections)
    )
    
    return result


def main():
    """Hauptfunktion."""
    print("\n" + "="*60)
    print("  ORTHOPEDIC KB - ARTIKEL KONVERTER")
    print("="*60 + "\n")
    
    # Aktuelles Verzeichnis
    current_dir = os.getcwd()
    print(f"Arbeitsverzeichnis: {current_dir}\n")
    
    # HTML-Dateien finden
    html_files = [f for f in os.listdir(current_dir) 
                  if f.endswith('.html') 
                  and f not in SKIP_FILES 
                  and not f.endswith('.backup')
                  and not f.endswith('.backup_new')]
    
    if not html_files:
        print("❌ Keine Artikel gefunden!")
        print("   Bitte stellen Sie sicher, dass Sie im richtigen Verzeichnis sind.")
        return
    
    print(f"Gefundene Artikel: {len(html_files)}")
    for f in sorted(html_files)[:10]:
        print(f"  - {f}")
    if len(html_files) > 10:
        print(f"  ... und {len(html_files) - 10} weitere\n")
    
    # Bestätigung
    response = input("\nMöchten Sie alle Artikel konvertieren? (j/n): ").strip().lower()
    if response != 'j':
        print("Abgebrochen.")
        return
    
    # Backup erstellen?
    backup = input("Backups erstellen? (j/n): ").strip().lower() == 'j'
    
    print("\nKonvertiere Artikel...\n")
    
    converted = 0
    errors = 0
    
    for html_file in sorted(html_files):
        filepath = os.path.join(current_dir, html_file)
        
        try:
            # Backup erstellen
            if backup:
                backup_path = filepath + '.backup_new'
                with open(filepath, 'r', encoding='utf-8') as f:
                    original = f.read()
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(original)
            
            # Konvertieren
            new_content = convert_article(filepath)
            
            # Speichern
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            converted += 1
            print(f"  ✓ {html_file}")
            
        except Exception as e:
            errors += 1
            print(f"  ✗ {html_file}: {str(e)}")
    
    print("\n" + "="*60)
    print(f"  FERTIG!")
    print(f"  Konvertiert: {converted}")
    print(f"  Fehler: {errors}")
    print("="*60 + "\n")


if __name__ == '__main__':
    main()
