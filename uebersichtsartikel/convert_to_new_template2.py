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

class ContentExtractor(HTMLParser):
    """Extrahiert den relevanten Inhalt aus kaputtem HTML."""
    
    def __init__(self):
        super().__init__()
        self.reset_state()
    
    def reset_state(self):
        self.sections = []
        self.current_section = None
        self.current_content = []
        self.in_content = False
        self.tag_stack = []
        self.title = ""
        self.subtitle = ""
        self.skip_next = False
        
        # Tags die wir sammeln wollen
        self.content_tags = {'h2', 'h3', 'h4', 'p', 'ul', 'ol', 'li', 'table', 'thead', 'tbody', 'tr', 'th', 'td', 'strong', 'em', 'a'}
        self.block_tags = {'h2', 'h3', 'h4', 'p', 'ul', 'ol', 'li', 'table', 'tr', 'th', 'td', 'thead', 'tbody'}
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        
        # Titel aus verschiedenen Quellen extrahieren
        if tag == 'h1' and not self.title:
            self.in_content = True
            self.tag_stack.append(('h1_title', attrs_dict))
            return
            
        # H2 startet eine neue Section
        if tag == 'h2':
            if self.current_section:
                self.sections.append(self.current_section)
            self.current_section = {
                'id': attrs_dict.get('id', ''),
                'title': '',
                'content': []
            }
            self.tag_stack.append(('h2', attrs_dict))
            return
        
        # Content-Tags sammeln wenn wir in einer Section sind
        if self.current_section and tag in self.content_tags:
            self.tag_stack.append((tag, attrs_dict))
            
            # Block-Tags als neuen Content-Block
            if tag in {'h3', 'h4', 'p'}:
                self.current_content = []
            elif tag == 'ul':
                self.current_content = ['<ul>']
            elif tag == 'ol':
                self.current_content = ['<ol>']
            elif tag == 'li':
                self.current_content.append('<li>')
            elif tag == 'table':
                self.current_content = ['<table>']
            elif tag in {'thead', 'tbody', 'tr', 'th', 'td'}:
                self.current_content.append(f'<{tag}>')
    
    def handle_endtag(self, tag):
        if not self.tag_stack:
            return
            
        current_tag, _ = self.tag_stack[-1]
        
        # H1 Title
        if current_tag == 'h1_title' and tag == 'h1':
            self.tag_stack.pop()
            self.title = ' '.join(self.current_content).strip()
            self.current_content = []
            return
        
        # H2 Title
        if current_tag == 'h2' and tag == 'h2':
            self.tag_stack.pop()
            if self.current_section:
                self.current_section['title'] = ' '.join(self.current_content).strip()
                # ID generieren wenn nicht vorhanden
                if not self.current_section['id']:
                    self.current_section['id'] = self.make_id(self.current_section['title'])
            self.current_content = []
            return
        
        # H3, H4, P schließen
        if tag in {'h3', 'h4', 'p'} and self.current_section:
            text = ' '.join(self.current_content).strip()
            if text:
                if tag == 'h3':
                    self.current_section['content'].append(f'<h3>{text}</h3>')
                elif tag == 'h4':
                    self.current_section['content'].append(f'<h4>{text}</h4>')
                else:
                    self.current_section['content'].append(f'<p>{text}</p>')
            self.current_content = []
            if self.tag_stack and self.tag_stack[-1][0] == tag:
                self.tag_stack.pop()
            return
        
        # Listen schließen
        if tag == 'li' and self.current_section:
            self.current_content.append('</li>')
        elif tag == 'ul' and self.current_section:
            self.current_content.append('</ul>')
            content = ''.join(self.current_content)
            if '<li>' in content:
                self.current_section['content'].append(content)
            self.current_content = []
            if self.tag_stack and self.tag_stack[-1][0] == 'ul':
                self.tag_stack.pop()
        elif tag == 'ol' and self.current_section:
            self.current_content.append('</ol>')
            content = ''.join(self.current_content)
            if '<li>' in content:
                self.current_section['content'].append(content)
            self.current_content = []
            if self.tag_stack and self.tag_stack[-1][0] == 'ol':
                self.tag_stack.pop()
        
        # Tabellen schließen
        elif tag in {'thead', 'tbody', 'tr', 'th', 'td'}:
            self.current_content.append(f'</{tag}>')
        elif tag == 'table' and self.current_section:
            self.current_content.append('</table>')
            content = ''.join(self.current_content)
            if '<tr>' in content:
                self.current_section['content'].append(content)
            self.current_content = []
            if self.tag_stack and self.tag_stack[-1][0] == 'table':
                self.tag_stack.pop()
    
    def handle_data(self, data):
        text = data.strip()
        if not text:
            return
        
        if self.tag_stack:
            # Für Inline-Tags den Text hinzufügen
            self.current_content.append(text)
    
    def make_id(self, text):
        """Erstellt eine ID aus einem Text."""
        # Umlaute ersetzen
        text = text.lower()
        text = text.replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace('ß', 'ss')
        # Nur alphanumerische Zeichen und Bindestriche
        text = re.sub(r'[^a-z0-9]+', '-', text)
        text = text.strip('-')
        return text[:50] if text else 'section'
    
    def get_result(self):
        """Gibt die extrahierten Daten zurück."""
        # Letzte Section hinzufügen
        if self.current_section:
            self.sections.append(self.current_section)
        
        return {
            'title': self.title,
            'subtitle': self.subtitle,
            'sections': self.sections
        }


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


def extract_content_simple(html_content):
    """Einfachere Extraktion mit RegEx."""
    sections = []
    
    # Finde alle H2 Überschriften mit ihrem Inhalt
    h2_pattern = r'<h2[^>]*id="([^"]*)"[^>]*>([^<]*)</h2>'
    h2_matches = list(re.finditer(h2_pattern, html_content, re.IGNORECASE | re.DOTALL))
    
    if not h2_matches:
        # Versuche H2 ohne id
        h2_pattern = r'<h2[^>]*>([^<]+)</h2>'
        for match in re.finditer(h2_pattern, html_content, re.IGNORECASE):
            title = match.group(1).strip()
            section_id = re.sub(r'[^a-z0-9]+', '-', title.lower())[:40]
            sections.append({
                'id': section_id,
                'title': title,
                'content': []
            })
    else:
        for match in h2_matches:
            sections.append({
                'id': match.group(1),
                'title': match.group(2).strip(),
                'content': []
            })
    
    # Extrahiere Paragraphen
    p_pattern = r'<p[^>]*>(.+?)</p>'
    paragraphs = re.findall(p_pattern, html_content, re.IGNORECASE | re.DOTALL)
    
    # Extrahiere Listen
    ul_pattern = r'<ul[^>]*>(.+?)</ul>'
    lists = re.findall(ul_pattern, html_content, re.IGNORECASE | re.DOTALL)
    
    return {
        'title': extract_title_from_html(html_content),
        'sections': sections,
        'raw_paragraphs': paragraphs,
        'raw_lists': lists
    }


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
    
    # Einfache Extraktion der Sections
    data = extract_content_simple(html_content)
    
    # Sections für Template vorbereiten
    sections = data.get('sections', [])
    
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
        
        # Content hinzufügen (wenn vorhanden)
        content = section.get('content', [])
        if content:
            for item in content:
                section_html += f'                {item}\n'
        else:
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
                  and not f.endswith('.backup')]
    
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
