"""NiceGUI frontend for the file transfer application."""

from nicegui import ui

from server.models.files import FilesInfo
from server.services.file_transfer import (
    construct_full_paths,
    create_temp_zip,
    get_available_files,
)


def format_size(size: int) -> str:
    """Format a file size into a human-readable value."""
    if size < 1024:
        return f"{size} B"

    if size < 1024**2:
        return f"{size / 1024:.1f} KB"

    if size < 1024**3:
        return f"{size / 1024**2:.1f} MB"

    return f"{size / 1024**3:.1f} GB"


def render_file_list(files: list[FilesInfo]) -> list[tuple]:
    """Render the available files and return their checkboxes."""
    checkboxes: list[tuple] = []

    with ui.card().classes("w-full"):
        with ui.scroll_area().classes("w-full h-[640px]"):
            render_file_rows(
                files=files,
                checkboxes=checkboxes,
            )

    return checkboxes


def render_file_rows(
    files: list[FilesInfo],
    checkboxes: list[tuple],
) -> None:
    """Render a checkbox row for every available file."""
    with ui.column().classes("w-full gap-0"):
        for file in files:
            checkbox = ui.checkbox(f"{file.name} - {format_size(file.size)}")

            checkboxes.append((checkbox, file.name))

            ui.separator()


def toggle_all_files(
    checkboxes: list[tuple],
    toggle_button: ui.button,
) -> None:
    """Select or deselect all files."""
    all_selected = all(checkbox.value for checkbox, _ in checkboxes)

    for checkbox, _ in checkboxes:
        checkbox.set_value(not all_selected)

    toggle_button.text = "Select all" if all_selected else "Deselect all"


def download_selected_files(
    checkboxes: list[tuple],
) -> None:
    """Download all selected files as a zip archive."""
    selected_files = [filename for checkbox, filename in checkboxes if checkbox.value]

    if not selected_files:
        ui.notify(
            "Select at least one file",
            type="warning",
        )
        return

    full_paths = construct_full_paths(selected_files)

    zip_name = create_temp_zip(full_paths)

    ui.download(
        zip_name,
        filename="files.zip",
    )


def render_actions(
    checkboxes: list[tuple],
) -> None:
    """Render the file selection actions."""
    toggle_button = ui.button("Select all")

    toggle_button.on(
        "click",
        lambda: toggle_all_files(
            checkboxes=checkboxes,
            toggle_button=toggle_button,
        ),
    )

    ui.button(
        "Download selected",
        on_click=lambda: download_selected_files(checkboxes),
    )


@ui.page("/")
def index_page() -> None:
    """Render the file transfer landing page."""
    ui.page_title("File Transfer")

    files = get_available_files()

    ui.label("File Transfer").classes("text-3xl font-bold")

    checkboxes = render_file_list(files)

    with ui.row().classes("gap-3"):
        render_actions(checkboxes)
