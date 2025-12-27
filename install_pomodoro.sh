#!/bin/bash

# Pomodoro Timer - Instalator

echo "Pomodoro Timer - Instalator"
echo "==========================="
echo ""

# Sprawdź Python3
if ! command -v python3 &> /dev/null; then
    echo "[x] Python3 nie jest zainstalowany"
    echo "    Zainstaluj: brew install python3"
    exit 1
fi

PYTHON_PATH=$(which python3)
echo "[ok] Python3: $PYTHON_PATH"

# Zainstaluj rumps
echo ""
echo "[..] Instaluję bibliotekę rumps..."
pip3 install rumps

if [ $? -ne 0 ]; then
    echo "[x] Błąd instalacji rumps"
    exit 1
fi
echo "[ok] Biblioteka rumps zainstalowana"

# Ścieżki
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLIST_PATH="$HOME/Library/LaunchAgents/com.user.pomodoro.plist"

echo "[ok] Folder aplikacji: $SCRIPT_DIR"

# Sprawdź czy pliki istnieją
if [ ! -f "$SCRIPT_DIR/pomodoro_menubar.py" ]; then
    echo "[x] Nie znaleziono pliku pomodoro_menubar.py"
    exit 1
fi

if [ ! -f "$SCRIPT_DIR/tomatoTemplate.png" ]; then
    echo "[!] Brak ikony tomatoTemplate.png - aplikacja użyje domyślnej"
fi

# Utwórz folder LaunchAgents jeśli nie istnieje
mkdir -p "$HOME/Library/LaunchAgents"

# Utwórz plist
cat > "$PLIST_PATH" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.user.pomodoro</string>
    <key>ProgramArguments</key>
    <array>
        <string>$PYTHON_PATH</string>
        <string>$SCRIPT_DIR/pomodoro_menubar.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>WorkingDirectory</key>
    <string>$SCRIPT_DIR</string>
    <key>StandardOutPath</key>
    <string>/tmp/pomodoro.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/pomodoro.error.log</string>
</dict>
</plist>
EOF

echo "[ok] Utworzono plik autostartu"

# Załaduj Launch Agent
launchctl unload "$PLIST_PATH" 2>/dev/null
launchctl load "$PLIST_PATH"

if [ $? -eq 0 ]; then
    echo "[ok] Autostart włączony"
else
    echo "[!] Nie udało się włączyć autostartu"
fi

echo ""
echo "==========================="
echo "[ok] INSTALACJA ZAKOŃCZONA"
echo "==========================="
echo ""
echo "Pliki aplikacji: $SCRIPT_DIR"
echo ""
echo "Aplikacja uruchomi się automatycznie przy logowaniu."
echo "NIE PRZENOŚ plików do innego folderu!"
echo ""
echo "Uruchamiam teraz..."
echo ""

# Uruchom aplikację
cd "$SCRIPT_DIR"
python3 pomodoro_menubar.py &

echo "[ok] Sprawdź menu bar"
echo ""
echo "---"
echo "Wyłącz autostart:  launchctl unload ~/Library/LaunchAgents/com.user.pomodoro.plist"
echo "Włącz autostart:   launchctl load ~/Library/LaunchAgents/com.user.pomodoro.plist"
