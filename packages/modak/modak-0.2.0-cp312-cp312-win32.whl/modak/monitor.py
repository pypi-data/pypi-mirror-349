from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import ClassVar

import click
import tzlocal
from rich.text import Text
from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, ScrollableContainer
from textual.reactive import reactive
from textual.widgets import (
    DataTable,
    Footer,
    Header,
    RichLog,
    Static,
    TabbedContent,
    TabPane,
)

from modak.graph import from_state

STATUS_ORDER = {
    "done": 0,
    "skipped": 1,
    "running": 2,
    "queued": 3,
    "pending": 4,
    "failed": 5,
    "canceled": 6,
}
STATUS_COLOR = {
    "done": "green",
    "skipped": "cyan",
    "running": "blue",
    "queued": "yellow",
    "pending": "white",
    "failed": "red",
    "canceled": "magenta",
}


class QueueDisplay(Static):
    selected_task: reactive[str | None] = reactive(None)
    _current_task: str | None = None
    _current_mtime: float | None = None
    _current_log_lines: int = 0

    CSS = """
QueueDisplay > #table_container,
QueueDisplay > #log_container {
    width: 100%;
    padding: 1 2;
    background: $surface;
    border: round $secondary;
    margin-bottom: 1;
}

#task_table {
    height: 100%;
    background: $boost;
}

#log_view {
    height: 100%;
    background: $panel-darken-1;
}

.section-title {
    text-style: bold;
    color: $text-muted;
    padding-bottom: 1;
}
"""

    def __init__(self, state_file: Path, *args, **kwargs):
        self.state_file = state_file
        self.state = {}
        super().__init__(*args, **kwargs)

    def compose(self) -> ComposeResult:
        yield Container(
            Static("Task Queue", classes="section-title"),
            DataTable(zebra_stripes=True, cursor_type="row", id="task_table"),
            id="table_container",
        )
        yield Container(
            Static("Log Output", classes="section-title"),
            RichLog(highlight=True, wrap=True, markup=True, id="log_view"),
            id="log_container",
        )

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns("Task", "Status", "Start Time", "End Time")
        self.set_interval(1.0, self.refresh_table)
        self.set_interval(1.0, self.refresh_log)

    @on(DataTable.RowSelected)
    def select_row(self, event: DataTable.RowSelected) -> None:
        row_key = event.row_key
        if row_key and row_key.value != self.selected_task:
            self.selected_task = row_key.value
            self.refresh_log()

    def refresh_table(self) -> None:
        table = self.query_one(DataTable)
        current_cursor_coordinate = table.cursor_coordinate
        if self.state_file.exists():
            with self.state_file.open() as f:
                self.state = json.load(f)
        else:
            self.state = {}

        def status_key(task):
            return STATUS_ORDER.get(self.state[task]["status"], 99)

        local_tz = tzlocal.get_localzone()

        def fmt_time(ts):
            if not ts:
                return ""
            return datetime.fromtimestamp(ts, tz=local_tz).strftime("%H:%M:%S")

        self.rows = []
        table.clear()
        for task in sorted(self.state, key=status_key):
            status = self.state[task]["status"]
            start = fmt_time(self.state[task].get("start_time"))
            end = fmt_time(self.state[task].get("end_time"))
            self.rows.append((task, status, start, end))
            table.add_row(
                Text(task, style="bold"),
                Text(status, style=f"bold {STATUS_COLOR[status]}"),
                start,
                end,
                key=task,
            )
        table.cursor_coordinate = current_cursor_coordinate

    def refresh_log(self) -> None:
        log_view = self.query_one(RichLog)
        if not self.selected_task:
            return
        log_path = Path(
            self.state.get(self.selected_task, {}).get("log_path", "DOES_NOT_EXIST.log")
        )

        new_task = self.selected_task != self._current_task
        self._current_task = self.selected_task
        if not log_path.exists():
            if new_task or self._current_mtime is not None:
                log_view.clear()
                log_view.write(f"No log found for {self.selected_task}")
                self._current_mtime = None
            return

        mtime = log_path.stat().st_mtime
        if not new_task and mtime == self._current_mtime:
            return

        if new_task:
            self._current_log_lines = 0
            log_view.clear()

        self._current_mtime = mtime
        content = log_path.read_text()
        lines = content.splitlines()
        if len(lines) > self._current_log_lines:
            for line in lines[self._current_log_lines :]:
                log_view.write(line)


class GraphDisplay(Static):
    def __init__(self, state_file: Path, *args, **kwargs):
        self.state_file = state_file
        self.state: str = ""
        super().__init__(*args, **kwargs)

    def on_mount(self) -> None:
        self.set_interval(1.0, self.refresh_graph)

    def refresh_graph(self) -> None:
        if self.state_file.exists():
            new_state = self.state_file.read_text()
            if new_state != self.state:
                self.state = new_state
                graph = from_state(json.loads(self.state))
                self.update(graph)
        else:
            self.state = ""
            self.update("")


class StateApp(App):
    active_tab: reactive[str] = reactive("monitor")
    CSS = """
#main {
    padding: 2;
    border: double $accent;
    height: 100%;
    width: 100%;
    background: $background;
}

QueueDisplay {
    height: 100%;
    width: 100%;
    content-align: center middle;
}

TabbedContent {
    background: $background;
    border: round $primary;
    padding: 1;
}

Tab {
    text-style: bold;
}

#info_text {
    padding: 2;
    border: round $secondary;
    background: $panel;
    color: $text;
}
"""

    BINDINGS: ClassVar = [
        Binding("q", "quit", "Exit"),
        Binding("m", "show_tab('monitor')", "Queue Monitor"),
        Binding("1", "show_tab('monitor')", "Queue Monitor", show=False),
        Binding("g", "show_tab('graph')", "Queue Graph"),
        Binding("2", "show_tab('graph')", "Queue Graph", show=False),
        Binding("i", "show_tab('info')", "Info"),
        Binding("3", "show_tab('info')", "Info", show=False),
    ]

    def __init__(self, state_file: Path, *args, **kwargs):
        self.state_file = state_file
        super().__init__(*args, **kwargs)

    def compose(self) -> ComposeResult:
        yield Header()
        with TabbedContent(initial="monitor"):
            with TabPane("Monitor", id="monitor"):
                yield Container(QueueDisplay(self.state_file), id="monitor_container")
            with TabPane("Graph", id="graph"):
                yield ScrollableContainer(
                    GraphDisplay(self.state_file), id="graph_container"
                )
            with TabPane("Info", id="info"):
                yield Static("Modak Monitor\n\nThis is an info panel.", id="info_text")
        yield Footer()

    def action_show_tab(self, tab: str) -> None:
        if tab == "monitor":
            monitor = self.query_one(QueueDisplay)
            monitor.query_one(DataTable).focus()
        elif tab != self.active_tab:
            monitor = self.query_one(QueueDisplay)
            monitor.query_one(DataTable).blur()
        self.active_tab = tab
        self.get_child_by_type(TabbedContent).active = tab

    def on_mount(self) -> None:
        self.title = "Modak Monitor"
        monitor = self.query_one(QueueDisplay)
        monitor.query_one(DataTable).focus()


@click.command()
@click.argument(
    "cwd",
    type=click.Path(exists=True, file_okay=True),
    default=".modak",
    required=False,
)
def main(cwd: Path):
    state_file = Path(cwd)
    StateApp(state_file).run()
