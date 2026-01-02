#!/usr/bin/env python3
"""
=======================================================
Joint Alignment Compendium - Batch Update Script
=======================================================
Aktualisiert alle HTML-Artikel mit neuem Branding und Footer

Ausführung im Terminal:
  cd /Users/julianmarques/Library/Mobile\ Documents/com~apple~CloudDocs/1_Forschung/Hüfte/Spinopelvines\ Alignmentstrategien/website/uebersichtsartikel
  python3 update_all_articles.py
=======================================================
"""

import os
import re
from pathlib import Path

# Basis-Pfad (wird automatisch ermittelt)
BASE_PATH = Path(__file__).parent

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

# Dateien die übersprungen werden
SKIP_FILES = {
    'index.html', 'huefte.html', 'impressum.html', 'datenschutz.html', 
    'disclaimer.html', 'ueber.html', '404.html', 
    'artikel-vorlage-leer.html', 'artikel-vorlage-neu.html',
    'update_all_articles.py'
}

def update_html_content(content):
    """Aktualisiert HTML-Inhalt mit neuem Branding"""
    original = content
    
    # 1. Titel aktualisieren
    content = content.replace('Orthopedic Knowledge Base', 'Joint Alignment Compendium')
    content = content.replace('OrthopedicKB', 'Joint Alignment Compendium')
    
    # 2. Logo aktualisieren (verschiedene Varianten)
    content = re.sub(
        r'Orthopedic<span class="logo-highlight">KB</span>',
        '<span>Joint</span><span class="logo-highlight">Alignment</span><span>Compendium</span>',
        content
    )
    content = re.sub(
        r'<span class="logo-text">Orthopedic<span class="highlight">KB</span></span>',
        '<span>Joint</span><span class="logo-highlight">Alignment</span><span>Compendium</span>',
        content
    )
    
    # 3. Navigation erweitern um "Über" (wenn nicht vorhanden)
    if 'ueber.html' not in content:
        content = re.sub(
            r'(<a href="huefte\.html"[^>]*>Hüfte</a>)\s*(</nav>)',
            r'\1\n                <a href="ueber.html" class="nav-link">Über</a>\2',
            content
        )
        content = re.sub(
            r'(<a href="huefte\.html">Hüfte</a>)\s*(</nav>)',
            r'\1\n                <a href="ueber.html">Über</a>\2',
            content
        )
    
    # 4. Alten Footer entfernen (verschiedene Varianten)
    # Einfacher alter Footer
    content = re.sub(
        r'<footer class="site-footer">\s*<p class="footer-brand">.*?</footer>',
        '',
        content,
        flags=re.DOTALL
    )
    # Main-Footer
    content = re.sub(
        r'<footer class="main-footer"[^>]*>.*?</footer>',
        '',
        content,
        flags=re.DOTALL
    )
    
    # 5. Neuen Footer vor </body> einfügen (wenn nicht schon vorhanden)
    if 'Joint Alignment Compendium. Alle Rechte vorbehalten' not in content:
        if '</body>' in content:
            content = content.replace('</body>', NEW_FOOTER + '\n</body>')
    
    return content, content != original

def process_directory(directory, depth=0):
    """Verarbeitet ein Verzeichnis rekursiv"""
    updated_count = 0
    skipped_count = 0
    error_count = 0
    
    for item in sorted(directory.iterdir()):
        if item.is_dir():
            # Rekursiv in Unterverzeichnisse
            if not item.name.startswith('.'):
                u, s, e = process_directory(item, depth + 1)
                updated_count += u
                skipped_count += s
                error_count += e
        elif item.suffix == '.html' and item.name not in SKIP_FILES:
            # HTML-Datei verarbeiten
            if '.backup' in item.name:
                continue
                
            try:
                content = item.read_text(encoding='utf-8')
                updated_content, changed = update_html_content(content)
                
                if changed:
                    # Backup erstellen
                    backup_path = item.with_suffix('.html.backup_jac')
                    if not backup_path.exists():
                        backup_path.write_text(content, encoding='utf-8')
                    
                    # Datei aktualisieren
                    item.write_text(updated_content, encoding='utf-8')
                    print(f"  ✅ {item.name}")
                    updated_count += 1
                else:
                    print(f"  ⏭️  {item.name} (keine Änderung)")
                    skipped_count += 1
                    
            except Exception as e:
                print(f"  ❌ {item.name}: {e}")
                error_count += 1
    
    return updated_count, skipped_count, error_count

def main():
    print("=" * 60)
    print("Joint Alignment Compendium - Website Update")
    print("=" * 60)
    print(f"\n📁 Verzeichnis: {BASE_PATH}")
    print("\n🔄 Verarbeite HTML-Dateien...\n")
    
    updated, skipped, errors = process_directory(BASE_PATH)
    
    print("\n" + "=" * 60)
    print("ZUSAMMENFASSUNG:")
    print(f"   ✅ Aktualisiert: {updated}")
    print(f"   ⏭️  Übersprungen: {skipped}")
    print(f"   ❌ Fehler: {errors}")
    print(f"   📁 Backups erstellt mit Endung .backup_jac")
    print("=" * 60)

if __name__ == "__main__":
    main()
