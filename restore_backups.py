#!/usr/bin/env python3
"""
Backup-Restore Script
Stellt alle .html.backup Dateien wieder her
"""

from pathlib import Path
import shutil

def restore_backups():
    """Stellt alle Backups wieder her"""
    print("=" * 70)
    print("🔄 Backup-Restore Tool")
    print("=" * 70)
    print()
    
    current_dir = Path.cwd()
    print(f"📂 Arbeitsverzeichnis: {current_dir}")
    print()
    
    # Finde alle Backup-Dateien
    backup_files = list(current_dir.glob('*.html.backup'))
    
    if not backup_files:
        print("❌ Keine Backup-Dateien gefunden!")
        return
    
    print(f"💾 Gefundene Backups: {len(backup_files)}")
    print()
    
    # Zeige Liste der Backups
    print("📋 Folgende Dateien werden wiederhergestellt:")
    for backup in backup_files:
        original_name = backup.stem  # Dateiname ohne .backup
        print(f"   • {backup.name} → {original_name}")
    print()
    
    # Bestätigung
    print("⚠️  WARNUNG:")
    print("   • Die aktuellen HTML-Dateien werden ÜBERSCHRIEBEN!")
    print("   • Die Backups bleiben erhalten")
    print()
    
    response = input("Möchten Sie fortfahren? (j/n): ")
    if response.lower() not in ['j', 'ja', 'y', 'yes']:
        print("❌ Abgebrochen.")
        return
    
    print()
    print("=" * 70)
    print("🔄 Stelle Backups wieder her...")
    print("=" * 70)
    print()
    
    # Restore jede Backup-Datei
    success_count = 0
    for backup in backup_files:
        try:
            # Original-Dateiname (ohne .backup)
            original_file = backup.parent / backup.stem
            
            # Kopiere Backup zur Original-Datei
            shutil.copy2(backup, original_file)
            
            print(f"✅ Wiederhergestellt: {original_file.name}")
            success_count += 1
            
        except Exception as e:
            print(f"❌ Fehler bei {backup.name}: {e}")
    
    print()
    print("=" * 70)
    print(f"✅ Erfolgreich wiederhergestellt: {success_count}/{len(backup_files)}")
    print(f"💾 Backups bleiben erhalten (.html.backup)")
    print()
    print("🎉 Fertig!")
    print("=" * 70)


if __name__ == "__main__":
    restore_backups()
