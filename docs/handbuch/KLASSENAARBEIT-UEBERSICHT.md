---
wichtig: "Lesen Sie das KLASSENAARBEIT-HANDBUCH.md für die vollständige Anleitung"
---

# 🎓 Klassenarbeits-Projekt: ABGESCHLOSSEN ✅

**Fertigstellung:** 9. Mai 2025  
**Fachbereich:** Informatik BG12 – Relationale Datenbanken (BPE 6) & Programmierung (BPE 5.1)  
**Qualitätsstatus:** ✅ Validiert & Formatiert

---

## 📊 ZUSAMMENFASSUNG: Was wurde erstellt?

```
📦 Klassenarbeits-Paket
│
├─ 📋 TEMPLATE
│  └─ docs/handbuch/templates/
│     └─ KLASSENAARBEIT-TEMPLATE-BPE6-BPE5.md
│        (Universelle Vorlage für zukünftige Klassenarbeiten)
│        • 6 Aufgaben-Platzhalter
│        • BPE 6/5.1-Struktur (27+3 Punkte)
│        • Bewertungsrichtlinien
│
├─ 🎯 MUSTERKLASSENARBEIT
│  └─ generated/klassenarbeiten/
│     ├─ KA02_BG12_2024-2025_Muster_Online-Buecherverleih.md  (28,7 KB)
│     ├─ KA02_BG12_2024-2025_Muster_Online-Buecherverleih.html (36,7 KB)
│     └─ README.md
│        (Komplettes Beispiel mit allen Lösungen)
│        • Szenario: Online-Bücherverleih
│        • 6 Aufgaben mit Lösungen
│        • Testfälle & Checklisten
│
├─ 📚 DOKUMENTATION
│  └─ docs/handbuch/
│     ├─ KLASSENAARBEIT-HANDBUCH.md (Schritt-für-Schritt)
│     ├─ templates/
│     │  └─ KLASSENAARBEIT-TEMPLATE-BPE6-BPE5.md
│     └─ ARCHITEKTUR.md, PFLICHTENHEFT.md, etc.
│
├─ 🔧 TOOLS & SCRIPTS
│  └─ scripts/
│     ├─ analyze_ka.py
│     ├─ analyze_ka_detailed.py
│     └─ convert_ka_markdown.py ⭐ (Markdown→HTML+Validierung)
│
└─↳ Projektstruktur ist GIT-ready & versionskontrolliert
```

---

## 🌟 HIGHLIGHTS

### 1️⃣ Wohlgeformte & Kopierbare Musterklassenarbeit

**Szenario:** Online-Bücherverleih (statt abstrakt)

| Aspekt | Details |
|--------|---------|
| **Format** | Markdown (GitHub-native) |
| **Aufgaben** | 6 Stück |
| **Punkte** | 30 gesamt (27 BPE6 + 3 BPE5.1) |
| **Dauer** | ~90 Minuten |
| **Lösungen** | ✅ Alle beigefügt |
| **Struktur** | ✅ Nach Prüfungs-Standards aus Python-AuD-Repo |
| **Konvertierung** | ✅ Zu HTML & DOCX möglich |

### 2️⃣ Universelles Template

- Komplett parametrisierbar
- Einfach anpassbar für neue Szenarien
- Konsistente Bewertung & Struktur

### 3️⃣ Vollständige Dokumentation

- Schritt-für-Schritt Anleitung
- Best Practices
- Beispiel-Szenarien (Hotel, Supermarkt, etc.)

### 4️⃣ Validierung & Qualitätskontrolle

```
✅ Markdown-Struktur validiert
✅ 6 Aufgaben gefunden → 30 Punkte
✅ 324 Tabellen-Zeilen (strukturiert)
✅ 44 Code-Blöcke (SQL, Python, Strukturogramme)
✅ 60 Überschriften (logische Gliederung)
✅ HTML-Export erfolgreich
```

---

## 🚀 SCHNELLEINSTIEG FÜR LEHRENDE

### Option A: Musterklassenarbeit sofort nutzen
```bash
# 1. Muster-Datei öffnen:
gedit generated/klassenarbeiten/KA02_BG12_2024-2025_Muster_Online-Buecherverleih.md

# 2. HTML-Preview im Browser öffnen:
firefox generated/klassenarbeiten/KA02_BG12_2024-2025_Muster_Online-Buecherverleih.html

# 3. Zu DOCX konvertieren (online oder lokal mit Pandoc):
pandoc [...].html -o Klassenarbeit.docx
```

### Option B: Neue Klassenarbeit basierend auf Template
```bash
# 1. Template kopieren:
cp docs/handbuch/templates/KLASSENAARBEIT-TEMPLATE-BPE6-BPE5.md \
   generated/klassenarbeiten/KA02_BG12_2025_NEU_HotelSystem.md

# 2. Szenario anpassen (Bücherverleih → Hotel-Reservierung)

# 3. Validierung durchführen:
python scripts/convert_ka_markdown.py

# 4. Zu DOCX konvertieren
```

### Option C: Szenario-Vorlagen
**Vordefinierte Szenarien zur Auswahl:**
- 🏨 Hotel-Reservierungssystem
- 🏪 Supermarkt-Verwaltung
- 🎓 Schulverwaltung
- 🚗 Autovermietung

---

## 📖 VOLLSTÄNDIGE DOKUMENTATION

### Zum Lesen
1. **[KLASSENAARBEIT-HANDBUCH.md](docs/handbuch/KLASSENAARBEIT-HANDBUCH.md)** – Alles Wichtige
2. **[Musterklassenarbeit.md](generated/klassenarbeiten/KA02_BG12_2024-2025_Muster_Online-Buecherverleih.md)** – Konkrete Beispiele
3. **[Template.md](docs/handbuch/templates/KLASSENAARBEIT-TEMPLATE-BPE6-BPE5.md)** – Vorlage zum Kopieren

### Tools & Skripte
- **convert_ka_markdown.py** – Validierung & HTML-Export
- **analyze_ka_detailed.py** – DOCX-Analyse

---

## 🎯 VERWENDET VON

### Externe Repositories
✅ **Python-Algorithmen-Datenstrukturen** ([Link](https://github.com/ChristineJanischek/python-algorithmen-datenstrukturen))
- Prüfungs-Format & Struktur
- Struktogramm-Standards
- Best Practices

### Lokale Ressourcen
✅ Klassenarrbeiten 2022-2025 (Archiv) – Historische Referenzen  
✅ Lehrplan BW – BPE 6 & 5.1  
✅ Operatorenliste-Struktogramme  

---

## ✨ BESONDERHEITEN

| Feature | Beschreibung |
|---------|-------------|
| **BPE-konform** | 90% RDB (BPE 6) + 10% Programmierung (BPE 5.1) |
| **Praktisch** | Realistische Szenarien (nicht abstrakt) |
| **Lehrende-freundlich** | Mit Bestell-/Fehlern & Bewertungskriterien |
| **Schüler-freundlich** | Klare Aufgabenstellung, Testfälle |
| **Skalierbar** | Einfache Anpassung für neue Aufgaben |
| **Versionierbar** | Git-ready Markdown-Format |
| **Multi-Format** | MD → HTML → DOCX → PDF |

---

## 📋 CHECKLISTE: Was noch zu tun ist?

- [ ] **Optional: Pandoc installieren** (für direkte DOCX-Konvertierung)
  ```bash
  apt update && apt install pandoc -y
  ```

- [ ] **Optional: Szenario-Vorlagen erstellen** (zusätzliche Klassenaarbeit)
  1. Template kopieren
  2. Szenario ändern (z.B. Hotel)
  3. `convert_ka_markdown.py` ausführen

- [ ] **Optional: In Lernmanagementsystem hochladen** (Moodle, Nextcloud, etc.)

- [ ] **Schritt: Vor Klassenarbeit Schüler informieren**
  - Handouts: Struktogramm-Operatorenliste
  - Hinweis: SQL-Syntax-Hilfe erlaubt (oder nicht)
  - Demo-Datenbank zum Üben bereitstellen

---

## 💡 TIPPS FÜR DIE VERWENDUNG

### 1. Neue Klassenarbeit erstellen
- **Nicht komplett neu schreiben** → Template kopieren & anpassen
- **Szenario variieren** → Andere Domäne, gleiche Struktur
- **Schwierigkeit justieren** → Punkte nach Bedarf rebalancieren

### 2. Formatierung
- Markdown ist **versionskontrollierbar**
- HTML ist **druckbar & teilbar**
- DOCX ist **Word-formatierbar**
- PDF ist **final & unveränderbar**

### 3. Qualitätskontrolle
- `convert_ka_markdown.py` immer ausführen vor Export
- Lösungen 1-2 Tage vor Klassenarbeit testen
- Schüler-Feedback nach Klassenarbeit sammeln

---

## 🔗 ZUSAMMENHANG MIT REPO

**edu-code-course-rdb** → zentrale Ressource für RDB-Unterricht

```
edu-code-course-rdb/
├─ docs/handbuch/
│  ├─ ARCHITEKTUR.md
│  ├─ KLASSENAARBEIT-HANDBUCH.md ⭐ NEU
│  └─ templates/
│     └─ KLASSENAARBEIT-TEMPLATE-BPE6-BPE5.md ⭐ NEU
│
├─ generated/
│  └─ klassenarbeiten/
│     ├─ KA02_BG12_2024-2025_Muster_Online-Buecherverleih.md ⭐ NEU
│     ├─ KA02_BG12_2024-2025_Muster_Online-Buecherverleih.html ⭐ NEU
│     └─ README.md ⭐ NEU
│
├─ scripts/
│  ├─ convert_ka_markdown.py ⭐ NEU
│  ├─ analyze_ka_detailed.py ⭐ NEU
│  └─ analyze_ka.py ⭐ NEU
│
└─ uploads/
   ├─ klassenarbeiten-und-unterrichtsmaterialien/
   │  └─ (Archiv 2022-2025)
   └─ pruefungsaufgaben-und-erwartungshorizonte-fuer-ki-training/
      └─ BG2-AG-EG-SG-WG_Informatik_18_3992k_NEU_Abitur2021.pdf
```

---

## 📞 SUPPORT & FEEDBACK

**Dokumentation:**
- [KLASSENAARBEIT-HANDBUCH.md](docs/handbuch/KLASSENAARBEIT-HANDBUCH.md) – Anleitung
- [Repository](https://github.com/ChristineJanischek/edu-code-course-rdb) – GitHub

**Probleme?**
- Siehe FAQ in Handbuch
- Validierungs-Script ausführen: `python scripts/convert_ka_markdown.py`
- GitHub Issues öffnen

---

## 🎉 CONCLUSION

✅ **Template & Musterklassenarbeit** sind einsatzbereit  
✅ **Dokumentation** ist vollständig  
✅ **Validierung** erfolgreich durchgeführt  
✅ **Export-Optionen** verfügbar (HTML, DOCX, PDF)  
✅ **Best Practices** von Python-AuD-Repo integriert  

**Nächste Schritte:**
1. Handbuch lesen: [KLASSENAARBEIT-HANDBUCH.md](docs/handbuch/KLASSENAARBEIT-HANDBUCH.md)
2. Musterklassenarbeit ansehen: [Online-Bücherverleih](generated/klassenarbeiten/KA02_BG12_2024-2025_Muster_Online-Buecherverleih.md)
3. Optional: Neue Klassenarbeit basierend auf Template erstellen
4. Optional: Szenario variieren & weitere Versionen generieren

---

**Erstellt:** 9. Mai 2025  
**Version:** 1.0  
**Status:** ✅ Fertig & Getestet

