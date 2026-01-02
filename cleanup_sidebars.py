#!/usr/bin/env python3
"""
Bereinigt Artikel:
1. Löscht alle .backup und .backup2 Dateien
2. Entfernt das 2. <aside class="sidebar"> Element aus jedem Artikel
"""

import re
from pathlib import Path


def remove_second_sidebar(html):
    """Entfernt das 2. <aside class="sidebar"> Element"""
    
    # Finde alle <aside class="sidebar">...</aside> Blöcke
    pattern = r'<aside\s+class=["\']sidebar["\'][^>]*>.*?</aside>'
    matches = list(re.finditer(pattern, html, re.DOTALL | re.IGNORECASE))
    
    if len(matches) < 2:
        # Weniger als 2 Sidebars gefunden
        return html, False
    
    # Entferne das 2. Match (Index 1)
    second_sidebar = matches[1]
    
    # Schneide das 2. Sidebar-Element heraus
    cleaned = html[:second_sidebar.start()] + html[second_sidebar.end():]
    
    return cleaned, True


def clean_article(filepath):
    """Bereinigt einen Artikel"""
    print(f"📄 {filepath.name}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()
        
        # Entferne 2. Sidebar
        cleaned, removed = remove_second_sidebar(html)
        
        if removed:
            print(f"   🗑️  2. Sidebar entfernt")
            
            # Backup erstellen
            backup = filepath.with_suffix('.html.backup')
            with open(backup, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"   💾 Backup erstellt")
            
            # Schreibe bereinigte Version
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(cleaned)
            
            print(f"   ✅ Bereinigt")
            return True
        else:
            print(f"   ℹ️  Keine 2. Sidebar gefunden")
            return False
        
    except Exception as e:
        print(f"   ❌ Fehler: {e}")
        return False


def delete_backups(directory):
    """Löscht alle .backup und .backup2 Dateien"""
    backups = list(directory.glob('*.backup')) + list(directory.glob('*.backup2'))
    
    if not backups:
        print("ℹ️  Keine Backups gefunden")
        return 0
    
    print(f"💾 {len(backups)} Backup-Dateien gefunden:")
    for b in backups:
        print(f"   • {b.name}")
    print()
    
    resp = input("Alle Backups LÖSCHEN? (j/n): ")
    if resp.lower() not in ['j', 'ja', 'y', 'yes']:
        print("❌ Backups nicht gelöscht")
        return 0
    
    deleted = 0
    for backup in backups:
        try:
            backup.unlink()
            deleted += 1
        except Exception as e:
            print(f"   ❌ Fehler beim Löschen {backup.name}: {e}")
    
    print(f"🗑️  {deleted} Backups gelöscht")
    return deleted


def main():
    print("=" * 70)
    print("🔧 ARTIKEL-BEREINIGUNG")
    print("=" * 70)
    print()
    print("1. Löscht alle .backup und .backup2 Dateien")
    print("2. Entfernt 2. <aside class='sidebar'> aus jedem Artikel")
    print()
    
    cwd = Path.cwd()
    print(f"📂 {cwd}")
    print()
    
    # SCHRITT 1: Backups löschen
    print("=" * 70)
    print("SCHRITT 1: Backups löschen")
    print("=" * 70)
    print()
    
    deleted = delete_backups(cwd)
    print()
    
    # SCHRITT 2: Artikel bereinigen
    print("=" * 70)
    print("SCHRITT 2: Artikel bereinigen")
    print("=" * 70)
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
    
    resp = input("2. Sidebar aus allen Artikeln entfernen? (j/n): ")
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
    print("ZUSAMMENFASSUNG")
    print("=" * 70)
    print(f"🗑️  Backups gelöscht: {deleted}")
    print(f"✅ Artikel bereinigt: {cleaned}/{len(files)}")
    print(f"💾 Neue Backups erstellt: {cleaned}")
    print()
    print("🎉 Fertig!")
    print("=" * 70)


if __name__ == "__main__":
    main()
