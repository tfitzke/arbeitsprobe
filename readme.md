# Arbeitsprobe

## Installationsanweisungen
1. Ich habe mit python 3.7 32bit gearbeitet, falls es bei anderen Versionen Probleme geben sollte 

2. Erstellen Sie sich per Konsole im Projektverzeichnis mit python -m venv [Ordnername] eine virtuelle Umgebung. Diese muss per Konsole auf Windows mit [Ordnername]/Scripts/activate, auf Linux [Ordnername]/bin/activate aktiviert werden.

3. Laden Sie sich mit "pip install -r requirements.txt" alle Module herunter.

4. "python db_create.py" erstellt die sqlite-Datenbank, die für den Server notwendig ist

5. "python arbeitsprobe_server.py" startet den Server

6. Die Website ist unter 127.0.0.1:4000 in den getesteten Browsern (Opera, Firefox, Chrome) verfügbar