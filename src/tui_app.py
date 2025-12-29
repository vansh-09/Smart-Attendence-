"""
Smart Attendance TUI Application
Main application entry point
"""

from textual.app import ComposeResult, App
from textual.containers import Container
from textual.widgets import Header, Footer
from src.tui import WelcomeScreen


class SmartAttendanceApp(App):
    """The Smart Attendance Terminal User Interface Application."""
    
    TITLE = "Smart Attendance System"
    SUB_TITLE = "Face Recognition Attendance Management"
    
    CSS = """
    Screen {
        background: $surface;
        color: $text;
    }
    
    Header {
        background: $primary;
        color: $background;
    }
    
    Footer {
        background: $surface;
        color: $text;
    }
    
    .title {
        width: 100%;
        height: auto;
        content-align: center middle;
        background: $primary;
        color: $background;
        text-style: bold;
        padding: 1;
        margin-bottom: 1;
    }
    
    .subtitle {
        width: 100%;
        height: auto;
        content-align: center middle;
        color: $accent;
        text-style: italic;
        margin: 1 0;
    }
    
    Button {
        margin: 1;
        width: 1fr;
    }
    
    Button:hover {
        background: $accent;
        color: $background;
    }
    
    Input {
        border: solid $primary;
        padding: 1;
        margin: 1 0;
    }
    
    DataTable {
        border: solid $primary;
        padding: 1;
        height: 100%;
    }
    
    Label {
        margin: 0 1;
    }
    """
    
    BINDINGS = [
        ("q", "quit", "Quit"),
    ]
    
    def on_mount(self) -> None:
        """Called when app starts."""
        # Use default theme with custom CSS styling
        self.theme = "nord"
        self.push_screen(WelcomeScreen())


def main() -> None:
    """Run the application."""
    app = SmartAttendanceApp()
    app.run()


if __name__ == "__main__":
    main()
