# Pomodoro Timer

Minimalistyczna aplikacja Pomodoro w menu bar dla macOS.

## Funkcje

- Ikona pomidora w menu bar
- Konfigurowalne czasy pracy (15, 20, 25, 30, 45, 60 min)
- Konfigurowalne przerwy krótkie (3, 5, 10, 15 min) i długie (10, 15, 20, 30 min)
- Powiadomienia systemowe z dźwiękiem
- Licznik ukończonych sesji
- Autostart przy logowaniu

## Instalacja

1. Pobierz pliki i umieść w wybranym folderze (np. `~/Pomodoro`):
   - `pomodoro_menubar.py`
   - `tomatoTemplate.png`
   - `install_pomodoro.sh`

2. Uruchom instalator:

```bash
cd ~/Pomodoro
chmod +x install_pomodoro.sh
./install_pomodoro.sh
```

**Ważne:** Nie przenoś plików po instalacji - autostart wskazuje na ten folder.

## Autostart

Po instalacji aplikacja uruchamia się automatycznie przy każdym logowaniu.

**Sprawdź status:**
```bash
launchctl list | grep pomodoro
```

**Wyłącz autostart:**
```bash
launchctl unload ~/Library/LaunchAgents/com.user.pomodoro.plist
```

**Włącz autostart:**
```bash
launchctl load ~/Library/LaunchAgents/com.user.pomodoro.plist
```

**Uruchom ręcznie:**
```bash
python3 ~/Pomodoro/pomodoro_menubar.py
```

## Menu

```
▶  Start             - uruchom timer
‖  Pauza             - zatrzymaj timer
↺  Resetuj           - resetuj do początku
»  Pomiń             - pomiń sesję
●  Czas pracy        - ustaw czas pracy
○  Krótka przerwa    - ustaw krótką przerwę
◐  Długa przerwa     - ustaw długą przerwę
◆  Ukończone         - licznik sesji
✕  Zamknij           - zamknij aplikację
```

## Pliki

```
pomodoro_menubar.py  - aplikacja
tomatoTemplate.png   - ikona pomidora
install_pomodoro.sh  - instalator
```

## Odinstalowanie

```bash
launchctl unload ~/Library/LaunchAgents/com.user.pomodoro.plist
rm ~/Library/LaunchAgents/com.user.pomodoro.plist
rm -rf ~/Pomodoro
```

## Wymagania

- macOS 10.14+
- Python 3.6+
- rumps (`pip3 install rumps`)

## Licencja

MIT
