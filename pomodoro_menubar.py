#!/usr/bin/env python3
"""
Pomodoro Timer - Minimalistyczna aplikacja Menu Bar dla macOS
Wymagania: pip3 install rumps
"""

import rumps
import os
from pathlib import Path


def get_icon_path():
    """Zwraca ścieżkę do ikony"""
    script_dir = Path(__file__).parent
    return str(script_dir / "tomatoTemplate.png")


class PomodoroApp(rumps.App):
    def __init__(self):
        # Ścieżka do ikony
        self.icon_path = get_icon_path()
        self.icon_available = os.path.exists(self.icon_path)
        
        # Inicjalizacja z ikoną lub tekstem
        if self.icon_available:
            super(PomodoroApp, self).__init__("", icon=self.icon_path, template=True, quit_button=None)
        else:
            super(PomodoroApp, self).__init__("●", quit_button=None)
        
        # Domyślne ustawienia czasowe (w minutach)
        self.work_duration = 25
        self.short_break = 5
        self.long_break = 15
        
        # Stan aplikacji
        self.timer = None
        self.time_left = self.work_duration * 60
        self.is_running = False
        self.is_break = False
        self.pomodoros_completed = 0
        
        # Budowanie menu
        self.build_menu()
    
    def build_menu(self):
        """Buduje menu aplikacji"""
        self.menu.clear()
        
        # Status
        self.status_item = rumps.MenuItem(self.get_status_text())
        self.status_item.set_callback(None)
        self.menu.add(self.status_item)
        
        self.menu.add(rumps.separator)
        
        # Kontrolki
        self.start_stop_item = rumps.MenuItem(
            "‖  Pauza" if self.is_running else "▶  Start",
            callback=self.toggle_timer
        )
        self.menu.add(self.start_stop_item)
        
        self.menu.add(rumps.MenuItem("↺  Resetuj", callback=self.reset_timer))
        self.menu.add(rumps.MenuItem("»  Pomiń", callback=self.skip_session))
        
        self.menu.add(rumps.separator)
        
        # Ustawienia czasu pracy
        work_menu = rumps.MenuItem("●  Czas pracy")
        for minutes in [15, 20, 25, 30, 45, 60]:
            item = rumps.MenuItem(
                f"{'✓ ' if self.work_duration == minutes else '   '}{minutes} min",
                callback=self.set_work_duration
            )
            item.minutes = minutes
            work_menu.add(item)
        self.menu.add(work_menu)
        
        # Ustawienia krótkiej przerwy
        short_break_menu = rumps.MenuItem("○  Krótka przerwa")
        for minutes in [3, 5, 10, 15]:
            item = rumps.MenuItem(
                f"{'✓ ' if self.short_break == minutes else '   '}{minutes} min",
                callback=self.set_short_break
            )
            item.minutes = minutes
            short_break_menu.add(item)
        self.menu.add(short_break_menu)
        
        # Ustawienia długiej przerwy
        long_break_menu = rumps.MenuItem("◐  Długa przerwa")
        for minutes in [10, 15, 20, 30]:
            item = rumps.MenuItem(
                f"{'✓ ' if self.long_break == minutes else '   '}{minutes} min",
                callback=self.set_long_break
            )
            item.minutes = minutes
            long_break_menu.add(item)
        self.menu.add(long_break_menu)
        
        self.menu.add(rumps.separator)
        
        # Statystyki
        self.stats_item = rumps.MenuItem(f"◆  Ukończone: {self.pomodoros_completed}")
        self.stats_item.set_callback(None)
        self.menu.add(self.stats_item)
        
        self.menu.add(rumps.separator)
        self.menu.add(rumps.MenuItem("✕  Zamknij", callback=rumps.quit_application))
    
    def get_status_text(self):
        """Zwraca tekst statusu"""
        minutes = self.time_left // 60
        seconds = self.time_left % 60
        
        if self.is_break:
            session_type = "○ Przerwa"
        else:
            session_type = "● Praca"
        
        status = "▶" if self.is_running else "‖"
        return f"{status}  {session_type}  {minutes:02d}:{seconds:02d}"
    
    def update_display(self):
        """Aktualizuje wyświetlacz"""
        minutes = self.time_left // 60
        seconds = self.time_left % 60
        
        # Aktualizuj tytuł w menu bar
        if self.is_running:
            self.title = f"  {minutes:02d}:{seconds:02d}"
        else:
            self.title = ""
        
        # Aktualizuj status w menu
        self.status_item.title = self.get_status_text()
        self.stats_item.title = f"◆  Ukończone: {self.pomodoros_completed}"
    
    def toggle_timer(self, _):
        """Włącza/wyłącza timer"""
        if self.is_running:
            self.pause_timer()
        else:
            self.start_timer()
    
    def start_timer(self):
        """Uruchamia timer"""
        self.is_running = True
        self.start_stop_item.title = "‖  Pauza"
        
        if self.timer:
            self.timer.stop()
        
        self.timer = rumps.Timer(self.tick, 1)
        self.timer.start()
        self.update_display()
    
    def pause_timer(self):
        """Pauzuje timer"""
        self.is_running = False
        self.start_stop_item.title = "▶  Start"
        
        if self.timer:
            self.timer.stop()
        
        self.update_display()
    
    def tick(self, _):
        """Funkcja wywoływana co sekundę"""
        if self.time_left > 0:
            self.time_left -= 1
            self.update_display()
        else:
            self.session_complete()
    
    def session_complete(self):
        """Obsługuje zakończenie sesji"""
        self.timer.stop()
        self.is_running = False
        
        if self.is_break:
            rumps.notification(
                title="Pomodoro",
                subtitle="Przerwa zakończona",
                message="Czas wracać do pracy",
                sound=True
            )
            self.is_break = False
            self.time_left = self.work_duration * 60
        else:
            self.pomodoros_completed += 1
            
            if self.pomodoros_completed % 4 == 0:
                break_time = self.long_break
                break_type = "długą"
            else:
                break_time = self.short_break
                break_type = "krótką"
            
            rumps.notification(
                title="Pomodoro",
                subtitle=f"Sesja #{self.pomodoros_completed} ukończona",
                message=f"Czas na {break_type} przerwę ({break_time} min)",
                sound=True
            )
            self.is_break = True
            self.time_left = break_time * 60
        
        self.build_menu()
        self.update_display()
        self.start_timer()
    
    def reset_timer(self, _):
        """Resetuje timer"""
        if self.timer:
            self.timer.stop()
        
        self.is_running = False
        self.is_break = False
        self.time_left = self.work_duration * 60
        
        self.build_menu()
        self.update_display()
    
    def skip_session(self, _):
        """Pomija bieżącą sesję"""
        self.time_left = 0
        self.session_complete()
    
    def set_work_duration(self, sender):
        """Ustawia czas pracy"""
        self.work_duration = sender.minutes
        if not self.is_break and not self.is_running:
            self.time_left = self.work_duration * 60
        self.build_menu()
        self.update_display()
    
    def set_short_break(self, sender):
        """Ustawia krótką przerwę"""
        self.short_break = sender.minutes
        self.build_menu()
    
    def set_long_break(self, sender):
        """Ustawia długą przerwę"""
        self.long_break = sender.minutes
        self.build_menu()


if __name__ == "__main__":
    app = PomodoroApp()
    app.run()
