#!/usr/bin/env python3
"""
Entfernt Inhaltsverzeichnis-Boxen aus dem Artikel-Content
Behält die Sidebar-Navigation bei
"""

import re
from pathlib import Path


def remove_toc_from_content(html):
    """
    Entfernt Inhaltsverzeichnis-Boxen aus dem Artikel-Content
    Patterns die erkannt werden:
    - <div>INHALTSVERZEICHNIS</div>
    - TOC-Listen im Content
    - Etc.
    """
    
    # Pattern 1: Div mit "INHALTSVERZEICHNIS" Text
    html = re.sub(
        r'<div[^>]*>\s*INHALTSVERZEICHNIS\s*</div>',
        '',
        html,
        flags=re.IGNORECASE
    )
    
    # Pattern 2: Sections mit TOC/Inhaltsverzeichnis
    html = re.sub(
        r'<section[^>]*class=["\'][^"\']*toc[^"\']*["\'][^>]*>.*?</section>',
        '',
        html,
        flags=re.IGNORECASE | re.DOTALL
    )
    
    # Pattern 3: Divs mit TOC-Klassen im Content
    html = re.sub(
        r'<div[^>]*class=["\'][^"\']*table-of-contents[^"\']*["\'][^>]*>.*?</div>',
        '',
        html,
        flags=re.IGNORECASE | re.DOTALL
    )
    
    # Pattern 4: Heading + Liste die wie TOC aussieht
    # z.B. <h2>Inhaltsverzeichnis</h2><ul>...</ul>
    html = re.sub(
        r'<h[2-4][^>]*>\s*Inhaltsverzeichnis\s*</h[2-4]>\s*<ul>.*?</ul>',
        '',
        html,
        flags=re.IGNORECASE | re.DOTALL
    )
    
    # Pattern 5: Standalone "INHALTSVERZEICHNIS" Header
    html = re.sub(
        r'<h[2-4][^>]*>\s*INHALTSVERZEICHNIS\s*</h[2-4]>',
        '',
        html,
        flags=re.IGNORECASE
    )
    
    return html


def clean_article(filepath):
    """Bereinigt einen Artikel von TOC-Boxen"""
    print(f"📄 {filepath.name}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()
        
        original_length = len(html)
        
        # Entferne TOC aus Content
        cleaned = remove_toc_from_content(html)
        
        # Bereinige mehrfache Leerzeilen
        cleaned = re.sub(r'\n\s*\n\s*\n+', '\n\n', cleaned)
        
        if len(cleaned) < original_length:
            removed = original_length - len(cleaned)
            print(f"   🗑️  {removed} Zeichen entfernt")
            
            # Backup (falls nicht existiert)
            backup = filepath.with_suffix('.html.backup2')
            if not backup.exists():
                with open(backup, 'w', encoding='utf-8') as f:
                    f.write(html)
                print(f"   💾 Backup: {backup.name}")
            
            # Schreibe bereinigte Version
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(cleaned)
            
            print(f"   ✅ Bereinigt")
            return True
        else:
            print(f"   ℹ️  Kein TOC gefunden")
            return False
        
    except Exception as e:
        print(f"   ❌ Fehler: {e}")
        return False


def main():
    print("=" * 70)
    print("🗑️  INHALTSVERZEICHNIS-ENTFERNER")
    print("=" * 70)
    print()
    print("Entfernt 'INHALTSVERZEICHNIS' Boxen AUS dem Artikel-Content")
    print("Die Sidebar-Navigation bleibt erhalten!")
    print()
    
    cwd = Path.cwd()
    print(f"📂 {cwd}")
    print()
    
    # Finde Artikel
    exclude = {'index.html', 'huefte.html', 'hufte.html'}
    files = [f for f in cwd.glob('*.html') 
             if f.name.lower() not in exclude 
             and not f.name.endswith('.backup')
             and not f.name.endswith('.backup2')]
    
    if not files:
        print("❌ Keine Artikel gefunden!")
        return
    
    print(f"📋 {len(files)} Artikel gefunden")
    print()
    
    resp = input("TOC-Boxen aus Artikeln entfernen? (j/n): ")
    if resp.lower() not in ['j', 'ja', 'y', 'yes']:
        print("❌ Abgebrochen")
        return
    
    print()
    print("🔄 Verarbeite Artikel...")
    print()
    
    cleaned = 0
    for f in files:
        if clean_article(f):
            cleaned += 1
    
    print()
    print("=" * 70)
    print(f"✅ {cleaned} Artikel bereinigt")
    print(f"💾 Backups: *.html.backup2")
    print()
    print("🎉 Fertig!")
    print("=" * 70)


if __name__ == "__main__":
    main()
