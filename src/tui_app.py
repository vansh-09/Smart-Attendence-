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
        text-style: bold;
    }
    
    Footer {
        background: $surface;
        color: $text;
        border-top: solid $primary;
    }
    
    .title {
        width: 100%;
        height: auto;
        content-align: center middle;
        background: $primary;
        color: $background;
        text-style: bold;
        padding: 1 2;
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
        margin: 0 1;
        min-width: 20;
    }
    
    Button:focus {
        background: $accent;
        color: $background;
        text-style: bold;
    }
    
    Button.back-btn {
        margin: 0 1;
        width: auto;
    }
    
    Button.primary {
        background: $success;
    }
    
    Button.warning {
        background: $warning;
    }
    
    Button.primary:focus {
        background: $accent;
    }
    
    Button.warning:focus {
        background: $error;
    }
    
    Input {
        border: solid $primary;
        padding: 1;
        margin: 1 0;
        background: $panel;
        color: $text;
    }
    
    Input:focus {
        border: solid $accent;
        background: $accent;
        color: $background;
    }
    
    DataTable {
        border: solid $primary;
        padding: 1;
        height: 1fr;
    }
    
    DataTable > .datatable--cursor {
        background: $accent;
        color: $background;
    }
    
    Label {
        margin: 0 1;
        color: $text;
    }
    
    Static {
        color: $text;
    }
    
    OptionList {
        border: solid $primary;
        background: $panel;
        padding: 1;
    }
    
    OptionList:focus {
        border: solid $accent;
    }
    
    .welcome-title {
        width: 100%;
        content-align: center middle;
        background: $primary;
        color: $background;
        text-style: bold;
        padding: 2 1;
        margin-bottom: 1;
        border-bottom: solid $accent;
    }
    
    .stat-box {
        width: 1fr;
        height: auto;
        border: round $primary;
        background: $panel;
        padding: 1;
        margin: 0 1;
    }
    
    .stat-box:focus {
        border: round $accent;
        background: $accent;
        color: $background;
    }
    
    .info-box {
        border: round $primary;
        background: $panel;
        padding: 1;
        margin: 1 0;
    }
    
    .action-buttons {
        height: auto;
        background: $panel;
        border: solid $primary;
        padding: 1;
        margin: 1 0;
    }
    
    .form-group {
        height: auto;
        margin: 1 0;
        padding: 1;
        border-left: solid $accent;
        background: $panel;
    }
    
    .settings-panel {
        width: 100%;
        height: auto;
        border: solid $primary;
        background: $panel;
        padding: 1;
        margin: 1 0;
    }
    """
    
    BINDINGS = [
        ("q", "quit", "Quit"),
    ]
    
    def on_mount(self) -> None:
        """Called when app starts."""
        # Use a nice theme
        self.theme = "nord"
        self.push_screen(WelcomeScreen())


def main() -> None:
    """Run the application."""
    app = SmartAttendanceApp()
    app.run()


if __name__ == "__main__":
    main()
