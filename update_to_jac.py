#!/usr/bin/env python3
"""
Update-Skript für Joint Alignment Compendium
Aktualisiert alle HTML-Dateien mit neuem Branding, Footer und Cookie-Banner
"""

import os
import re
from pathlib import Path

# Basis-Pfad
BASE_PATH = "/Users/julianmarques/Library/Mobile Documents/com~apple~CloudDocs/1_Forschung/Hüfte/Spinopelvines Alignmentstrategien/website/uebersichtsartikel"

# Neuer Footer HTML
NEW_FOOTER = '''
    <!-- ===== FOOTER ===== -->
    <footer class="site-footer">
        <div class="footer-inner">
            <div class="footer-top">
                <div class="footer-brand">
                    <h3>Joint Alignment Compendium</h3>
                    <p>Digitales Handbuch für Alignment-Strategien in der Endoprothetik. Strukturiertes Wissen und klinische Strategien für Fachpublikum.</p>
                </div>
                <div class="footer-links">
                    <h4>Navigation</h4>
                    <ul>
                        <li><a href="index.html">Home</a></li>
                        <li><a href="huefte.html">Hüfte</a></li>
                        <li><a href="ueber.html">Über den Autor</a></li>
                    </ul>
                </div>
                <div class="footer-links">
                    <h4>Rechtliches</h4>
                    <ul>
                        <li><a href="impressum.html">Impressum</a></li>
                        <li><a href="datenschutz.html">Datenschutz</a></li>
                        <li><a href="disclaimer.html">Disclaimer</a></li>
                    </ul>
                </div>
            </div>
            <div class="footer-bottom">
                <p class="footer-copyright">© 2025 Joint Alignment Compendium. Alle Rechte vorbehalten.</p>
                <p class="footer-disclaimer">Die Inhalte dienen der Information und Fortbildung und stellen keine klinische Anweisung dar.</p>
            </div>
        </div>
    </footer>
    <style>
    .site-footer { background: #111827; color: white; padding: 3rem 2rem 1.5rem; margin-top: 2rem; }
    .footer-inner { max-width: 1400px; margin: 0 auto; }
    .footer-top { display: grid; grid-template-columns: 2fr 1fr 1fr; gap: 3rem; margin-bottom: 2rem; }
    .footer-brand h3 { font-size: 1.25rem; font-weight: 700; margin-bottom: 0.5rem; }
    .footer-brand p { color: #9ca3af; font-size: 0.875rem; line-height: 1.6; }
    .footer-links h4 { font-size: 0.875rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 1rem; color: #d1d5db; }
    .footer-links ul { list-style: none; padding: 0; margin: 0; }
    .footer-links li { margin-bottom: 0.5rem; }
    .footer-links a { color: #9ca3af; text-decoration: none; font-size: 0.9375rem; }
    .footer-links a:hover { color: white; }
    .footer-bottom { border-top: 1px solid #374151; padding-top: 1.5rem; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; }
    .footer-copyright { font-size: 0.8125rem; color: #6b7280; }
    .footer-disclaimer { font-size: 0.75rem; color: #6b7280; max-width: 600px; line-height: 1.5; }
    @media (max-width: 768px) { .footer-top { grid-template-columns: 1fr; } .footer-bottom { flex-direction: column; text-align: center; } }
    </style>
'''

# Neuer Header HTML
NEW_HEADER = '''<header class="site-header" style="background: rgba(255,255,255,0.95); border-bottom: 1px solid #e5e7eb; position: sticky; top: 0; z-index: 100; backdrop-filter: blur(8px);">
        <div class="header-inner" style="max-width: 1400px; margin: 0 auto; padding: 0.875rem 2rem; display: flex; justify-content: space-between; align-items: center;">
            <a href="index.html" class="logo" style="font-size: 1.25rem; font-weight: 700; color: #1f2937; text-decoration: none; display: flex; align-items: center; gap: 0.5rem;">
                <span>Joint</span><span style="background: linear-gradient(135deg, #2563eb, #14b8a6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">Alignment</span><span>Compendium</span>
            </a>
            <nav class="nav-links" style="display: flex; gap: 1.5rem;">
                <a href="index.html" style="color: #4b5563; text-decoration: none; font-weight: 500;">Home</a>
                <a href="huefte.html" style="color: #4b5563; text-decoration: none; font-weight: 500;">Hüfte</a>
                <a href="ueber.html" style="color: #4b5563; text-decoration: none; font-weight: 500;">Über</a>
            </nav>
        </div>
    </header>'''

# Dateien die übersprungen werden sollen
SKIP_FILES = [
    'index.html', 
    'huefte.html', 
    'impressum.html', 
    'datenschutz.html', 
    'disclaimer.html', 
    'ueber.html', 
    '404.html',
    'artikel-vorlage-leer.html',
    'artikel-vorlage-neu.html'
]

def update_article_file(filepath):
    """Aktualisiert eine Artikel-HTML-Datei mit neuem Header, Footer und Branding"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 1. Titel aktualisieren
        content = content.replace('Orthopedic Knowledge Base', 'Joint Alignment Compendium')
        content = content.replace('OrthopedicKB', 'Joint Alignment Compendium')
        
        # 2. Logo-Text aktualisieren (verschiedene Varianten)
        content = re.sub(
            r'<span class="logo-text">Orthopedic<span class="highlight">KB</span></span>',
            '<span>Joint</span><span class="logo-highlight">Alignment</span><span>Compendium</span>',
            content
        )
        content = re.sub(
            r'Orthopedic<span class="highlight">KB</span>',
            '<span>Joint</span><span class="logo-highlight">Alignment</span><span>Compendium</span>',
            content
        )
        
        # 3. Logo-Highlight CSS hinzufügen wenn nicht vorhanden
        if '.logo-highlight' not in content and '<style>' in content:
            content = content.replace(
                '<style>',
                '<style>\n        .logo-highlight { background: linear-gradient(135deg, #2563eb, #14b8a6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }\n'
            )
        
        # 4. Navigation um "Über" erweitern (wenn nicht vorhanden)
        if 'ueber.html' not in content:
            # Suche nach nav-links und füge Über hinzu
            content = re.sub(
                r'(<a href="huefte\.html"[^>]*>Hüfte</a>)\s*(</nav>)',
                r'\1\n                <a href="ueber.html" class="nav-link">Über</a>\2',
                content
            )
            content = re.sub(
                r'(<a href="huefte\.html"[^>]*>[^<]*</a>)\s*(</nav>)',
                r'\1\n                <a href="ueber.html" class="nav-link">Über</a>\2',
                content
            )
        
        # 5. Alten Footer entfernen
        # Pattern für verschiedene Footer-Varianten
        content = re.sub(r'<footer class="main-footer"[^>]*>.*?</footer>', '', content, flags=re.DOTALL)
        content = re.sub(r'<footer class="site-footer"[^>]*>.*?</footer>\s*(<style>.*?</style>)?', '', content, flags=re.DOTALL)
        content = re.sub(r'<!-- Footer -->.*?</footer>', '', content, flags=re.DOTALL)
        
        # 6. Füge neuen Footer vor </body> ein (wenn noch nicht vorhanden)
        if 'Joint Alignment Compendium. Alle Rechte vorbehalten' not in content:
            if '</body>' in content:
                content = content.replace('</body>', NEW_FOOTER + '\n</body>')
        
        # 7. Speichern nur wenn sich etwas geändert hat
        if content != original_content:
            # Backup erstellen
            backup_path = filepath + '.backup_jac'
            if not os.path.exists(backup_path):
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(original_content)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
        
    except Exception as e:
        print(f"    Fehler: {e}")
        return False

def main():
    print("=" * 60)
    print("Joint Alignment Compendium - Website Update")
    print("=" * 60)
    
    # Alle HTML-Dateien finden
    html_files = []
    for f in os.listdir(BASE_PATH):
        filepath = os.path.join(BASE_PATH, f)
        if os.path.isfile(filepath) and f.endswith('.html'):
            # Überspringe Backup-Dateien und bereits aktualisierte Seiten
            if '.backup' not in f and f not in SKIP_FILES:
                html_files.append(f)
    
    print(f"\n📄 Gefunden: {len(html_files)} HTML-Dateien zum Aktualisieren")
    print(f"   (Übersprungen: {', '.join(SKIP_FILES[:5])}...)")
    
    updated = 0
    skipped = 0
    failed = 0
    
    for filename in sorted(html_files):
        filepath = os.path.join(BASE_PATH, filename)
        print(f"   {filename}...", end=" ")
        result = update_article_file(filepath)
        if result:
            print("✅ aktualisiert")
            updated += 1
        elif result is False:
            print("⏭️  keine Änderung")
            skipped += 1
        else:
            print("❌ Fehler")
            failed += 1
    
    print("\n" + "=" * 60)
    print("ZUSAMMENFASSUNG:")
    print(f"   ✅ Aktualisiert: {updated}")
    print(f"   ⏭️  Übersprungen: {skipped}")
    print(f"   ❌ Fehlgeschlagen: {failed}")
    print(f"   📁 Backups erstellt mit Endung .backup_jac")
    print("=" * 60)

if __name__ == "__main__":
    main()
