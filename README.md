# Orthopedic Knowledge Base - Projekt-Dokumentation

## 📋 Überblick

Dieses Projekt ist eine **evidenzbasierte Wissenssammlung** zur Hüftendoprothetik mit einer übersichtlichen Web-Oberfläche.

**Struktur:**
- Hauptseite (index.html)
- Kategorieübersicht (huefte.html)
- Einzelne Fachartikel (~30+ HTML-Dateien)

---

## 🗂️ Dateistruktur

```
projekt-ordner/
├── index.html                    # Hauptseite mit Body-Diagram
├── huefte.html                   # Kategorien-Übersicht (6 Rubriken)
├── styles.css                    # Haupt-Stylesheet
├── allgemeineinfos.html         # Artikel-Beispiel
├── adipositas.html              # Artikel-Beispiel
├── [weitere ~30 Artikel]
├── ultra_minimal.py             # Haupt-Konvertierungs-Script
├── restore_backups.py           # Backup-Wiederherstellung
└── README.md                    # Diese Datei
```

---

## 🎯 Website-Navigation

### **Ebene 1: Hauptseite (index.html)**
- Gradient Hero-Section
- Interaktives SVG Body-Diagram
- Region-Karten (nur "Hüfte" aktiv)
- Link zu: huefte.html

### **Ebene 2: Kategorien (huefte.html)**
6 Kategorien in 2-Spalten-Layout:
- 📐 Grundlagen & Parameter (4 Artikel)
- 🔬 Diagnostik (3 Artikel)
- ⚕️ Therapie (8 Artikel)
- 🤖 Robotik & Navigation (6 Artikel)
- ⚡ Spezialfälle (7 Artikel)
- 🔩 Implantate (4 Artikel)

### **Ebene 3: Einzelartikel**
Jeder Artikel hat:
- Navigation links (Sidebar mit Abschnitten)
- Content rechts (mit Breadcrumbs + Zurück-Link)
- Minimales, übersichtliches Design

---

## 🛠️ Python-Scripts

### **ultra_minimal.py** (Haupt-Script)

**Zweck:** Konvertiert alle Artikel in einheitliches, minimales Design

**Features:**
- Löscht alte Backups (.backup, .backup2)
- Erstellt neue Backups vor Änderungen
- Extrahiert H2-Überschriften automatisch
- Generiert Navigation-Sidebar
- Ultra-minimales Design
- Behält Breadcrumbs + "Zurück"-Link im Content

**Verwendung:**
```bash
python3 ultra_minimal.py
```

**Ablauf:**
1. Fragt: "Backups löschen?" → `j` oder `n`
2. Findet alle Artikel (außer index.html, huefte.html)
3. Fragt: "Konvertieren?" → `j`
4. Konvertiert jeden Artikel
5. Erstellt neue .backup Dateien

**Was das Script macht:**
- ✅ Erstellt Navigation aus H2-Überschriften
- ✅ Fügt IDs zu H2-Überschriften hinzu (für Anchor-Links)
- ✅ Minimales Design (keine unnötigen Elemente)
- ✅ Responsive Layout (funktioniert auf Mobile)
- ✅ Sticky Navigation (bleibt beim Scrollen sichtbar)

**Was das Script NICHT ändert:**
- ❌ index.html
- ❌ huefte.html
- ❌ styles.css
- ❌ Backup-Dateien (.backup)

---

### **restore_backups.py**

**Zweck:** Stellt alle Backup-Dateien wieder her

**Verwendung:**
```bash
python3 restore_backups.py
```

**Was es tut:**
- Findet alle .html.backup Dateien
- Zeigt Liste der Backups
- Kopiert .backup zurück zu .html
- Überschreibt aktuelle Dateien

**Wichtig:** Backups bleiben nach Restore erhalten!

---

## 📐 Artikel-Zuordnung

### Grundlagen & Parameter (4 Artikel)
- allgemeineinfos.html
- funktionellesafezoneundkinematischesalignment.html
- altersabhaengigeveraenderungen.html
- enthnischeunterschiede.html

### Diagnostik (3 Artikel)
- klassifikation.html
- radiologischemessungendirektewinkel.html
- radiologischemessungenindikretewinkel.html

### Therapie (8 Artikel)
- implantatpositionierung.html
- weichteilmanagement.html
- zugangswege.html
- instabilitaetundluxation.html
- kniealskompensator.html
- muskulaeresbalancingundabduktorenfunktion.html
- postoperativekomplikationen.html
- traumaundinfektionen.html

### Robotik & Navigation (6 Artikel)
- robotikallgemein.html
- cori.html
- mako.html
- rosa.html
- velys.html
- intraoperativestrategienundnavigation.html

### Spezialfälle (7 Artikel)
- adipositas.html
- rheuma.html
- lwsfusion.html
- geriatrischepatient.html
- hueftdysplasie.html
- revisionen.html
- beinlaengendifferenz.html

### Implantate (4 Artikel)
- dualmobilityeins.html
- dualmobilityzewi.html
- dualmobilitydrei.html
- femurschaft.html

---

## 🎨 Design-Prinzipien

### Minimal & Übersichtlich
- Weiß/Grau/Schwarz Farbschema
- Keine unnötigen Dekorationen
- Fokus auf Lesbarkeit
- Klare Hierarchie

### Responsive
- Funktioniert auf Desktop, Tablet, Mobile
- Navigation wird auf Mobile zu Akkordeon

### Navigation
- Sidebar links (250px, sticky)
- Zeigt bis zu 10 Abschnitte
- Aktiver Abschnitt wird gehighlightet
- Smooth Scrolling zu Abschnitten

---

## 🔧 Häufige Aufgaben

### Neuen Artikel hinzufügen
1. HTML-Datei in Hauptordner legen
2. `python3 ultra_minimal.py` ausführen
3. Artikel-Link zu huefte.html hinzufügen

### Artikel-Link zu huefte.html hinzufügen
1. Öffne `huefte.html` in Editor
2. Finde die richtige Kategorie
3. Füge hinzu:
```html
<a href="dateiname.html" class="article-link">
    <span class="article-name">Titel des Artikels</span>
    <span class="article-arrow">→</span>
</a>
```
4. Aktualisiere `article-count-badge` (+1)

### Design aller Artikel ändern
1. Bearbeite `ultra_minimal.py`
2. Ändere das `MINIMAL_TEMPLATE`
3. Führe Script aus: `python3 ultra_minimal.py`

### Backups wiederherstellen
```bash
python3 restore_backups.py
```

### Alle Backups löschen
```bash
rm *.backup *.backup2
```

---

## ⚠️ Wichtige Hinweise

### Browser-Cache
**Problem:** Änderungen werden nicht angezeigt

**Lösung:**
- **Chrome/Safari:** `Cmd + Shift + R` (Hard Refresh)
- **Firefox:** `Cmd + Shift + R`
- Oder: Browser-Cache komplett löschen

### Backup-Strategie
- Scripts erstellen automatisch .backup Dateien
- Backups werden NICHT überschrieben
- Alte Backups können gelöscht werden
- Empfehlung: Zusätzliches externes Backup

### Dateinamen
- Keine Leerzeichen in Dateinamen!
- Kleinschreibung empfohlen
- Umlaute vermeiden (ä→ae, ö→oe, ü→ue)

### Python-Version
- Benötigt: Python 3.6+
- Keine externen Dependencies
- Standard-Library only

---

## 🐛 Troubleshooting

### "Keine Artikel gefunden"
**Ursache:** Script läuft im falschen Ordner

**Lösung:**
```bash
cd /pfad/zum/ordner
python3 ultra_minimal.py
```

### Layout ist "zerschossen"
**Ursache:** Alte/fehlerhafte HTML-Struktur

**Lösung:**
1. Backups wiederherstellen: `python3 restore_backups.py`
2. Script erneut ausführen: `python3 ultra_minimal.py`

### Navigation fehlt
**Ursache:** Keine H2-Überschriften im Artikel

**Lösung:**
- Artikel muss H2-Überschriften haben
- Mindestens eine `<h2>Überschrift</h2>`

### Breadcrumbs fehlen
**Ursache:** Script hat Content-Extraktion falsch gemacht

**Lösung:**
- Backup wiederherstellen
- Script erneut ausführen

### Links funktionieren nicht
**Ursache:** Dateiname in huefte.html stimmt nicht mit echtem Dateinamen überein

**Lösung:**
1. Prüfe echten Dateinamen im Ordner
2. Korrigiere in huefte.html
3. Dateinamen müssen exakt übereinstimmen (inkl. Groß-/Kleinschreibung)

---

## 📝 Entwicklungs-Notizen

### Version History
- **v1.0** - Initial Setup mit komplexem Design
- **v2.0** - Vereinfachung, Sidebar-Navigation
- **v3.0** - Ultra-minimal Design, keine doppelten Header
- **v4.0** (aktuell) - Finale Version mit perfekter Navigation

### Design-Entscheidungen
- **Warum ultra-minimal?** → Fokus auf Inhalt, nicht Design
- **Warum Sidebar links?** → Bessere Übersicht, sticky navigation
- **Warum keine fancy Farben?** → Professionell, medizinisch, seriös

### Bekannte Einschränkungen
- Nur eine Region (Hüfte) aktiv
- Keine Suchfunktion
- Keine Benutzerkonten
- Statische HTML-Dateien (kein CMS)

---

## 🚀 Zukünftige Erweiterungen (Optional)

### Mögliche Features
- [ ] Suchfunktion über alle Artikel
- [ ] Weitere Regionen (Knie, Schulter, etc.)
- [ ] PDF-Export von Artikeln
- [ ] Druckansicht
- [ ] Dark Mode
- [ ] Bookmarks/Favoriten
- [ ] Artikel-Versionen/Changelog

### Technische Verbesserungen
- [ ] Static Site Generator (Jekyll, Hugo)
- [ ] Markdown statt HTML für Artikel
- [ ] Automatische TOC-Generierung
- [ ] Build-System mit CI/CD
- [ ] SEO-Optimierung

---

## 📞 Support

Bei Fragen oder Problemen:
1. Diese README durchlesen
2. Troubleshooting-Section prüfen
3. Backups wiederherstellen und neu versuchen

---

## 📜 Lizenz

Dieses Projekt ist für interne/akademische Zwecke.

---

**Letzte Aktualisierung:** 31. Dezember 2024
**Version:** 4.0
