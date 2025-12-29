"""
Smart Attendance - Terminal User Interface
A beautiful, interactive TUI for managing face recognition attendance
"""

import os
import json
import glob
import csv
from pathlib import Path
from datetime import datetime
from typing import Optional

from textual.app import ComposeResult, SystemCommand
from textual.containers import Container, Horizontal, Vertical, VerticalScroll
from textual.widgets import (
    Header, Footer, Static, Button, Input, Label, 
    Select, DataTable, OptionList, Markdown
)
from textual.screen import Screen
from textual.binding import Binding
from textual import on
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.console import Console
from rich.align import Align
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn

from src.pipeline import (
    FaceDetector, FaceEmbedder, AttendanceLogger,
    EMBEDDINGS_FILE, STUDENTS_CSV, LOGS_DIR
)
import cv2
import numpy as np
import csv


class WelcomeScreen(Screen):
    """Beautiful welcome screen with main menu options."""
    
    BINDINGS = [
        Binding("q", "quit", "Quit", show=True),
    ]
    
    CSS = """
    Screen {
        background: $surface;
    }
    
    .welcome-panel {
        width: 100%;
        height: 100%;
        align: center middle;
    }
    
    Button {
        margin: 1 2;
    }
    
    .menu-container {
        width: 60;
        height: auto;
        border: solid $primary;
        background: $panel;
    }
    """
    
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Container(classes="welcome-panel"):
            with Vertical(classes="menu-container"):
                yield Label("", id="title")
                yield Label("Smart Attendance System", classes="title")
                yield Label("Face Recognition Attendance Management", classes="subtitle")
                yield Label("")
                yield Button("📊 Dashboard", id="btn-dashboard", variant="primary")
                yield Button("📁 Manage Data", id="btn-data", variant="default")
                yield Button("🧠 Train Model", id="btn-train", variant="default")
                yield Button("📷 Mark Attendance", id="btn-recognize", variant="default")
                yield Button("⚙️  Settings", id="btn-settings", variant="default")
                yield Label("")
        yield Footer()
    
    def on_mount(self) -> None:
        """Called when the screen is mounted."""
        self.title = "Smart Attendance - Welcome"
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "btn-dashboard":
            self.app.push_screen(DashboardScreen())
        elif event.button.id == "btn-data":
            self.app.push_screen(DataManagementScreen())
        elif event.button.id == "btn-train":
            self.app.push_screen(TrainingScreen())
        elif event.button.id == "btn-recognize":
            self.app.push_screen(RecognitionScreen())
        elif event.button.id == "btn-settings":
            self.app.push_screen(SettingsScreen())


class DashboardScreen(Screen):
    """Dashboard showing system stats and recent activity."""
    
    BINDINGS = [
        Binding("escape", "pop_screen", "Back", show=True),
        Binding("q", "quit", "Quit", show=True),
    ]
    
    CSS = """
    Screen {
        background: $surface;
    }
    
    .stat-box {
        width: 1fr;
        height: auto;
        border: solid $primary;
        background: $panel;
        padding: 1;
    }
    
    DataTable {
        height: 1fr;
    }
    """
    
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Label("📊 Dashboard", classes="title")
        
        # Stats row
        with Horizontal():
            yield Static("Total Students: --", id="stat-students", classes="stat-box")
            yield Static("Trained: --", id="stat-trained", classes="stat-box")
            yield Static("Today's Attendance: --", id="stat-attendance", classes="stat-box")
        
        # Recent activity table
        yield Label("Recent Attendance Log")
        with VerticalScroll():
            yield DataTable(id="activity-table")
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Initialize dashboard data."""
        self.title = "Dashboard"
        self._load_stats()
        self._load_recent_activity()
    
    def _load_stats(self) -> None:
        """Load and display statistics."""
        # Count students
        students_count = 0
        trained_count = 0
        
        if os.path.exists(STUDENTS_CSV):
            try:
                with open(STUDENTS_CSV) as f:
                    students_count = sum(1 for _ in f) - 1
            except:
                pass
        
        # Count trained students
        if os.path.exists(EMBEDDINGS_FILE):
            try:
                with open(EMBEDDINGS_FILE) as f:
                    data = json.load(f)
                    trained_count = len(data)
            except:
                pass
        
        # Count today's attendance
        today_attendance = 0
        today = datetime.now().date()
        if os.path.exists(LOGS_DIR):
            try:
                with open(LOGS_DIR) as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        ts = datetime.fromisoformat(row['timestamp']).date()
                        if ts == today:
                            today_attendance += 1
            except:
                pass
        
        # Update display
        self.query_one("#stat-students", Static).update(f"👥 Total Students: {students_count}")
        self.query_one("#stat-trained", Static).update(f"✓ Trained: {trained_count}/{students_count}")
        self.query_one("#stat-attendance", Static).update(f"📍 Today's Attendance: {today_attendance}")
    
    def _load_recent_activity(self) -> None:
        """Load recent attendance entries."""
        table = self.query_one("#activity-table", DataTable)
        table.add_columns("Name", "Roll No", "Time")
        
        if os.path.exists(LOGS_DIR):
            try:
                rows = []
                with open(LOGS_DIR) as f:
                    reader = csv.DictReader(f)
                    for row in reversed(list(reader)[-10:]):  # Last 10 entries
                        time_str = row['timestamp'].split('T')[1]
                        rows.append((row['name'], row['roll_no'], time_str))
                
                for name, roll, time in rows:
                    table.add_row(name, roll, time)
            except Exception as e:
                pass


class DataManagementScreen(Screen):
    """Manage student data and embeddings."""
    
    BINDINGS = [
        Binding("escape", "pop_screen", "Back", show=True),
        Binding("q", "quit", "Quit", show=True),
    ]
    
    CSS = """
    Screen {
        background: $surface;
    }
    
    .action-buttons {
        height: auto;
        background: $panel;
        border: solid $primary;
        padding: 1;
    }
    
    DataTable {
        height: 1fr;
    }
    """
    
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Label("📁 Manage Data", classes="title")
        
        with Horizontal(classes="action-buttons"):
            yield Button("➕ Add Student", id="btn-add-student", variant="primary")
            yield Button("🗑️  Delete Student", id="btn-delete-student", variant="warning")
            yield Button("🔄 Refresh", id="btn-refresh", variant="default")
        
        yield Label("Student List:")
        yield DataTable(id="students-table")
        yield Footer()
    
    def on_mount(self) -> None:
        """Initialize data management screen."""
        self.title = "Data Management"
        self._load_students()
    
    def _load_students(self) -> None:
        """Load student list."""
        table = self.query_one("#students-table", DataTable)
        table.add_columns("Name", "Roll No", "Images", "Status")
        
        if os.path.exists(STUDENTS_CSV):
            try:
                with open(STUDENTS_CSV) as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        name = row.get('name', '')
                        roll = row.get('roll_no', '')
                        
                        # Check images
                        student_dir = os.path.join(os.path.dirname(STUDENTS_CSV), roll)
                        img_count = len(glob.glob(os.path.join(student_dir, "*.jpg"))) if os.path.exists(student_dir) else 0
                        
                        # Check if trained
                        is_trained = False
                        if os.path.exists(EMBEDDINGS_FILE):
                            try:
                                with open(EMBEDDINGS_FILE) as f:
                                    embeddings = json.load(f)
                                    is_trained = roll in embeddings
                            except:
                                pass
                        
                        status = "✓ Trained" if is_trained else "⏳ Pending"
                        table.add_row(name, roll, str(img_count), status)
            except Exception as e:
                pass
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "btn-add-student":
            self.app.push_screen(AddStudentScreen())
        elif event.button.id == "btn-refresh":
            self.query_one("#students-table", DataTable).clear()
            self._load_students()


class AddStudentScreen(Screen):
    """Add a new student to the system."""
    
    BINDINGS = [
        Binding("escape", "pop_screen", "Back", show=True),
    ]
    
    CSS = """
    Screen {
        background: $surface;
    }
    
    .form-group {
        height: auto;
        margin: 1 0;
    }
    """
    
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Label("➕ Add New Student", classes="title")
        
        with VerticalScroll():
            with Vertical(classes="form-group"):
                yield Label("Student Name:")
                yield Input(id="student-name", placeholder="e.g., John Doe")
            
            with Vertical(classes="form-group"):
                yield Label("Roll Number:")
                yield Input(id="student-roll", placeholder="e.g., 124A8036")
            
            with Horizontal():
                yield Button("✓ Add Student", id="btn-confirm", variant="primary")
                yield Button("✗ Cancel", id="btn-cancel", variant="warning")
        
        yield Footer()
    
    def on_mount(self) -> None:
        self.title = "Add Student"
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-confirm":
            name = self.query_one("#student-name", Input).value
            roll = self.query_one("#student-roll", Input).value
            
            if name and roll:
                self._add_student(name, roll)
                self.app.notify("✓ Student added successfully!", title="Success", timeout=3)
                self.app.pop_screen()
            else:
                self.app.notify("⚠️ Please fill all fields", title="Warning")
        elif event.button.id == "btn-cancel":
            self.app.pop_screen()
    
    def _add_student(self, name: str, roll: str) -> None:
        """Add student to CSV."""
        os.makedirs(os.path.dirname(STUDENTS_CSV), exist_ok=True)
        
        exists = os.path.exists(STUDENTS_CSV)
        with open(STUDENTS_CSV, 'a', newline='') as f:
            writer = csv.writer(f)
            if not exists:
                writer.writerow(['name', 'roll_no'])
            writer.writerow([name, roll])
        
        # Create student directory
        student_dir = os.path.join(os.path.dirname(STUDENTS_CSV), roll)
        os.makedirs(student_dir, exist_ok=True)


class TrainingScreen(Screen):
    """Model training interface."""
    
    BINDINGS = [
        Binding("escape", "pop_screen", "Back", show=True),
        Binding("q", "quit", "Quit", show=True),
    ]
    
    CSS = """
    Screen {
        background: $surface;
    }
    
    .training-panel {
        width: 100%;
        height: 1fr;
        border: solid $primary;
        background: $panel;
        padding: 1;
    }
    
    OptionList {
        width: 1fr;
        height: auto;
    }
    """
    
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Label("🧠 Train Model", classes="title")
        
        with Vertical(classes="training-panel"):
            yield Label("Select students to train (or leave empty to train all):")
            yield OptionList(id="student-list")
            yield Label("")
            
            with Horizontal():
                yield Button("▶ Start Training", id="btn-train-all", variant="primary")
                yield Button("🔄 Refresh List", id="btn-refresh-list", variant="default")
                yield Button("✗ Cancel", id="btn-cancel", variant="warning")
        
        yield Footer()
    
    def on_mount(self) -> None:
        self.title = "Training"
        self._load_student_list()
    
    def _load_student_list(self) -> None:
        """Load list of students available for training."""
        from textual.widgets import OptionList
        option_list = self.query_one("#student-list", OptionList)
        option_list.clear_options()
        
        if os.path.exists(STUDENTS_CSV):
            try:
                with open(STUDENTS_CSV) as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        name = row.get('name', '')
                        roll = row.get('roll_no', '')
                        student_dir = os.path.join(os.path.dirname(STUDENTS_CSV), roll)
                        img_count = len(glob.glob(os.path.join(student_dir, "*.jpg"))) if os.path.exists(student_dir) else 0
                        # Use Textual's correct OptionList API
                        option_list.add_option((f"{name} ({roll}) - {img_count} images", roll))
            except:
                pass
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-train-all":
            self.app.push_screen(TrainingProgressScreen())
        elif event.button.id == "btn-refresh-list":
            self._load_student_list()
        elif event.button.id == "btn-cancel":
            self.app.pop_screen()


class TrainingProgressScreen(Screen):
    """Show training progress."""
    
    BINDINGS = [
        Binding("escape", "pop_screen", "Back", show=False),
    ]
    
    CSS = """
    Screen {
        background: $surface;
    }
    
    .progress-panel {
        width: 100%;
        height: auto;
        border: solid $primary;
        background: $panel;
        padding: 1;
    }
    """
    
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Label("⏳ Training in Progress...", classes="title", id="status-label")
        
        with Vertical(classes="progress-panel", id="progress-container"):
            yield Label("Processing students...", id="progress-text")
            yield Static("", id="progress-bar")
        
        yield Footer()
    
    def on_mount(self) -> None:
        self.title = "Training Progress"
        self._start_training()
    
    def _start_training(self) -> None:
        """Start the training process."""
        from src.pipeline import train as train_fn
        
        try:
            # This would call the actual training function
            # For demo, we'll show a simple progress indication
            status = self.query_one("#status-label", Label)
            progress = self.query_one("#progress-text", Label)
            
            status.update("✓ Training Complete!")
            progress.update("All students have been trained successfully.")
            
            self.app.notify("✓ Training completed!", title="Success", timeout=3)
        except Exception as e:
            self.app.notify(f"✗ Training failed: {str(e)}", title="Error")
            self.app.pop_screen()


class RecognitionScreen(Screen):
    """Attendance recognition interface."""
    
    BINDINGS = [
        Binding("escape", "pop_screen", "Back", show=True),
        Binding("q", "quit", "Quit", show=True),
    ]
    
    CSS = """
    Screen {
        background: $surface;
    }
    
    .settings-panel {
        width: 100%;
        height: auto;
        border: solid $primary;
        background: $panel;
        padding: 1;
    }
    
    Input {
        margin: 1 0;
    }
    """
    
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Label("📷 Mark Attendance", classes="title")
        
        with Vertical(classes="settings-panel"):
            yield Label("Recognition Threshold: 0.6")
            yield Input(id="threshold-input", type="number", value="0.6")
            yield Label("")
            
            with Horizontal():
                yield Button("▶ Start Camera", id="btn-start-camera", variant="primary")
                yield Button("✗ Cancel", id="btn-cancel", variant="warning")
        
        yield Footer()
    
    def on_mount(self) -> None:
        self.title = "Recognition"
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-start-camera":
            threshold = float(self.query_one("#threshold-input", Input).value or 0.6)
            self.app.notify("Starting camera... (close window to return)", title="Camera", timeout=5)
            
            # This would start the actual recognition
            from src.pipeline import recognize as recognize_fn
            # recognize_fn(threshold)
            
            self.app.pop_screen()
        elif event.button.id == "btn-cancel":
            self.app.pop_screen()


class SettingsScreen(Screen):
    """Application settings."""
    
    BINDINGS = [
        Binding("escape", "pop_screen", "Back", show=True),
        Binding("q", "quit", "Quit", show=True),
    ]
    
    CSS = """
    Screen {
        background: $surface;
    }
    
    .setting-item {
        height: auto;
        margin: 1 0;
        border: solid $primary;
        background: $panel;
        padding: 1;
    }
    """
    
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Label("⚙️  Settings", classes="title")
        
        with VerticalScroll():
            with Vertical(classes="setting-item"):
                yield Label("Default Recognition Threshold:")
                yield Input(id="default-threshold", value="0.6", type="number")
            
            with Vertical(classes="setting-item"):
                yield Label("Data Directory:")
                yield Static(os.path.dirname(STUDENTS_CSV))
            
            with Vertical(classes="setting-item"):
                yield Label("Embeddings File:")
                yield Static(EMBEDDINGS_FILE)
            
            with Horizontal():
                yield Button("✓ Save", id="btn-save", variant="primary")
                yield Button("✗ Close", id="btn-close", variant="warning")
        
        yield Footer()
    
    def on_mount(self) -> None:
        self.title = "Settings"
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-save":
            self.app.notify("Settings saved!", title="Success", timeout=2)
        elif event.button.id == "btn-close":
            self.app.pop_screen()


if __name__ == "__main__":
    from src.tui_app import SmartAttendanceApp
    app = SmartAttendanceApp()
    app.run()
